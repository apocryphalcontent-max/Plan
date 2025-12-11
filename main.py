#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Main Entry Point
Central command-line interface for all system operations

A comprehensive Orthodox Exegetical Commentary System implementing:
- Fourfold Sense Analysis (Literal 30%, Allegorical 25%, Tropological 25%, Anagogical 20%)
- Stratified Foundation System (Seven Layers)
- Nine-Matrix Verse Processing
- Orbital Resonance Motif Tracking
- Thread Density Management (18-22 target bounds)
- Patristic Integration
- Typological Network Building
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from enum import IntEnum

__version__ = "2.2.0"


class ExitCode(IntEnum):
    """Standardized exit codes for CLI operations."""
    SUCCESS = 0
    GENERAL_ERROR = 1
    DATABASE_ERROR = 2
    VALIDATION_ERROR = 3
    IO_ERROR = 4
    CONFIGURATION_ERROR = 5

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import config, BASE_DIR, OUTPUT_DIR, LOGS_DIR
from scripts.database import init_db, close_db, get_db

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure logging with console and file handlers.

    Args:
        verbose: If True, set log level to DEBUG; otherwise INFO.

    Returns:
        The root logger instance.
    """
    level = logging.DEBUG if verbose else logging.INFO

    # Create log file path with date
    log_file = LOGS_DIR / f"biblos_logou_{datetime.now().strftime('%Y%m%d')}.log"

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler with colored output hints
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)

    # File handler with full details
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)

    return root_logger


def cmd_init(args: argparse.Namespace) -> int:
    """
    Initialize the database with schema and motifs.

    Args:
        args: Parsed command-line arguments containing schema path and flags.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.ingestion import IngestionOrchestrator

    db = get_db()
    orchestrator = IngestionOrchestrator(db)

    # Run schema if provided or use default
    schema_path = args.schema or (BASE_DIR / 'bible_refinement_db.sql')
    if schema_path.exists():
        print(f"Running schema from {schema_path}...")
        if orchestrator.run_schema(schema_path):
            print("✓ Schema executed successfully")
        else:
            print("✗ Schema execution failed")
            return ExitCode.DATABASE_ERROR
    else:
        print(f"✗ Schema file not found: {schema_path}")
        return ExitCode.IO_ERROR

    # Initialize motifs
    if args.motifs or args.all:
        print("Initializing motifs...")
        stats = orchestrator.initialize_system()
        print(f"✓ Initialized {stats.get('motifs', 0)} motifs")

    return ExitCode.SUCCESS


def cmd_ingest(args: argparse.Namespace) -> int:
    """
    Ingest data into the database from files.

    Args:
        args: Parsed command-line arguments containing file paths.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.ingestion import IngestionOrchestrator

    db = get_db()
    orchestrator = IngestionOrchestrator(db)

    if args.verses:
        verse_path = Path(args.verses)
        if not verse_path.exists():
            print(f"✗ Verse file not found: {verse_path}")
            return ExitCode.IO_ERROR
        print(f"Ingesting verses from {verse_path}...")
        count = orchestrator.ingest_verses_from_file(verse_path)
        print(f"✓ Ingested {count:,} verses")
    else:
        print("No input file specified. Use --verses <path>")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def cmd_process(args: argparse.Namespace) -> int:
    """
    Process verses through the refinement pipeline.

    Args:
        args: Parsed command-line arguments for processing options.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.processing import VerseProcessor

    db = get_db()
    processor = VerseProcessor(db)

    if args.verse_id:
        print(f"Processing verse ID {args.verse_id}...")
        success = processor.process_verse(args.verse_id)
        if success:
            print("✓ Successfully processed verse")
            return ExitCode.SUCCESS
        else:
            print("✗ Failed to process verse")
            return ExitCode.GENERAL_ERROR
    elif args.continuous:
        print("Starting continuous processing (Ctrl+C to stop)...")
        try:
            processor.run_continuous()
        except KeyboardInterrupt:
            print("\n✓ Processing stopped by user")
    else:
        print(f"Processing batch of {args.batch} verses...")
        stats = processor.process_batch(args.batch)
        print(f"✓ Processed: {stats['processed']:,} | Success: {stats['success']:,} | Failed: {stats['failed']:,}")
        if stats['failed'] > 0:
            return ExitCode.GENERAL_ERROR

    return ExitCode.SUCCESS


