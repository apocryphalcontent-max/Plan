#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Batch Orchestration System
Advanced batch processing with parallelization, resumption, and monitoring
"""

import sys
import time
import json
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from queue import Queue, Empty
import signal

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, LOGS_DIR
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# BATCH STATUS AND CONFIGURATION
# ============================================================================

class BatchStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    batch_size: int = 100
    max_workers: int = 4
    max_retries: int = 3
    retry_delay: float = 2.0
    checkpoint_interval: int = 50  # Save progress every N items
    timeout_per_item: float = 30.0
    pause_on_error_threshold: int = 10  # Pause if errors exceed this
    enable_resumption: bool = True
    progress_callback: Optional[Callable] = None


@dataclass
class BatchProgress:
    """Track batch processing progress"""
    batch_id: str
    total_items: int = 0
    processed: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_checkpoint: datetime = field(default_factory=datetime.now)
    current_item: str = ""
    errors: List[Dict] = field(default_factory=list)
    status: BatchStatus = BatchStatus.PENDING
    
    @property
    def elapsed_time(self) -> timedelta:
        return datetime.now() - self.start_time
    
    @property
    def items_per_second(self) -> float:
        elapsed = self.elapsed_time.total_seconds()
        return self.processed / elapsed if elapsed > 0 else 0
    
    @property
    def estimated_remaining(self) -> timedelta:
        if self.items_per_second > 0:
            remaining_items = self.total_items - self.processed
            seconds = remaining_items / self.items_per_second
            return timedelta(seconds=seconds)
        return timedelta(0)
    
    @property
    def completion_percentage(self) -> float:
        return (self.processed / self.total_items * 100) if self.total_items > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            'batch_id': self.batch_id,
            'total_items': self.total_items,
            'processed': self.processed,
            'successful': self.successful,
            'failed': self.failed,
            'skipped': self.skipped,
            'elapsed_seconds': self.elapsed_time.total_seconds(),
            'items_per_second': self.items_per_second,
            'completion_percentage': self.completion_percentage,
            'status': self.status.value,
            'recent_errors': self.errors[-5:] if self.errors else []
        }


# ============================================================================
# CHECKPOINT MANAGER
# ============================================================================

class CheckpointManager:
    """Manage batch processing checkpoints for resumption"""
    
    def __init__(self, checkpoint_dir: Path = None):
        self.checkpoint_dir = checkpoint_dir or (LOGS_DIR / "checkpoints")
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(self, batch_id: str, progress: BatchProgress, 
                       processed_ids: List[int]):
        """Save checkpoint for later resumption"""
        checkpoint = {
            'batch_id': batch_id,
            'timestamp': datetime.now().isoformat(),
            'progress': progress.to_dict(),
            'processed_ids': processed_ids,
            'last_successful_id': processed_ids[-1] if processed_ids else None
        }
        
        checkpoint_file = self.checkpoint_dir / f"{batch_id}.checkpoint.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        logger.debug(f"Checkpoint saved: {checkpoint_file}")
    
    def load_checkpoint(self, batch_id: str) -> Optional[Dict]:
        """Load checkpoint if exists"""
        checkpoint_file = self.checkpoint_dir / f"{batch_id}.checkpoint.json"
        
        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return None
    
    def clear_checkpoint(self, batch_id: str):
        """Clear checkpoint after successful completion"""
        checkpoint_file = self.checkpoint_dir / f"{batch_id}.checkpoint.json"
        if checkpoint_file.exists():
            checkpoint_file.unlink()
            logger.debug(f"Checkpoint cleared: {checkpoint_file}")
    
    def list_checkpoints(self) -> List[Dict]:
        """List all available checkpoints"""
        checkpoints = []
        for f in self.checkpoint_dir.glob("*.checkpoint.json"):
            with open(f, 'r') as file:
                data = json.load(file)
                checkpoints.append({
                    'batch_id': data['batch_id'],
                    'timestamp': data['timestamp'],
                    'processed': data['progress']['processed'],
                    'total': data['progress']['total_items']
                })
        return checkpoints


# ============================================================================
# BATCH PROCESSOR
# ============================================================================

class BatchProcessor:
    """Advanced batch processor with parallel execution"""
    
    def __init__(self, db: DatabaseManager = None, config: BatchConfig = None):
        self.db = db or get_db()
        self.config = config or BatchConfig()
        self.checkpoint_manager = CheckpointManager()
        self._stop_flag = threading.Event()
        self._pause_flag = threading.Event()
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)
    
    def _handle_interrupt(self, signum, frame):
        """Handle interrupt signals gracefully"""
        logger.warning("Interrupt received, stopping gracefully...")
        self._stop_flag.set()
    
    def process_verses(self, batch_id: str = None, 
                      where_clause: str = None,
                      resume: bool = True) -> BatchProgress:
        """Process verses in batches with full orchestration"""
        from scripts.processing import VerseProcessor
        
        batch_id = batch_id or f"verse_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Check for existing checkpoint
        processed_ids = []
        if resume:
            checkpoint = self.checkpoint_manager.load_checkpoint(batch_id)
            if checkpoint:
                processed_ids = checkpoint.get('processed_ids', [])
                logger.info(f"Resuming from checkpoint: {len(processed_ids)} already processed")
        
        # Get verses to process
        query = """
            SELECT v.id, v.verse_reference
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.status IN ('raw', 'parsed', 'analyzed')
        """
        
        if processed_ids:
            query += f" AND v.id NOT IN ({','.join(map(str, processed_ids))})"
        
        if where_clause:
            query += f" AND ({where_clause})"
        
        query += " ORDER BY cb.canonical_order, v.chapter, v.verse_number"
        
        verses = self.db.fetch_all(query)
        
        # Initialize progress
        progress = BatchProgress(
            batch_id=batch_id,
            total_items=len(verses) + len(processed_ids),
            processed=len(processed_ids),
            successful=len(processed_ids),
            status=BatchStatus.RUNNING
        )
        
        logger.info(f"Starting batch {batch_id}: {len(verses)} verses to process")
        
        # Process in parallel
        processor = VerseProcessor(self.db)
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {}
            
            for verse in verses:
                if self._stop_flag.is_set():
                    progress.status = BatchStatus.CANCELLED
                    break
                
                while self._pause_flag.is_set():
                    time.sleep(1)
                
                future = executor.submit(self._process_single_verse, processor, verse)
                futures[future] = verse
            
            for future in as_completed(futures):
                verse = futures[future]
                progress.current_item = verse['verse_reference']
                
                try:
                    success = future.result(timeout=self.config.timeout_per_item)
                    progress.processed += 1
                    
                    if success:
                        progress.successful += 1
                        processed_ids.append(verse['id'])
                    else:
                        progress.failed += 1
                        progress.errors.append({
                            'id': verse['id'],
                            'reference': verse['verse_reference'],
                            'error': 'Processing returned False'
                        })
                
                except Exception as e:
                    progress.processed += 1
                    progress.failed += 1
                    progress.errors.append({
                        'id': verse['id'],
                        'reference': verse['verse_reference'],
                        'error': str(e)
                    })
                
                # Checkpoint
                if progress.processed % self.config.checkpoint_interval == 0:
                    self.checkpoint_manager.save_checkpoint(batch_id, progress, processed_ids)
                    progress.last_checkpoint = datetime.now()
                    
                    if self.config.progress_callback:
                        self.config.progress_callback(progress)
                
                # Check error threshold
                if progress.failed >= self.config.pause_on_error_threshold:
                    logger.warning(f"Error threshold reached ({progress.failed} failures)")
                    self._pause_flag.set()
        
        # Final status
        if not self._stop_flag.is_set():
            progress.status = BatchStatus.COMPLETED
            self.checkpoint_manager.clear_checkpoint(batch_id)
        
        # Record batch in database
        self._record_batch(progress, processed_ids)
        
        logger.info(f"Batch {batch_id} complete: {progress.successful}/{progress.total_items} successful")
        return progress
    
    def _process_single_verse(self, processor, verse: Dict) -> bool:
        """Process a single verse with retry logic"""
        for attempt in range(self.config.max_retries):
            try:
                return processor.process_verse(verse['id'])
            except Exception as e:
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    raise
        return False
    
    def _record_batch(self, progress: BatchProgress, processed_ids: List[int]):
        """Record batch processing in database"""
        query = """
            INSERT INTO processing_batches 
            (batch_number, batch_type, verse_count, status, started_at, completed_at,
             success_count, failure_count, failed_verse_ids)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Extract batch number from ID
        batch_num = hash(progress.batch_id) % 1000000
        
        try:
            self.db.execute(query, (
                batch_num,
                'verse',
                progress.total_items,
                progress.status.value,
                progress.start_time,
                datetime.now(),
                progress.successful,
                progress.failed,
                [e['id'] for e in progress.errors]
            ))
        except Exception as e:
            logger.error(f"Failed to record batch: {e}")
    
    def pause(self):
        """Pause processing"""
        self._pause_flag.set()
        logger.info("Processing paused")
    
    def resume(self):
        """Resume processing"""
        self._pause_flag.clear()
        logger.info("Processing resumed")
    
    def stop(self):
        """Stop processing"""
        self._stop_flag.set()
        logger.info("Processing stopped")


