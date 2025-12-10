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
from typing import Optional
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import config, BASE_DIR, OUTPUT_DIR, LOGS_DIR
from scripts.database import init_db, close_db, get_db

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(verbose: bool = False):
    """Configure logging"""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create log file path with date
    log_file = LOGS_DIR / f"biblos_logou_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )


def cmd_init(args):
    """Initialize the database"""
    from scripts.ingestion import IngestionOrchestrator
    
    db = get_db()
    orchestrator = IngestionOrchestrator(db)
    
    # Run schema if provided
    schema_path = args.schema or (BASE_DIR / 'bible_refinement_db.sql')
    if schema_path.exists():
        print(f"Running schema from {schema_path}...")
        if orchestrator.run_schema(schema_path):
            print("Schema executed successfully")
        else:
            print("Schema execution failed")
            return 1
    
    # Initialize motifs
    if args.motifs or args.all:
        print("Initializing motifs...")
        stats = orchestrator.initialize_system()
        print(f"Initialized {stats.get('motifs', 0)} motifs")
    
    return 0


def cmd_ingest(args):
    """Ingest data into the database"""
    from scripts.ingestion import IngestionOrchestrator
    
    db = get_db()
    orchestrator = IngestionOrchestrator(db)
    
    if args.verses:
        print(f"Ingesting verses from {args.verses}...")
        count = orchestrator.ingest_verses_from_file(Path(args.verses))
        print(f"Ingested {count} verses")
    
    return 0


def cmd_process(args):
    """Process verses through the refinement pipeline"""
    from scripts.processing import VerseProcessor
    
    db = get_db()
    processor = VerseProcessor(db)
    
    if args.verse_id:
        print(f"Processing verse ID {args.verse_id}...")
        success = processor.process_verse(args.verse_id)
        print("Success" if success else "Failed")
    elif args.continuous:
        print("Starting continuous processing...")
        processor.run_continuous()
    else:
        print(f"Processing batch of {args.batch} verses...")
        stats = processor.process_batch(args.batch)
        print(f"Processed: {stats['processed']}, Success: {stats['success']}, Failed: {stats['failed']}")
    
    return 0


def cmd_export(args):
    """Export data to various formats"""
    from scripts.output_generator import OutputOrchestrator
    
    db = get_db()
    orchestrator = OutputOrchestrator(db)
    
    formats = ['markdown', 'json'] if args.format == 'both' else [args.format]
    
    if args.book:
        print(f"Exporting {args.book}...")
        results = orchestrator.export_book(args.book, formats)
        for fmt, path in results.items():
            if path:
                print(f"  {fmt}: {path}")
    elif args.dashboard:
        print("Generating dashboard...")
        path = orchestrator.markdown.export_progress_dashboard()
        print(f"Dashboard: {path}")
    elif args.all:
        print("Exporting all outputs...")
        results = orchestrator.export_all(formats)
        for fmt, paths in results.items():
            for path in paths:
                if path:
                    print(f"  {fmt}: {path}")
    
    return 0


def cmd_status(args):
    """Show system status"""
    from scripts.ingestion import IngestionOrchestrator
    
    db = get_db()
    orchestrator = IngestionOrchestrator(db)
    
    status = orchestrator.get_ingestion_status()
    
    print("\n" + "=" * 50)
    print("ΒΊΒΛΟΣ ΛΌΓΟΥ System Status")
    print("=" * 50)
    
    print("\nTable Counts:")
    for table, count in status.items():
        print(f"  {table}: {count:,}")
    
    # Get processing stats
    from scripts.database import VerseRepository
    verse_repo = VerseRepository(db)
    stats = verse_repo.get_completion_stats()
    
    print("\nProcessing Status:")
    for status_name, count in stats.items():
        print(f"  {status_name}: {count:,}")
    
    total = sum(stats.values())
    refined = stats.get('refined', 0)
    if total > 0:
        print(f"\nCompletion: {refined/total*100:.1f}%")
    
    print("=" * 50 + "\n")
    
    return 0


def cmd_fetch(args):
    """Fetch verse text from Bible API"""
    from tools.bible_api import VerseFetcher
    
    db = get_db()
    fetcher = VerseFetcher(db)
    
    if args.populate:
        print(f"Populating missing verse text (limit: {args.limit})...")
        count = fetcher.populate_missing_verses(args.book, args.limit)
        print(f"Updated {count} verses")
    elif args.verse:
        parts = args.verse.split()
        if len(parts) >= 2:
            book = ' '.join(parts[:-1])
            ref = parts[-1].split(':')
            if len(ref) == 2:
                text = fetcher.fetch_verse(book, int(ref[0]), int(ref[1]))
                if text:
                    print(f"\n{args.verse}:\n{text}\n")
                else:
                    print("Verse not found")
    
    return 0