def cmd_export(args: argparse.Namespace) -> int:
    """
    Export data to various formats (Markdown, JSON).

    Args:
        args: Parsed command-line arguments for export options.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.output_generator import OutputOrchestrator

    db = get_db()
    orchestrator = OutputOrchestrator(db)

    formats = ['markdown', 'json'] if args.format == 'both' else [args.format]

    if args.book:
        print(f"Exporting {args.book}...")
        results = orchestrator.export_book(args.book, formats)
        if not any(results.values()):
            print(f"✗ No data found for book: {args.book}")
            return ExitCode.GENERAL_ERROR
        for fmt, path in results.items():
            if path:
                print(f"  ✓ {fmt}: {path}")
    elif args.dashboard:
        print("Generating dashboard...")
        path = orchestrator.markdown.export_progress_dashboard()
        print(f"✓ Dashboard: {path}")
    elif args.all:
        print("Exporting all outputs...")
        results = orchestrator.export_all(formats)
        for fmt, paths in results.items():
            for path in paths:
                if path:
                    print(f"  ✓ {fmt}: {path}")
    else:
        # Default action: generate dashboard
        print("No export option specified. Generating dashboard...")
        path = orchestrator.markdown.export_progress_dashboard()
        print(f"✓ Dashboard: {path}")

    return ExitCode.SUCCESS


def cmd_status(args: argparse.Namespace) -> int:
    """
    Show comprehensive system status including database and processing statistics.

    Args:
        args: Parsed command-line arguments (unused but required for consistency).

    Returns:
        Exit code indicating success.
    """
    from scripts.ingestion import IngestionOrchestrator
    from scripts.database import VerseRepository

    db = get_db()
    orchestrator = IngestionOrchestrator(db)
    verse_repo = VerseRepository(db)

    status = orchestrator.get_ingestion_status()
    stats = verse_repo.get_completion_stats()

    print("\n" + "=" * 55)
    print(f"  ΒΊΒΛΟΣ ΛΌΓΟΥ System Status  (v{__version__})")
    print("=" * 55)

    print("\n📊 Table Counts:")
    for table, count in status.items():
        print(f"    {table:<25} {count:>10,}")

    print("\n⚙️  Processing Status:")
    for status_name, count in stats.items():
        print(f"    {status_name:<25} {count:>10,}")

    total = sum(stats.values())
    refined = stats.get('refined', 0)
    if total > 0:
        pct = refined / total * 100
        bar_filled = int(pct / 5)
        bar_empty = 20 - bar_filled
        print(f"\n📈 Completion: [{'█' * bar_filled}{'░' * bar_empty}] {pct:.1f}%")
        print(f"    {refined:,} of {total:,} verses refined")

    print("\n" + "=" * 55 + "\n")

    return ExitCode.SUCCESS


def cmd_fetch(args: argparse.Namespace) -> int:
    """
    Fetch verse text from Bible API or offline database.

    Args:
        args: Parsed command-line arguments for fetch options.

    Returns:
        Exit code indicating success or failure.
    """
    from tools.bible_api import VerseFetcher

    db = get_db()
    fetcher = VerseFetcher(db)

    if args.populate:
        print(f"Populating missing verse text (limit: {args.limit:,})...")
        count = fetcher.populate_missing_verses(args.book, args.limit)
        print(f"✓ Updated {count:,} verses")
        stats = fetcher.get_fetch_statistics()
        print(f"  Offline hits: {stats['offline_hits']:,} | API calls: {stats['api_calls']:,}")
    elif args.verse:
        # Parse verse reference like "Genesis 1:1"
        parts = args.verse.rsplit(' ', 1)
        if len(parts) == 2:
            book = parts[0]
            ref_parts = parts[1].split(':')
            if len(ref_parts) == 2:
                try:
                    chapter = int(ref_parts[0])
                    verse_num = int(ref_parts[1])
                    text = fetcher.fetch_verse(book, chapter, verse_num)
                    if text:
                        print(f"\n{args.verse}:\n  {text}\n")
                        return ExitCode.SUCCESS
                    else:
                        print(f"✗ Verse not found: {args.verse}")
                        return ExitCode.GENERAL_ERROR
                except ValueError:
                    pass
        print(f"✗ Invalid verse reference format: {args.verse}")
        print("  Expected format: \"Book Chapter:Verse\" (e.g., \"Genesis 1:1\")")
        return ExitCode.VALIDATION_ERROR
    else:
        print("No fetch option specified. Use --verse or --populate")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def cmd_validate(args: argparse.Namespace) -> int:
    """
    Run validation checks on processed data.

    Args:
        args: Parsed command-line arguments for validation options.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.validation import ValidationOrchestrator

    db = get_db()
    orchestrator = ValidationOrchestrator(db)

    if args.full:
        print(f"Running full validation suite (sample size: {args.sample_size})...")
        results = orchestrator.run_full_validation(args.sample_size)

        print("\n" + "=" * 60)
        print("  VALIDATION RESULTS")
        print("=" * 60)

        for check_name, check_data in results['checks'].items():
            print(f"\n  {check_name.upper()}:")
            for key, value in check_data.items():
                if isinstance(value, float):
                    print(f"    {key}: {value:.3f}")
                else:
                    print(f"    {key}: {value}")

        overall_status = results['overall']['status']
        status_icon = '✓' if overall_status == 'PASS' else '✗'
        print(f"\n  {status_icon} OVERALL STATUS: {overall_status}")
        print("=" * 60)

        return ExitCode.SUCCESS if overall_status == 'PASS' else ExitCode.VALIDATION_ERROR

    elif args.verse_id:
        result = orchestrator.invisibility.verify_verse(args.verse_id)
        passes = result.get('passes', False)
        status = 'PASS' if passes else 'FAIL'
        print(f"\nVerse {args.verse_id}: {status}")

        if result.get('checks'):
            for field, check in result['checks'].items():
                icon = '✓' if check['passes'] else '✗'
                print(f"  {icon} {field}: score={check['score']:.2f}")

        return ExitCode.SUCCESS if passes else ExitCode.VALIDATION_ERROR

    elif args.density_page:
        recommendations = orchestrator.density.get_density_recommendations(args.density_page)
        print(f"\n📊 Thread Density at page {args.density_page}:")
        for rec in recommendations:
            print(f"  • {rec}")
    else:
        print("No validation option specified. Use --full, --verse-id, or --density-page")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def cmd_analytics(args: argparse.Namespace) -> int:
    """
    Generate analytics reports and processing statistics.

    Args:
        args: Parsed command-line arguments for analytics options.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.analytics import AnalyticsDashboard

    db = get_db()
    dashboard = AnalyticsDashboard(db)

    if args.report:
        print("Generating analytics report...")

        if args.format in ['json', 'both']:
            path = dashboard.export_to_json(OUTPUT_DIR / 'analytics_report.json')
            print(f"  ✓ JSON: {path}")

        if args.format in ['markdown', 'both']:
            path = dashboard.export_to_markdown(OUTPUT_DIR / 'Analytics_Report.md')
            print(f"  ✓ Markdown: {path}")

    elif args.processing:
        from scripts.analytics import ProcessingAnalytics
        analytics = ProcessingAnalytics(db)

        velocity = analytics.get_processing_velocity()
        print("\n📈 Processing Velocity (Last 7 Days):")
        print(f"    Total Processed: {velocity.get('total_processed', 0):,}")
        print(f"    Average/Day:     {velocity.get('average_per_day', 0):.1f}")
        trend = velocity.get('trend', 'N/A')
        trend_icon = '↑' if trend == 'increasing' else ('↓' if trend == 'decreasing' else '→')
        print(f"    Trend:           {trend_icon} {trend}")

    elif args.motifs:
        from scripts.analytics import MotifAnalytics
        analytics = MotifAnalytics(db)

        overview = analytics.get_motif_status_overview()
        print("\n🎯 Motif Status Overview:")
        for layer, statuses in overview.get('by_layer', {}).items():
            print(f"    {layer}:")
            for status, count in statuses.items():
                print(f"      {status}: {count}")

        approaching = analytics.get_approaching_convergences()
        if approaching['approaching']:
            print("\n⏳ Approaching Convergences:")
            for m in approaching['approaching'][:5]:
                print(f"    • {m['name']}: {m['pages_remaining']} pages remaining")
    else:
        print("No analytics option specified. Use --report, --processing, or --motifs")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def cmd_orchestrate(args: argparse.Namespace) -> int:
    """
    Batch orchestration operations for large-scale processing.

    Args:
        args: Parsed command-line arguments for orchestration options.

    Returns:
        Exit code indicating success or failure.
    """
    from scripts.orchestration import BatchProcessor, OrchestrationScheduler, CheckpointManager, BatchConfig

    db = get_db()

    if args.list_checkpoints:
        manager = CheckpointManager()
        checkpoints = manager.list_checkpoints()

        print("\n📋 Available Checkpoints:")
        print("=" * 60)
        if checkpoints:
            for cp in checkpoints:
                print(f"    {cp['batch_id']}: {cp['processed']}/{cp['total']} ({cp['timestamp']})")
        else:
            print("    No checkpoints found")
        return ExitCode.SUCCESS

    if args.plan:
        scheduler = OrchestrationScheduler(db)
        plan = scheduler.create_processing_plan(args.plan)

        print(f"\n📝 Processing Plan ({args.plan}):")
        print("=" * 60)
        total_verses = 0
        for item in plan:
            print(f"    {item['type']}: {item['name']} ({item['verse_count']:,} verses) [{item['priority']}]")
            total_verses += item['verse_count']
        print(f"\n    Total: {total_verses:,} verses across {len(plan)} items")
        return ExitCode.SUCCESS

    if args.execute:
        scheduler = OrchestrationScheduler(db)
        plan = scheduler.create_processing_plan(args.execute)

        batch_config = BatchConfig(
            batch_size=args.batch_size,
            max_workers=args.workers
        )

        print(f"⚙️ Executing plan: {args.execute}")
        results = scheduler.execute_plan(plan, batch_config)

        print(f"\n✓ Plan Execution Complete:")
        print(f"    Completed: {results['completed']}/{results['plan_items']}")
        print(f"    Failed:    {results['failed']}")
        return ExitCode.SUCCESS if results['failed'] == 0 else ExitCode.GENERAL_ERROR

    if args.run:
        batch_config = BatchConfig(
            batch_size=args.batch_size,
            max_workers=args.workers,
            enable_resumption=True
        )
        processor = BatchProcessor(db, batch_config)

        print(f"⚙️ Starting batch processing (batch_size={args.batch_size}, workers={args.workers})...")
        try:
            progress = processor.process_verses(resume=True)

            print(f"\n✓ Processing Complete:")
            print(f"    Processed:  {progress.processed:,}")
            print(f"    Successful: {progress.successful:,}")
            print(f"    Failed:     {progress.failed:,}")
            print(f"    Status:     {progress.status.value}")
            return ExitCode.SUCCESS if progress.failed == 0 else ExitCode.GENERAL_ERROR
        except KeyboardInterrupt:
            print("\n✓ Processing stopped by user")
            return ExitCode.SUCCESS

    print("No orchestration option specified. Use --run, --plan, --execute, or --list-checkpoints")
    return ExitCode.CONFIGURATION_ERROR


def cmd_patristic(args: argparse.Namespace) -> int:
    """
    Patristic integration operations for Church Fathers commentary.

    Args:
        args: Parsed command-line arguments for patristic options.

    Returns:
        Exit code indicating success or failure.
    """
    from tools.patristic_integration import PatristicSourceManager, CatenaGenerator

    db = get_db()
    manager = PatristicSourceManager(db)

    if args.list_fathers:
        fathers = manager.get_all_fathers()
        print("\n📜 Church Fathers by Era:")
        print("=" * 60)
        for era, father_list in fathers.items():
            print(f"\n  {era.upper().replace('_', ' ')}:")
            for f in father_list:
                print(f"    • {f['name']} ({f['dates']}) - {f['tradition']}")

    elif args.father:
        info = manager.get_father_info(args.father)
        if info:
            print(f"\n📖 {info['name']}")
            print("=" * 40)
            print(f"    Dates:     {info['dates']}")
            print(f"    Tradition: {info['tradition']}")
            print(f"    Era:       {info['era']}")
            print(f"    Emphases:  {', '.join(info.get('emphases', []))}")
        else:
            print(f"✗ Father not found: {args.father}")
            return ExitCode.GENERAL_ERROR

    elif args.verse:
        commentaries = manager.get_commentary_for_verse(args.verse)
        print(f"\n📜 Patristic commentary for {args.verse}:")
        if commentaries:
            for c in commentaries:
                print(f"\n    {c.get('father_name', 'Unknown')}:")
                text = c.get('condensed_summary', c.get('original_text', ''))
                print(f"      {text[:200]}...")
        else:
            print("    No commentary found")

    elif args.catena:
        generator = CatenaGenerator(db)
        catena = generator.generate_catena(args.catena)
        print(f"\n📚 Catena for {args.catena}:")
        print("=" * 60)
        if catena['entries']:
            for entry in catena['entries']:
                print(f"\n    {entry['father']} ({entry['work']}):")
                print(f"      {entry['text'][:250]}...")
        else:
            print("    No catena entries found")
    else:
        print("No patristic option specified. Use --list-fathers, --father, --verse, or --catena")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def cmd_crossref(args: argparse.Namespace) -> int:
    """
    Cross-reference and typological network operations.

    Args:
        args: Parsed command-line arguments for cross-reference options.

    Returns:
        Exit code indicating success or failure.
    """
    from tools.cross_references import CrossReferenceAnalyzer, TypologicalNetworkBuilder, ReferenceSuggester

    db = get_db()

    if args.init_typology:
        builder = TypologicalNetworkBuilder(db)
        count = builder.initialize_core_typologies()
        print(f"✓ Initialized {count} typological correspondences")

    elif args.analyze:
        analyzer = CrossReferenceAnalyzer(db)
        refs = analyzer.find_references_for_verse(args.analyze)

        print(f"\n🔗 References for {args.analyze}:")
        outgoing = refs.get('outgoing', [])
        incoming = refs.get('incoming', [])
        print(f"    Outgoing ({len(outgoing)}):")
        for r in outgoing[:5]:
            print(f"      → {r['target']} ({r['relationship_type']})")
        if len(outgoing) > 5:
            print(f"      ... and {len(outgoing) - 5} more")
        print(f"    Incoming ({len(incoming)}):")
        for r in incoming[:5]:
            print(f"      ← {r['source']} ({r['relationship_type']})")
        if len(incoming) > 5:
            print(f"      ... and {len(incoming) - 5} more")

    elif args.suggest:
        suggester = ReferenceSuggester(db)
        suggestions = suggester.suggest_for_verse(args.suggest)

        print(f"\n💡 Suggestions for {args.suggest}:")
        print(f"    Existing references: {len(suggestions['existing_references'])}")
        if suggestions['suggested_additions']:
            print("    Suggested additions:")
            for s in suggestions['suggested_additions'][:5]:
                print(f"      • {s['reference']} ({s['reason']})")
        if suggestions['typological_opportunities']:
            print("    Typological opportunities:")
            for t in suggestions['typological_opportunities'][:5]:
                print(f"      • {t['reference']} (confidence: {t['confidence']:.2f})")

    elif args.stats:
        builder = TypologicalNetworkBuilder(db)
        stats = builder.get_network_statistics()

        print("\n📊 Typological Network Statistics:")
        print(f"    Total Correspondences: {stats['total_correspondences']:,}")
        print(f"    Average Distance:      {stats['average_distance']}")
        print("    By Type:")
        for t, c in stats.get('by_type', {}).items():
            print(f"      {t}: {c}")
    else:
        print("No crossref option specified. Use --init-typology, --analyze, --suggest, or --stats")
        return ExitCode.CONFIGURATION_ERROR

    return ExitCode.SUCCESS


def main() -> int:
    """
    Main entry point for the ΒΊΒΛΟΣ ΛΌΓΟΥ CLI.

    Returns:
        Exit code indicating success or failure.
    """
    parser = argparse.ArgumentParser(
        prog='biblos-logou',
        description='ΒΊΒΛΟΣ ΛΌΓΟΥ - Orthodox Exegetical Commentary System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py init --schema bible_refinement_db.sql --all
  python main.py ingest --verses data/verses.txt
  python main.py process --batch 100
  python main.py export --dashboard
  python main.py status
  python main.py validate --full
  python main.py analytics --report
  python main.py orchestrate --plan sequential
  python main.py patristic --list-fathers
  python main.py crossref --stats

For more information, see the README.md file.
        """
    )

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize database')
    init_parser.add_argument('--schema', type=Path, help='Path to SQL schema file')
    init_parser.add_argument('--motifs', action='store_true', help='Initialize motifs')
    init_parser.add_argument('--all', action='store_true', help='Initialize everything')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest data')
    ingest_parser.add_argument('--verses', type=str, help='Path to verses file')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process verses')
    process_parser.add_argument('--batch', type=int, default=100, help='Batch size')
    process_parser.add_argument('--continuous', action='store_true', help='Run continuously')
    process_parser.add_argument('--verse-id', type=int, help='Process specific verse')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--book', type=str, help='Export specific book')
    export_parser.add_argument('--dashboard', action='store_true', help='Generate dashboard')
    export_parser.add_argument('--all', action='store_true', help='Export all')
    export_parser.add_argument('--format', choices=['markdown', 'json', 'both'], 
                              default='markdown', help='Output format')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch verse text from API')
    fetch_parser.add_argument('--verse', type=str, help='Fetch specific verse (e.g., "Genesis 1:1")')
    fetch_parser.add_argument('--populate', action='store_true', help='Populate missing verses')
    fetch_parser.add_argument('--book', type=str, help='Limit to specific book')
    fetch_parser.add_argument('--limit', type=int, default=100, help='Limit number of verses')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run validation checks')
    validate_parser.add_argument('--full', action='store_true', help='Run full validation suite')
    validate_parser.add_argument('--sample-size', type=int, default=100, help='Sample size for validation')
    validate_parser.add_argument('--verse-id', type=int, help='Validate specific verse')
    validate_parser.add_argument('--density-page', type=int, help='Check density at page')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Generate analytics')
    analytics_parser.add_argument('--report', action='store_true', help='Generate full report')
    analytics_parser.add_argument('--format', choices=['markdown', 'json', 'both'], default='markdown')
    analytics_parser.add_argument('--processing', action='store_true', help='Show processing analytics')
    analytics_parser.add_argument('--motifs', action='store_true', help='Show motif analytics')
    
    # Orchestrate command
    orch_parser = subparsers.add_parser('orchestrate', help='Batch orchestration')
    orch_parser.add_argument('--run', action='store_true', help='Run batch processing')
    orch_parser.add_argument('--plan', choices=['sequential', 'by_category', 'incomplete_first'],
                            help='Show processing plan')
    orch_parser.add_argument('--execute', choices=['sequential', 'by_category', 'incomplete_first'],
                            help='Execute processing plan')
    orch_parser.add_argument('--list-checkpoints', action='store_true', help='List checkpoints')
    orch_parser.add_argument('--batch-size', type=int, default=100, help='Batch size')
    orch_parser.add_argument('--workers', type=int, default=4, help='Number of workers')
    
    # Patristic command
    patristic_parser = subparsers.add_parser('patristic', help='Patristic integration')
    patristic_parser.add_argument('--list-fathers', action='store_true', help='List Church Fathers')
    patristic_parser.add_argument('--father', type=str, help='Get info about Father')
    patristic_parser.add_argument('--verse', type=str, help='Get commentary for verse')
    patristic_parser.add_argument('--catena', type=str, help='Generate catena for verse')
    
    # Cross-reference command
    xref_parser = subparsers.add_parser('crossref', help='Cross-reference operations')
    xref_parser.add_argument('--init-typology', action='store_true', help='Initialize typological pairs')
    xref_parser.add_argument('--analyze', type=str, help='Analyze references for verse')
    xref_parser.add_argument('--suggest', type=str, help='Suggest references for verse')
    xref_parser.add_argument('--stats', action='store_true', help='Show network statistics')
    
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return ExitCode.SUCCESS

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Initialize database connection
    if not init_db():
        print("✗ Failed to initialize database connection")
        print("  Check your database configuration in config/settings.py or .env")
        print("  Ensure PostgreSQL is running and credentials are correct")
        return ExitCode.DATABASE_ERROR

    # Command dispatcher
    commands: Dict[str, Callable[[argparse.Namespace], int]] = {
        'init': cmd_init,
        'ingest': cmd_ingest,
        'process': cmd_process,
        'export': cmd_export,
        'status': cmd_status,
        'fetch': cmd_fetch,
        'validate': cmd_validate,
        'analytics': cmd_analytics,
        'orchestrate': cmd_orchestrate,
        'patristic': cmd_patristic,
        'crossref': cmd_crossref
    }

    try:
        return commands[args.command](args)
    except KeyboardInterrupt:
        print("\n✓ Operation cancelled by user")
        return ExitCode.SUCCESS
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n✗ Unexpected error: {e}")
        print("  Check the log file for details")
        return ExitCode.GENERAL_ERROR
    finally:
        close_db()


if __name__ == "__main__":
    sys.exit(main())
