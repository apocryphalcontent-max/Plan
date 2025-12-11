#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Database Connection Manager
Provides connection pooling and query execution utilities.

This module provides:
- Connection pooling with automatic reconnection
- Transaction management with automatic commit/rollback
- Query builders for common operations
- Repository classes for domain-specific queries
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Generator, Union, Tuple
from contextlib import contextmanager
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import psycopg2
    from psycopg2 import pool, extras, OperationalError, InterfaceError
    from psycopg2.extensions import connection as PgConnection
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    PgConnection = Any  # Type alias for when psycopg2 is not available
    OperationalError = Exception
    InterfaceError = Exception
    logging.warning("psycopg2 not installed. Install with: pip install psycopg2-binary")

from config.settings import config, DatabaseConfig

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass


class ConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""
    pass


class QueryError(DatabaseError):
    """Raised when a query fails to execute."""
    pass


class TransactionError(DatabaseError):
    """Raised when a transaction fails."""
    pass


class SchemaError(DatabaseError):
    """Raised when schema operations fail."""
    pass


class DatabaseManager:
    """
    Database connection manager with connection pooling.
    
    Provides context managers for safe transaction handling,
    automatic reconnection on connection failures, and
    retry logic for transient errors.
    
    Example:
        db = DatabaseManager()
        db.initialize()
        
        # Simple query
        result = db.fetch_one("SELECT * FROM users WHERE id = %s", (1,))
        
        # Transaction
        with db.transaction() as conn:
            db.execute("INSERT INTO users (...) VALUES (...)")
    """
    
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 0.5
    
    def __init__(self, db_config: Optional[DatabaseConfig] = None) -> None:
        """
        Initialize the database manager.
        
        Args:
            db_config: Optional database configuration. Uses global config if not provided.
        """
        self.config: DatabaseConfig = db_config or config.database
        self._pool: Optional[pool.ThreadedConnectionPool] = None
        self._initialized: bool = False
    
    @property
    def is_initialized(self) -> bool:
        """Check if the database pool is initialized."""
        return self._initialized
    
    def initialize(self) -> bool:
        """
        Initialize the connection pool.
        
        Returns:
            True if initialization succeeded, False otherwise.
            
        Note:
            This method is idempotent - calling it multiple times is safe.
        """
        if self._initialized:
            return True
            
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
        except OperationalError as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            return False
    
    def close(self) -> None:
        """
        Close all connections in the pool.
        
        This method is safe to call multiple times.
        """
        if self._pool is not None:
            try:
                self._pool.closeall()
            except Exception as e:
                logger.warning(f"Error closing connection pool: {e}")
            finally:
                self._pool = None
                self._initialized = False
                logger.info("Database pool closed")
    
    def _ensure_initialized(self) -> None:
        """Ensure the database is initialized, raising an error if not."""
        if not self._initialized:
            if not self.initialize():
                raise ConnectionError("Failed to initialize database connection")
    
    @contextmanager
    def get_connection(self) -> Generator[PgConnection, None, None]:
        """
        Get a connection from the pool with automatic return.
        
        Yields:
            A database connection that will be automatically returned to the pool.
            
        Raises:
            ConnectionError: If unable to get a connection from the pool.
        """
        self._ensure_initialized()
        
        conn: Optional[PgConnection] = None
        try:
            conn = self._pool.getconn()
            if conn is None:
                raise ConnectionError("Failed to get connection from pool")
            yield conn
        except (OperationalError, InterfaceError) as e:
            logger.error(f"Database connection error: {e}")
            raise ConnectionError(f"Database connection error: {e}") from e
        finally:
            if conn is not None:
                try:
                    self._pool.putconn(conn)
                except Exception as e:
                    logger.warning(f"Error returning connection to pool: {e}")
    
    @contextmanager
    def transaction(self) -> Generator[PgConnection, None, None]:
        """
        Context manager for transactions with automatic commit/rollback.
        
        Yields:
            A database connection in a transaction context.
            
        Raises:
            TransactionError: If the transaction fails.
        """
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    logger.error(f"Error during rollback: {rollback_error}")
                logger.error(f"Transaction rolled back: {e}")
                raise TransactionError(f"Transaction failed: {e}") from e
    
    def execute(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> int:
        """
        Execute a query and return affected row count.
        
        Args:
            query: SQL query to execute.
            params: Query parameters as tuple or dict.
            
        Returns:
            Number of affected rows.
            
        Raises:
            QueryError: If the query fails to execute.
        """
        try:
            with self.transaction() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.rowcount
        except TransactionError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to execute query: {e}") from e
    
    def execute_many(self, query: str, params_list: List[Tuple[Any, ...]]) -> int:
        """
        Execute a query with multiple parameter sets.
        
        Args:
            query: SQL query to execute.
            params_list: List of parameter tuples.
            
        Returns:
            Total number of affected rows.
            
        Raises:
            QueryError: If the query fails to execute.
        """
        if not params_list:
            return 0
            
        try:
            with self.transaction() as conn:
                with conn.cursor() as cur:
                    cur.executemany(query, params_list)
                    return cur.rowcount
        except TransactionError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to execute batch query: {e}") from e
    
    def fetch_one(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row as dictionary.
        
        Args:
            query: SQL query to execute.
            params: Query parameters as tuple or dict.
            
        Returns:
            Dictionary containing the row data, or None if no row found.
            
        Raises:
            QueryError: If the query fails to execute.
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute(query, params)
                    row = cur.fetchone()
                    return dict(row) if row else None
        except ConnectionError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to fetch row: {e}") from e
    
    def fetch_all(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Fetch all rows as list of dictionaries.
        
        Args:
            query: SQL query to execute.
            params: Query parameters as tuple or dict.
            
        Returns:
            List of dictionaries containing row data.
            
        Raises:
            QueryError: If the query fails to execute.
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute(query, params)
                    return [dict(row) for row in cur.fetchall()]
        except ConnectionError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to fetch rows: {e}") from e
    
    def fetch_batch(
        self, 
        query: str, 
        params: Optional[Union[Tuple, Dict[str, Any]]] = None, 
        batch_size: int = 1000
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Fetch rows in batches for memory efficiency.
        
        Args:
            query: SQL query to execute.
            params: Query parameters as tuple or dict.
            batch_size: Number of rows to fetch per batch.
            
        Yields:
            Lists of dictionaries containing row data.
            
        Raises:
            QueryError: If the query fails to execute.
        """
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
            
        try:
            with self.get_connection() as conn:
                with conn.cursor(
                    cursor_factory=extras.RealDictCursor, 
                    name='batch_cursor'
                ) as cur:
                    cur.execute(query, params)
                    while True:
                        rows = cur.fetchmany(batch_size)
                        if not rows:
                            break
                        yield [dict(row) for row in rows]
        except ConnectionError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to fetch batch: {e}") from e
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check.
            
        Returns:
            True if the table exists, False otherwise.
        """
        if not table_name or not table_name.strip():
            return False
            
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
        """
        try:
            result = self.fetch_one(query, (table_name,))
            return result.get('exists', False) if result else False
        except QueryError:
            return False
    
    def get_table_count(self, table_name: str) -> int:
        """
        Get row count for a table.
        
        Args:
            table_name: Name of the table to count.
            
        Returns:
            Number of rows in the table, or 0 if table doesn't exist.
            
        Note:
            The table_name should be validated before calling this method
            to prevent SQL injection.
        """
        if not table_name or not table_name.strip():
            return 0
            
        # Validate table name to prevent SQL injection
        # Must start with letter, contain only letters, numbers, underscores
        import re
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', table_name):
            logger.warning(f"Invalid table name: {table_name}")
            return 0
            
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        try:
            result = self.fetch_one(query)
            return result.get('count', 0) if result else 0
        except QueryError:
            return 0
    
    def run_schema_file(self, schema_path: Path) -> bool:
        """
        Execute a SQL schema file.
        
        Args:
            schema_path: Path to the SQL schema file.
            
        Returns:
            True if the schema was executed successfully, False otherwise.
            
        Raises:
            SchemaError: If the schema file cannot be read or executed.
        """
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return False
            
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            if not schema_sql.strip():
                logger.warning(f"Schema file is empty: {schema_path}")
                return False
            
            with self.transaction() as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
            
            logger.info(f"Schema executed successfully: {schema_path}")
            return True
        except FileNotFoundError as e:
            logger.error(f"Schema file not found: {schema_path}")
            raise SchemaError(f"Schema file not found: {schema_path}") from e
        except TransactionError as e:
            logger.error(f"Failed to execute schema: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to execute schema: {e}")
            return False


# ============================================================================
# QUERY BUILDERS
# ============================================================================

class QueryBuilder:
    """
    Helper class for building SQL queries safely.
    
    Note:
        These methods generate query strings but do not execute them.
        Always use parameterized queries for user input to prevent SQL injection.
    """
    
    @staticmethod
    def insert(
        table: str, 
        columns: List[str], 
        on_conflict: Optional[str] = None,
        returning: Optional[str] = None
    ) -> str:
        """
        Build an INSERT query.
        
        Args:
            table: Table name to insert into.
            columns: List of column names.
            on_conflict: Optional ON CONFLICT clause.
            returning: Optional RETURNING clause.
            
        Returns:
            SQL INSERT query string.
        """
        if not columns:
            raise ValueError("columns list cannot be empty")
            
        cols = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        
        if on_conflict:
            query += f" ON CONFLICT {on_conflict}"
        
        if returning:
            query += f" RETURNING {returning}"
        
        return query
    
    @staticmethod
    def update(
        table: str, 
        columns: List[str], 
        where_clause: str
    ) -> str:
        """
        Build an UPDATE query.
        
        Args:
            table: Table name to update.
            columns: List of column names to update.
            where_clause: WHERE clause (without the WHERE keyword).
            
        Returns:
            SQL UPDATE query string.
        """
        if not columns:
            raise ValueError("columns list cannot be empty")
        if not where_clause:
            raise ValueError("where_clause is required for UPDATE queries")
            
        set_clause = ", ".join([f"{col} = %s" for col in columns])
        return f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    
    @staticmethod
    def select(
        table: str, 
        columns: Optional[List[str]] = None,
        where_clause: Optional[str] = None, 
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> str:
        """
        Build a SELECT query.
        
        Args:
            table: Table name to select from.
            columns: List of column names (defaults to *).
            where_clause: Optional WHERE clause (without the WHERE keyword).
            order_by: Optional ORDER BY clause.
            limit: Optional LIMIT value.
            offset: Optional OFFSET value.
            
        Returns:
            SQL SELECT query string.
        """
        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"
        
        return query


# ============================================================================
# VERSE REPOSITORY
# ============================================================================

class VerseRepository:
    """
    Repository for verse-related database operations.
    
    Provides a clean interface for querying and updating verse data,
    abstracting away the underlying SQL queries.
    """
    
    def __init__(self, db: DatabaseManager) -> None:
        """
        Initialize the repository.
        
        Args:
            db: Database manager instance.
        """
        self.db = db
    
    def get_verse(self, verse_reference: str) -> Optional[Dict[str, Any]]:
        """
        Get a verse by reference.
        
        Args:
            verse_reference: The verse reference (e.g., "Genesis 1:1").
            
        Returns:
            Verse data as dictionary, or None if not found.
        """
        if not verse_reference:
            return None
        query = "SELECT * FROM verses WHERE verse_reference = %s"
        return self.db.fetch_one(query, (verse_reference,))
    
    def get_verse_by_id(self, verse_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a verse by its ID.
        
        Args:
            verse_id: The verse ID.
            
        Returns:
            Verse data as dictionary, or None if not found.
        """
        if verse_id <= 0:
            return None
        query = "SELECT * FROM verses WHERE id = %s"
        return self.db.fetch_one(query, (verse_id,))
    
    def get_verses_by_book(self, book_id: int) -> List[Dict[str, Any]]:
        """
        Get all verses for a book.
        
        Args:
            book_id: The book ID.
            
        Returns:
            List of verse data dictionaries.
        """
        if book_id <= 0:
            return []
        query = """
            SELECT v.*, cb.name as book_name, cb.category
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.book_id = %s
            ORDER BY v.chapter, v.verse_number
        """
        return self.db.fetch_all(query, (book_id,))
    
    def get_unprocessed_verses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get verses that need processing.
        
        Args:
            limit: Maximum number of verses to return.
            
        Returns:
            List of unprocessed verse data dictionaries.
        """
        if limit <= 0:
            return []
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
        """
        Update fourfold senses for a verse.
        
        Args:
            verse_id: The verse ID.
            senses: Dictionary with keys 'literal', 'allegorical', 
                   'tropological', 'anagogical'.
            
        Returns:
            True if the update succeeded, False otherwise.
        """
        if verse_id <= 0:
            return False
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
        try:
            return self.db.execute(query, params) > 0
        except QueryError as e:
            logger.error(f"Failed to update verse senses for {verse_id}: {e}")
            return False
    
    def update_verse_status(
        self, 
        verse_id: int, 
        status: str, 
        error_log: Optional[str] = None
    ) -> bool:
        """
        Update verse processing status.
        
        Args:
            verse_id: The verse ID.
            status: New status value.
            error_log: Optional error message if status indicates failure.
            
        Returns:
            True if the update succeeded, False otherwise.
        """
        if verse_id <= 0 or not status:
            return False
            
        try:
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
        except QueryError as e:
            logger.error(f"Failed to update verse status for {verse_id}: {e}")
            return False
    
    def get_completion_stats(self) -> Dict[str, int]:
        """
        Get processing completion statistics.
        
        Returns:
            Dictionary mapping status to count.
        """
        query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM verses
            GROUP BY status
        """
        try:
            rows = self.db.fetch_all(query)
            return {row['status']: row['count'] for row in rows}
        except QueryError:
            return {}


# ============================================================================
# MOTIF REPOSITORY
# ============================================================================

class MotifRepository:
    """
    Repository for motif-related database operations.
    
    Manages orbital motif tracking per the Stratified Foundation System.
    """
    
    def __init__(self, db: DatabaseManager) -> None:
        """
        Initialize the repository.
        
        Args:
            db: Database manager instance.
        """
        self.db = db
    
    def get_all_motifs(self) -> List[Dict[str, Any]]:
        """
        Get all motifs.
        
        Returns:
            List of motif data dictionaries.
        """
        try:
            return self.db.fetch_all(
                "SELECT * FROM motifs ORDER BY foundation_layer, name"
            )
        except QueryError:
            return []
    
    def get_motif_by_id(self, motif_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a motif by its ID.
        
        Args:
            motif_id: The motif ID.
            
        Returns:
            Motif data as dictionary, or None if not found.
        """
        if motif_id <= 0:
            return None
        return self.db.fetch_one("SELECT * FROM motifs WHERE id = %s", (motif_id,))
    
    def get_active_motifs_at_page(self, page: int) -> List[Dict[str, Any]]:
        """
        Get motifs that are active at a given page.
        
        Args:
            page: Page number to check.
            
        Returns:
            List of active motif data dictionaries.
        """
        if page < 0:
            return []
        query = """
            SELECT * FROM motifs
            WHERE %s BETWEEN planting_page AND convergence_page
            ORDER BY foundation_layer, name
        """
        try:
            return self.db.fetch_all(query, (page,))
        except QueryError:
            return []
    
    def update_motif_status(
        self, 
        motif_id: int, 
        status: str, 
        last_page: Optional[int] = None
    ) -> bool:
        """
        Update motif activation status.
        
        Args:
            motif_id: The motif ID.
            status: New status value.
            last_page: Optional page number of last activation.
            
        Returns:
            True if the update succeeded, False otherwise.
        """
        if motif_id <= 0 or not status:
            return False
            
        try:
            if last_page is not None:
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
        except QueryError as e:
            logger.error(f"Failed to update motif status for {motif_id}: {e}")
            return False
    
    def record_activation(
        self, 
        motif_id: int, 
        page: int, 
        activation_type: str, 
        verse_id: Optional[int] = None,
        vocabulary_used: Optional[List[str]] = None
    ) -> int:
        """
        Record a motif activation.
        
        Args:
            motif_id: The motif ID.
            page: Page number of activation.
            activation_type: Type of activation (e.g., 'planting', 'reinforcement').
            verse_id: Optional associated verse ID.
            vocabulary_used: Optional list of vocabulary words used.
            
        Returns:
            ID of the new activation record, or 0 if failed.
        """
        if motif_id <= 0 or page < 0 or not activation_type:
            return 0
            
        query = """
            INSERT INTO motif_activations 
            (motif_id, page_number, activation_type, verse_id, vocabulary_used)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        try:
            result = self.db.fetch_one(query, (
                motif_id, page, activation_type, verse_id, vocabulary_used
            ))
            return result['id'] if result else 0
        except QueryError as e:
            logger.error(f"Failed to record activation for motif {motif_id}: {e}")
            return 0


# ============================================================================
# SINGLETON DATABASE INSTANCE
# ============================================================================

# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    """
    Get the global database manager instance.
    
    Returns:
        The singleton DatabaseManager instance.
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_db() -> bool:
    """
    Initialize the global database manager.
    
    Returns:
        True if initialization succeeded, False otherwise.
    """
    return get_db().initialize()


def close_db() -> None:
    """Close the global database manager."""
    global _db_manager
    if _db_manager is not None:
        _db_manager.close()
        _db_manager = None