# ============================================================================
# ORCHESTRATION SCHEDULER
# ============================================================================

class OrchestrationScheduler:
    """Schedule and manage multiple batch operations"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.processors: Dict[str, BatchProcessor] = {}
        self.schedules: List[Dict] = []
    
    def create_processing_plan(self, strategy: str = 'sequential') -> List[Dict]:
        """Create a processing plan based on strategy"""
        plans = []
        
        if strategy == 'sequential':
            # Process books in canonical order
            books = self.db.fetch_all("""
                SELECT cb.name, COUNT(v.id) as verse_count
                FROM canonical_books cb
                LEFT JOIN verses v ON cb.id = v.book_id
                WHERE v.status IN ('raw', 'parsed')
                GROUP BY cb.id, cb.name, cb.canonical_order
                HAVING COUNT(v.id) > 0
                ORDER BY cb.canonical_order
            """)
            
            for book in books:
                plans.append({
                    'type': 'book',
                    'name': book['name'],
                    'verse_count': book['verse_count'],
                    'priority': 'normal'
                })
        
        elif strategy == 'by_category':
            # Process by category, prioritizing Gospels
            priority_order = ['gospel', 'pentateuch', 'pauline', 'major_prophet', 
                            'poetic', 'historical', 'minor_prophet', 'general_epistle',
                            'apocalyptic', 'acts', 'deuterocanonical']
            
            for category in priority_order:
                count = self.db.fetch_one("""
                    SELECT COUNT(v.id) as count
                    FROM verses v
                    JOIN canonical_books cb ON v.book_id = cb.id
                    WHERE cb.category = %s AND v.status IN ('raw', 'parsed')
                """, (category,))
                
                if count and count['count'] > 0:
                    plans.append({
                        'type': 'category',
                        'name': category,
                        'verse_count': count['count'],
                        'priority': 'high' if category in ['gospel', 'pentateuch'] else 'normal'
                    })
        
        elif strategy == 'incomplete_first':
            # Prioritize partially completed books
            books = self.db.fetch_all("""
                SELECT 
                    cb.name,
                    COUNT(v.id) as total,
                    SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined,
                    SUM(CASE WHEN v.status IN ('raw', 'parsed') THEN 1 ELSE 0 END) as pending
                FROM canonical_books cb
                JOIN verses v ON cb.id = v.book_id
                GROUP BY cb.id, cb.name
                HAVING SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) > 0
                   AND SUM(CASE WHEN v.status IN ('raw', 'parsed') THEN 1 ELSE 0 END) > 0
                ORDER BY 
                    SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END)::float / COUNT(v.id) DESC
            """)
            
            for book in books:
                plans.append({
                    'type': 'book',
                    'name': book['name'],
                    'verse_count': book['pending'],
                    'priority': 'high',
                    'completion': book['refined'] / book['total']
                })
        
        return plans
    
    def execute_plan(self, plan: List[Dict], 
                    batch_config: BatchConfig = None) -> Dict[str, Any]:
        """Execute a processing plan"""
        config = batch_config or BatchConfig()
        results = {
            'started_at': datetime.now().isoformat(),
            'plan_items': len(plan),
            'completed': 0,
            'failed': 0,
            'details': []
        }
        
        for item in plan:
            logger.info(f"Processing plan item: {item['name']}")
            
            processor = BatchProcessor(self.db, config)
            
            if item['type'] == 'book':
                where_clause = f"cb.name = '{item['name']}'"
            elif item['type'] == 'category':
                where_clause = f"cb.category = '{item['name']}'"
            else:
                where_clause = None
            
            try:
                progress = processor.process_verses(
                    batch_id=f"{item['type']}_{item['name']}_{datetime.now().strftime('%Y%m%d')}",
                    where_clause=where_clause
                )
                
                results['details'].append({
                    'item': item['name'],
                    'status': progress.status.value,
                    'processed': progress.processed,
                    'successful': progress.successful
                })
                
                if progress.status == BatchStatus.COMPLETED:
                    results['completed'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                logger.error(f"Plan item failed: {item['name']}: {e}")
                results['failed'] += 1
                results['details'].append({
                    'item': item['name'],
                    'status': 'error',
                    'error': str(e)
                })
        
        results['finished_at'] = datetime.now().isoformat()
        return results


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for batch orchestration"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Batch Orchestration')
    parser.add_argument('--process', action='store_true', help='Start batch processing')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size')
    parser.add_argument('--workers', type=int, default=4, help='Number of workers')
    parser.add_argument('--resume', action='store_true', help='Resume from checkpoint')
    parser.add_argument('--list-checkpoints', action='store_true', help='List checkpoints')
    parser.add_argument('--plan', choices=['sequential', 'by_category', 'incomplete_first'],
                       help='Create and show processing plan')
    parser.add_argument('--execute-plan', choices=['sequential', 'by_category', 'incomplete_first'],
                       help='Execute processing plan')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    from scripts.database import init_db
    if not init_db():
        print("Failed to initialize database")
        return 1
    
    if args.list_checkpoints:
        manager = CheckpointManager()
        checkpoints = manager.list_checkpoints()
        print("\nAvailable Checkpoints:")
        print("=" * 60)
        for cp in checkpoints:
            print(f"  {cp['batch_id']}: {cp['processed']}/{cp['total']} ({cp['timestamp']})")
        return 0
    
    if args.plan:
        scheduler = OrchestrationScheduler()
        plan = scheduler.create_processing_plan(args.plan)
        print(f"\nProcessing Plan ({args.plan}):")
        print("=" * 60)
        for item in plan:
            print(f"  {item['type']}: {item['name']} ({item['verse_count']} verses) [{item['priority']}]")
        return 0
    
    if args.execute_plan:
        scheduler = OrchestrationScheduler()
        plan = scheduler.create_processing_plan(args.execute_plan)
        config = BatchConfig(batch_size=args.batch_size, max_workers=args.workers)
        results = scheduler.execute_plan(plan, config)
        print(f"\nPlan Execution Complete:")
        print(f"  Completed: {results['completed']}/{results['plan_items']}")
        return 0
    
    if args.process:
        config = BatchConfig(
            batch_size=args.batch_size,
            max_workers=args.workers,
            enable_resumption=args.resume
        )
        processor = BatchProcessor(config=config)
        progress = processor.process_verses(resume=args.resume)
        print(f"\nProcessing Complete:")
        print(f"  Processed: {progress.processed}")
        print(f"  Successful: {progress.successful}")
        print(f"  Failed: {progress.failed}")
        print(f"  Status: {progress.status.value}")
        return 0
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
