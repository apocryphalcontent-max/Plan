#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Database Connection Manager
Provides connection pooling, query execution utilities, and repository patterns.

This module implements:
- Thread-safe connection pooling
- Automatic retry logic for transient failures
- Context managers for transaction handling
- Repository pattern for domain-specific queries
- SQL injection protection via parameterized queries

Usage:
    from scripts.database import get_db, init_db, close_db

    # Initialize at application startup
    if not init_db():
        sys.exit(1)

    # Get database manager
    db = get_db()

    # Use transactions
    with db.transaction() as conn:
        db.execute("INSERT INTO ...", params)
"""

import sys
import logging
import time
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Generator, Union, Tuple
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import psycopg2
    from psycopg2 import pool, extras, OperationalError, InterfaceError
    from psycopg2.extensions import connection as PgConnection
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    OperationalError = Exception  # Fallback for type hints
    InterfaceError = Exception

from config.settings import config, DatabaseConfig

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1.0  # seconds
RETRY_DELAY_MULTIPLIER = 2.0


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


class ConnectionError(DatabaseError):
    """Exception for connection failures."""
    pass


class QueryError(DatabaseError):
    """Exception for query execution failures."""
    pass


def with_retry(max_retries: int = MAX_RETRIES,
               delay_base: float = RETRY_DELAY_BASE,
               retryable_exceptions: tuple = None):
    """
    Decorator that adds retry logic for transient database failures.

    Args:
        max_retries: Maximum number of retry attempts.
        delay_base: Base delay between retries (exponential backoff).
        retryable_exceptions: Tuple of exception types to retry on.
    """
    if retryable_exceptions is None:
        retryable_exceptions = (OperationalError, InterfaceError) if PSYCOPG2_AVAILABLE else ()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = delay_base * (RETRY_DELAY_MULTIPLIER ** attempt)
                        logger.warning(f"Database operation failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                        logger.info(f"Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"Database operation failed after {max_retries + 1} attempts")
            raise last_exception
        return wrapper
    return decorator


class DatabaseManager:
    """
    Database connection manager with connection pooling.
    Provides context managers for safe transaction handling.
    """
    
    def __init__(self, db_config: Optional[DatabaseConfig] = None):
        self.config = db_config or config.database
        self._pool: Optional[pool.ThreadedConnectionPool] = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the connection pool"""
        if not PSYCOPG2_AVAILABLE:
            logger.error("psycopg2 is not available. Cannot initialize database.")
            return False
        
        try:
            self._pool = pool.ThreadedConnectionPool(
                minconn=self.config.min_connections,
                maxconn=self.config.max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                connect_timeout=self.config.connect_timeout
            )
            self._initialized = True
            logger.info(f"Database pool initialized: {self.config.database}@{self.config.host}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            return False
    
    def close(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            self._initialized = False
            logger.info("Database pool closed")
    
    @contextmanager
    def get_connection(self) -> Generator[PgConnection, None, None]:
        """Get a connection from the pool with automatic return"""
        if not self._initialized:
            if not self.initialize():
                raise DatabaseError("Database not initialized")
        
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        finally:
            if conn:
                self._pool.putconn(conn)
    
    @contextmanager
    def transaction(self) -> Generator[PgConnection, None, None]:
        """Context manager for transactions with automatic commit/rollback"""
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Transaction rolled back: {e}")
                raise
    
    def execute(self, query: str, params: tuple = None) -> int:
        """Execute a query and return affected row count"""
        with self.transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute a query with multiple parameter sets"""
        with self.transaction() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, params_list)
                return cur.rowcount
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """Fetch a single row as dictionary"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, params)
                row = cur.fetchone()
                return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Fetch all rows as list of dictionaries"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def fetch_batch(self, query: str, params: tuple = None, 
                    batch_size: int = 1000) -> Generator[List[Dict[str, Any]], None, None]:
        """Fetch rows in batches for memory efficiency"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor, 
                           name='batch_cursor') as cur:
                cur.execute(query, params)
                while True:
                    rows = cur.fetchmany(batch_size)
                    if not rows:
                        break
                    yield [dict(row) for row in rows]
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
        """
        result = self.fetch_one(query, (table_name,))
        return result.get('exists', False) if result else False
    
    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.fetch_one(query)
        return result.get('count', 0) if result else 0
    
    def run_schema_file(self, schema_path: Path) -> bool:
        """Execute a SQL schema file"""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            with self.transaction() as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
            
            logger.info(f"Schema executed successfully: {schema_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to execute schema: {e}")
            return False


# ============================================================================
# QUERY BUILDERS
# ============================================================================

# Valid SQL identifier pattern (letters, digits, underscores, starting with letter/underscore)
VALID_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

# Allowed table names (whitelist for safety)
ALLOWED_TABLES = frozenset({
    'canonical_books', 'verses', 'events', 'motifs', 'motif_activations',
    'typological_correspondences', 'sensory_vocabulary', 'patristic_sources',
    'hermeneutical_principles', 'cross_references', 'processing_queue'
})


def validate_identifier(identifier: str, identifier_type: str = "identifier") -> str:
    """
    Validate a SQL identifier to prevent injection attacks.

    Args:
        identifier: The identifier to validate.
        identifier_type: Type of identifier for error messages.

    Returns:
        The validated identifier.

    Raises:
        ValueError: If the identifier is invalid.
    """
    if not identifier:
        raise ValueError(f"Empty {identifier_type} not allowed")

    if not VALID_IDENTIFIER.match(identifier):
        raise ValueError(f"Invalid {identifier_type}: {identifier!r}")

    return identifier


def validate_table_name(table: str) -> str:
    """
    Validate a table name against the allowed whitelist.

    Args:
        table: The table name to validate.

    Returns:
        The validated table name.

    Raises:
        ValueError: If the table name is not in the whitelist.
    """
    validate_identifier(table, "table name")

    if table.lower() not in ALLOWED_TABLES:
        raise ValueError(f"Table not in allowed list: {table!r}")

    return table


class QueryBuilder:
    """
    Helper class for building SQL queries safely.

    All methods validate identifiers to prevent SQL injection.
    Use parameterized queries for all values.
    """

    @staticmethod
    def insert(table: str, columns: List[str],
               on_conflict: Optional[str] = None) -> str:
        """
        Build an INSERT query with parameterized placeholders.

        Args:
            table: Table name (must be in ALLOWED_TABLES).
            columns: List of column names.
            on_conflict: Optional ON CONFLICT clause.

        Returns:
            Parameterized INSERT query string.
        """
        validate_table_name(table)
        validated_cols = [validate_identifier(c, "column name") for c in columns]

        cols = ", ".join(validated_cols)
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

        if on_conflict:
            query += f" ON CONFLICT {on_conflict}"

        return query

    @staticmethod
    def update(table: str, columns: List[str],
               where_clause: str) -> str:
        """
        Build an UPDATE query with parameterized placeholders.

        Args:
            table: Table name (must be in ALLOWED_TABLES).
            columns: List of column names to update.
            where_clause: WHERE clause (use %s placeholders for values).

        Returns:
            Parameterized UPDATE query string.
        """
        validate_table_name(table)
        validated_cols = [validate_identifier(c, "column name") for c in columns]

        set_clause = ", ".join([f"{col} = %s" for col in validated_cols])
        return f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

    @staticmethod
    def select(table: str, columns: List[str] = None,
               where_clause: str = None, order_by: str = None,
               limit: int = None) -> str:
        """
        Build a SELECT query.

        Args:
            table: Table name (must be in ALLOWED_TABLES).
            columns: List of column names (None for *).
            where_clause: Optional WHERE clause (use %s placeholders).
            order_by: Optional ORDER BY clause.
            limit: Optional LIMIT value.

        Returns:
            SELECT query string.
        """
        validate_table_name(table)

        if columns:
            validated_cols = [validate_identifier(c, "column name") for c in columns]
            cols = ", ".join(validated_cols)
        else:
            cols = "*"

        query = f"SELECT {cols} FROM {table}"

        if where_clause:
            query += f" WHERE {where_clause}"
        if order_by:
            # Validate order_by column names
            for part in order_by.split(','):
                col = part.strip().split()[0]  # Get column name (ignore ASC/DESC)
                validate_identifier(col, "order by column")
            query += f" ORDER BY {order_by}"
        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError(f"Invalid limit: {limit}")
            query += f" LIMIT {limit}"

        return query


# ============================================================================
# VERSE REPOSITORY
# ============================================================================

class VerseRepository:
    """Repository for verse-related database operations"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_verse(self, verse_reference: str) -> Optional[Dict[str, Any]]:
        """Get a verse by reference"""
        query = "SELECT * FROM verses WHERE verse_reference = %s"
        return self.db.fetch_one(query, (verse_reference,))
    
    def get_verses_by_book(self, book_id: int) -> List[Dict[str, Any]]:
        """Get all verses for a book"""
        query = """
            SELECT v.*, cb.name as book_name, cb.category
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.book_id = %s
            ORDER BY v.chapter, v.verse_number
        """
        return self.db.fetch_all(query, (book_id,))
    
    def get_unprocessed_verses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get verses that need processing"""
        query = """
            SELECT v.*, cb.name as book_name, cb.category
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.status IN ('raw', 'parsed')
            ORDER BY cb.canonical_order, v.chapter, v.verse_number
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))
    
    def update_verse_senses(self, verse_id: int, senses: Dict[str, str]) -> bool:
        """Update fourfold senses for a verse"""
        query = """
            UPDATE verses SET
                sense_literal = %s,
                sense_allegorical = %s,
                sense_tropological = %s,
                sense_anagogical = %s,
                status = 'fleshed_out',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        params = (
            senses.get('literal'),
            senses.get('allegorical'),
            senses.get('tropological'),
            senses.get('anagogical'),
            verse_id
        )
        return self.db.execute(query, params) > 0
    
    def update_verse_status(self, verse_id: int, status: str, 
                           error_log: str = None) -> bool:
        """Update verse processing status"""
        if error_log:
            query = """
                UPDATE verses SET
                    status = %s,
                    failure_log = %s,
                    retry_count = retry_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            return self.db.execute(query, (status, error_log, verse_id)) > 0
        else:
            query = """
                UPDATE verses SET
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            return self.db.execute(query, (status, verse_id)) > 0
    
    def get_completion_stats(self) -> Dict[str, Any]:
        """Get processing completion statistics"""
        query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM verses
            GROUP BY status
        """
        rows = self.db.fetch_all(query)
        return {row['status']: row['count'] for row in rows}


# ============================================================================
# MOTIF REPOSITORY
# ============================================================================

class MotifRepository:
    """Repository for motif-related database operations"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_all_motifs(self) -> List[Dict[str, Any]]:
        """Get all motifs"""
        return self.db.fetch_all("SELECT * FROM motifs ORDER BY foundation_layer, name")
    
    def get_active_motifs_at_page(self, page: int) -> List[Dict[str, Any]]:
        """Get motifs that are active at a given page"""
        query = """
            SELECT * FROM motifs
            WHERE %s BETWEEN planting_page AND convergence_page
            ORDER BY foundation_layer, name
        """
        return self.db.fetch_all(query, (page,))
    
    def update_motif_status(self, motif_id: int, status: str, 
                           last_page: int = None) -> bool:
        """Update motif activation status"""
        if last_page:
            query = """
                UPDATE motifs SET
                    current_status = %s,
                    last_activation_page = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            return self.db.execute(query, (status, last_page, motif_id)) > 0
        else:
            query = """
                UPDATE motifs SET
                    current_status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            return self.db.execute(query, (status, motif_id)) > 0
    
    def record_activation(self, motif_id: int, page: int, 
                         activation_type: str, verse_id: int = None,
                         vocabulary_used: List[str] = None) -> int:
        """Record a motif activation"""
        query = """
            INSERT INTO motif_activations 
            (motif_id, page_number, activation_type, verse_id, vocabulary_used)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.db.fetch_one(query, (
            motif_id, page, activation_type, verse_id, vocabulary_used
        ))
        return result['id'] if result else 0


# ============================================================================
# SINGLETON DATABASE INSTANCE
# ============================================================================

# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> DatabaseManager:
    """Get the global database manager instance"""
    return db_manager


def init_db() -> bool:
    """Initialize the global database manager"""
    return db_manager.initialize()


def close_db():
    """Close the global database manager"""
    db_manager.close()