def cmd_validate(args):
    """Run validation checks"""
    from scripts.validation import ValidationOrchestrator
    
    db = get_db()
    orchestrator = ValidationOrchestrator(db)
    
    if args.full:
        print("Running full validation suite...")
        results = orchestrator.run_full_validation(args.sample_size)
        
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)
        
        for check_name, check_data in results['checks'].items():
            print(f"\n{check_name.upper()}:")
            for key, value in check_data.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.3f}")
                else:
                    print(f"  {key}: {value}")
        
        print(f"\nOVERALL STATUS: {results['overall']['status']}")
        print("=" * 60)
    
    elif args.verse_id:
        result = orchestrator.invisibility.verify_verse(args.verse_id)
        status = 'PASS' if result.get('passes') else 'FAIL'
        print(f"\nVerse {args.verse_id}: {status}")
        
        if result.get('checks'):
            for field, check in result['checks'].items():
                icon = '✓' if check['passes'] else '✗'
                print(f"  {icon} {field}: score={check['score']:.2f}")
    
    elif args.density_page:
        recommendations = orchestrator.density.get_density_recommendations(args.density_page)
        print(f"\nThread Density at page {args.density_page}:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    return 0


def cmd_analytics(args):
    """Generate analytics reports"""
    from scripts.analytics import AnalyticsDashboard
    
    db = get_db()
    dashboard = AnalyticsDashboard(db)
    
    if args.report:
        print("Generating analytics report...")
        
        if args.format in ['json', 'both']:
            path = dashboard.export_to_json(OUTPUT_DIR / 'analytics_report.json')
            print(f"  JSON: {path}")
        
        if args.format in ['markdown', 'both']:
            path = dashboard.export_to_markdown(OUTPUT_DIR / 'Analytics_Report.md')
            print(f"  Markdown: {path}")
    
    elif args.processing:
        from scripts.analytics import ProcessingAnalytics
        analytics = ProcessingAnalytics(db)
        
        velocity = analytics.get_processing_velocity()
        print("\nProcessing Velocity (Last 7 Days):")
        print(f"  Total Processed: {velocity.get('total_processed', 0):,}")
        print(f"  Average/Day: {velocity.get('average_per_day', 0):.1f}")
        print(f"  Trend: {velocity.get('trend', 'N/A')}")
    
    elif args.motifs:
        from scripts.analytics import MotifAnalytics
        analytics = MotifAnalytics(db)
        
        overview = analytics.get_motif_status_overview()
        print("\nMotif Status Overview:")
        for layer, statuses in overview.get('by_layer', {}).items():
            print(f"  {layer}:")
            for status, count in statuses.items():
                print(f"    {status}: {count}")
        
        approaching = analytics.get_approaching_convergences()
        if approaching['approaching']:
            print("\nApproaching Convergences:")
            for m in approaching['approaching'][:5]:
                print(f"  • {m['name']}: {m['pages_remaining']} pages remaining")
    
    return 0


def cmd_orchestrate(args):
    """Batch orchestration operations"""
    from scripts.orchestration import BatchProcessor, OrchestrationScheduler, CheckpointManager, BatchConfig
    
    db = get_db()
    
    if args.list_checkpoints:
        manager = CheckpointManager()
        checkpoints = manager.list_checkpoints()
        
        print("\nAvailable Checkpoints:")
        print("=" * 60)
        if checkpoints:
            for cp in checkpoints:
                print(f"  {cp['batch_id']}: {cp['processed']}/{cp['total']} ({cp['timestamp']})")
        else:
            print("  No checkpoints found")
        return 0
    
    if args.plan:
        scheduler = OrchestrationScheduler(db)
        plan = scheduler.create_processing_plan(args.plan)
        
        print(f"\nProcessing Plan ({args.plan}):")
        print("=" * 60)
        total_verses = 0
        for item in plan:
            print(f"  {item['type']}: {item['name']} ({item['verse_count']} verses) [{item['priority']}]")
            total_verses += item['verse_count']
        print(f"\nTotal: {total_verses:,} verses across {len(plan)} items")
        return 0
    
    if args.execute:
        scheduler = OrchestrationScheduler(db)
        plan = scheduler.create_processing_plan(args.execute)
        
        batch_config = BatchConfig(
            batch_size=args.batch_size,
            max_workers=args.workers
        )
        
        print(f"Executing plan: {args.execute}")
        results = scheduler.execute_plan(plan, batch_config)
        
        print(f"\nPlan Execution Complete:")
        print(f"  Completed: {results['completed']}/{results['plan_items']}")
        print(f"  Failed: {results['failed']}")
        return 0
    
    if args.run:
        config = BatchConfig(
            batch_size=args.batch_size,
            max_workers=args.workers,
            enable_resumption=True
        )
        processor = BatchProcessor(db, config)
        
        print(f"Starting batch processing (batch_size={args.batch_size}, workers={args.workers})...")
        progress = processor.process_verses(resume=True)
        
        print(f"\nProcessing Complete:")
        print(f"  Processed: {progress.processed:,}")
        print(f"  Successful: {progress.successful:,}")
        print(f"  Failed: {progress.failed:,}")
        print(f"  Status: {progress.status.value}")
        return 0
    
    return 0


def cmd_patristic(args):
    """Patristic integration operations"""
    from tools.patristic_integration import PatristicSourceManager, CatenaGenerator
    
    db = get_db()
    manager = PatristicSourceManager(db)
    
    if args.list_fathers:
        fathers = manager.get_all_fathers()
        print("\nChurch Fathers by Era:")
        print("=" * 60)
        for era, father_list in fathers.items():
            print(f"\n{era.upper().replace('_', ' ')}:")
            for f in father_list:
                print(f"  • {f['name']} ({f['dates']}) - {f['tradition']}")
    
    elif args.father:
        info = manager.get_father_info(args.father)
        if info:
            print(f"\n{info['name']}")
            print("=" * 40)
            print(f"Dates: {info['dates']}")
            print(f"Tradition: {info['tradition']}")
            print(f"Era: {info['era']}")
            print(f"Emphases: {', '.join(info.get('emphases', []))}")
        else:
            print(f"Father not found: {args.father}")
    
    elif args.verse:
        commentaries = manager.get_commentary_for_verse(args.verse)
        print(f"\nPatristic commentary for {args.verse}:")
        if commentaries:
            for c in commentaries:
                print(f"\n  {c.get('father_name', 'Unknown')}:")
                text = c.get('condensed_summary', c.get('original_text', ''))
                print(f"    {text[:200]}...")
        else:
            print("  No commentary found")
    
    elif args.catena:
        generator = CatenaGenerator(db)
        catena = generator.generate_catena(args.catena)
        print(f"\nCatena for {args.catena}:")
        print("=" * 60)
        if catena['entries']:
            for entry in catena['entries']:
                print(f"\n{entry['father']} ({entry['work']}):")
                print(f"  {entry['text'][:250]}...")
        else:
            print("  No catena entries found")
    
    return 0


def cmd_crossref(args):
    """Cross-reference operations"""
    from tools.cross_references import CrossReferenceAnalyzer, TypologicalNetworkBuilder, ReferenceSuggester
    
    db = get_db()
    
    if args.init_typology:
        builder = TypologicalNetworkBuilder(db)
        count = builder.initialize_core_typologies()
        print(f"Initialized {count} typological correspondences")
    
    elif args.analyze:
        analyzer = CrossReferenceAnalyzer(db)
        refs = analyzer.find_references_for_verse(args.analyze)
        
        print(f"\nReferences for {args.analyze}:")
        print(f"  Outgoing ({len(refs.get('outgoing', []))}):")
        for r in refs.get('outgoing', [])[:5]:
            print(f"    → {r['target']} ({r['relationship_type']})")
        print(f"  Incoming ({len(refs.get('incoming', []))}):")
        for r in refs.get('incoming', [])[:5]:
            print(f"    ← {r['source']} ({r['relationship_type']})")
    
    elif args.suggest:
        suggester = ReferenceSuggester(db)
        suggestions = suggester.suggest_for_verse(args.suggest)
        
        print(f"\nSuggestions for {args.suggest}:")
        print(f"  Existing references: {len(suggestions['existing_references'])}")
        if suggestions['suggested_additions']:
            print("  Suggested additions:")
            for s in suggestions['suggested_additions'][:5]:
                print(f"    • {s['reference']} ({s['reason']})")
        if suggestions['typological_opportunities']:
            print("  Typological opportunities:")
            for t in suggestions['typological_opportunities'][:5]:
                print(f"    • {t['reference']} (confidence: {t['confidence']:.2f})")
    
    elif args.stats:
        builder = TypologicalNetworkBuilder(db)
        stats = builder.get_network_statistics()
        
        print("\nTypological Network Statistics:")
        print(f"  Total Correspondences: {stats['total_correspondences']}")
        print(f"  Average Distance: {stats['average_distance']}")
        print("  By Type:")
        for t, c in stats.get('by_type', {}).items():
            print(f"    {t}: {c}")
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
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
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
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
        return 0
    
    # Setup
    setup_logging(args.verbose)
    
    # Initialize database
    if not init_db():
        print("Failed to initialize database connection")
        print("Check your database configuration in config/settings.py or .env")
        return 1
    
    try:
        # Execute command
        commands = {
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
        
        return commands[args.command](args)
    finally:
        close_db()


if __name__ == "__main__":
    sys.exit(main())
