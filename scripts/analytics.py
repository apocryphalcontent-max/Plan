#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Advanced Analytics System
Comprehensive analytics for content analysis, patterns, and insights
"""

import sys
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# PROCESSING ANALYTICS
# ============================================================================

class ProcessingAnalytics:
    """Analytics for processing pipeline performance"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def get_processing_velocity(self, days: int = 7) -> Dict[str, Any]:
        """Calculate processing velocity over time"""
        query = """
            SELECT 
                DATE(last_processed_at) as process_date,
                COUNT(*) as verses_processed,
                AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) as avg_processing_time
            FROM verses
            WHERE last_processed_at IS NOT NULL
            AND last_processed_at > CURRENT_DATE - INTERVAL '%s days'
            GROUP BY DATE(last_processed_at)
            ORDER BY process_date
        """
        
        results = self.db.fetch_all(query, (days,))
        
        if not results:
            return {'error': 'No processing data available'}
        
        total_processed = sum(r['verses_processed'] for r in results)
        avg_per_day = total_processed / len(results) if results else 0
        
        # Calculate trend
        if len(results) >= 2:
            first_half = sum(r['verses_processed'] for r in results[:len(results)//2])
            second_half = sum(r['verses_processed'] for r in results[len(results)//2:])
            trend = 'increasing' if second_half > first_half else 'decreasing' if second_half < first_half else 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'period_days': days,
            'total_processed': total_processed,
            'average_per_day': avg_per_day,
            'trend': trend,
            'daily_breakdown': [
                {
                    'date': str(r['process_date']),
                    'count': r['verses_processed'],
                    'avg_time_seconds': r['avg_processing_time']
                }
                for r in results
            ]
        }
    
    def get_status_distribution(self) -> Dict[str, Any]:
        """Get distribution of processing statuses"""
        query = """
            SELECT 
                status,
                COUNT(*) as count,
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage
            FROM verses
            GROUP BY status
            ORDER BY count DESC
        """
        
        results = self.db.fetch_all(query)
        
        return {
            'distribution': [
                {
                    'status': r['status'],
                    'count': r['count'],
                    'percentage': round(r['percentage'], 2)
                }
                for r in results
            ],
            'total': sum(r['count'] for r in results)
        }
    
    def get_failure_analysis(self) -> Dict[str, Any]:
        """Analyze processing failures"""
        query = """
            SELECT 
                failure_log,
                COUNT(*) as occurrences,
                array_agg(verse_reference) as affected_verses
            FROM verses
            WHERE status = 'failed' AND failure_log IS NOT NULL
            GROUP BY failure_log
            ORDER BY occurrences DESC
            LIMIT 10
        """
        
        results = self.db.fetch_all(query)
        
        return {
            'failure_types': [
                {
                    'error': r['failure_log'][:200] if r['failure_log'] else 'Unknown',
                    'occurrences': r['occurrences'],
                    'sample_verses': r['affected_verses'][:5] if r['affected_verses'] else []
                }
                for r in results
            ],
            'total_failures': sum(r['occurrences'] for r in results)
        }


# ============================================================================
# CONTENT ANALYTICS
# ============================================================================

class ContentAnalytics:
    """Analytics for generated content"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def get_book_completion_stats(self) -> Dict[str, Any]:
        """Get completion statistics by book"""
        query = """
            SELECT 
                cb.name,
                cb.category,
                cb.total_verses as expected_verses,
                COUNT(v.id) as actual_verses,
                SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined_verses,
                SUM(CASE WHEN v.sense_literal IS NOT NULL THEN 1 ELSE 0 END) as has_literal,
                SUM(CASE WHEN v.sense_allegorical IS NOT NULL THEN 1 ELSE 0 END) as has_allegorical,
                SUM(CASE WHEN v.sense_tropological IS NOT NULL THEN 1 ELSE 0 END) as has_tropological,
                SUM(CASE WHEN v.sense_anagogical IS NOT NULL THEN 1 ELSE 0 END) as has_anagogical
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.id, cb.name, cb.category, cb.total_verses, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        
        results = self.db.fetch_all(query)
        
        books = []
        for r in results:
            actual = r['actual_verses'] or 0
            refined = r['refined_verses'] or 0
            
            books.append({
                'name': r['name'],
                'category': r['category'],
                'expected_verses': r['expected_verses'],
                'actual_verses': actual,
                'refined_verses': refined,
                'completion_rate': refined / actual if actual > 0 else 0,
                'ingestion_rate': actual / r['expected_verses'] if r['expected_verses'] else 0,
                'sense_completion': {
                    'literal': (r['has_literal'] or 0) / actual if actual > 0 else 0,
                    'allegorical': (r['has_allegorical'] or 0) / actual if actual > 0 else 0,
                    'tropological': (r['has_tropological'] or 0) / actual if actual > 0 else 0,
                    'anagogical': (r['has_anagogical'] or 0) / actual if actual > 0 else 0
                }
            })
        
        return {
            'books': books,
            'total_expected': sum(b['expected_verses'] for b in books),
            'total_actual': sum(b['actual_verses'] for b in books),
            'total_refined': sum(b['refined_verses'] for b in books)
        }
    
    def get_category_analysis(self) -> Dict[str, Any]:
        """Analyze content by book category"""
        query = """
            SELECT 
                cb.category,
                COUNT(DISTINCT cb.id) as book_count,
                COUNT(v.id) as verse_count,
                AVG(v.emotional_valence) as avg_emotional,
                AVG(v.theological_weight) as avg_theological,
                AVG(v.sensory_intensity) as avg_sensory,
                AVG(LENGTH(COALESCE(v.refined_explication, ''))) as avg_content_length
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.category
            ORDER BY verse_count DESC
        """
        
        results = self.db.fetch_all(query)
        
        return {
            'categories': [
                {
                    'category': r['category'],
                    'book_count': r['book_count'],
                    'verse_count': r['verse_count'],
                    'averages': {
                        'emotional_valence': round(r['avg_emotional'] or 0, 3),
                        'theological_weight': round(r['avg_theological'] or 0, 3),
                        'sensory_intensity': round(r['avg_sensory'] or 0, 3),
                        'content_length': round(r['avg_content_length'] or 0, 1)
                    }
                }
                for r in results
            ]
        }
    
    def get_matrix_distribution(self) -> Dict[str, Any]:
        """Get distribution of nine-matrix values"""
        metrics = ['emotional_valence', 'theological_weight', 'sensory_intensity',
                   'grammatical_complexity', 'lexical_rarity']
        
        distributions = {}
        
        for metric in metrics:
            query = f"""
                SELECT 
                    ROUND({metric}::numeric, 1) as bucket,
                    COUNT(*) as count
                FROM verses
                WHERE {metric} IS NOT NULL
                GROUP BY ROUND({metric}::numeric, 1)
                ORDER BY bucket
            """
            results = self.db.fetch_all(query)
            
            distributions[metric] = {
                'buckets': [{'value': float(r['bucket']), 'count': r['count']} for r in results],
                'total': sum(r['count'] for r in results)
            }
        
        # Categorical distributions
        for field in ['narrative_function', 'breath_rhythm', 'register_baseline', 'tonal_weight']:
            query = f"""
                SELECT {field} as value, COUNT(*) as count
                FROM verses
                WHERE {field} IS NOT NULL
                GROUP BY {field}
                ORDER BY count DESC
            """
            results = self.db.fetch_all(query)
            distributions[field] = {
                'values': [{'value': r['value'], 'count': r['count']} for r in results]
            }
        
        return distributions


# ============================================================================
# MOTIF ANALYTICS
# ============================================================================

class MotifAnalytics:
    """Analytics for motif tracking and resonance"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def get_motif_status_overview(self) -> Dict[str, Any]:
        """Get overview of all motif statuses"""
        query = """
            SELECT 
                foundation_layer,
                current_status,
                COUNT(*) as count
            FROM motifs
            GROUP BY foundation_layer, current_status
            ORDER BY foundation_layer, current_status
        """
        
        results = self.db.fetch_all(query)
        
        # Organize by layer
        by_layer = defaultdict(lambda: defaultdict(int))
        for r in results:
            by_layer[r['foundation_layer']][r['current_status']] = r['count']
        
        return {
            'by_layer': dict(by_layer),
            'total_motifs': sum(r['count'] for r in results)
        }
    
    def get_activation_history(self, motif_name: str = None) -> Dict[str, Any]:
        """Get activation history for motifs"""
        query = """
            SELECT 
                m.name,
                m.foundation_layer,
                ma.page_number,
                ma.activation_type,
                ma.target_intensity,
                ma.actual_intensity,
                ma.vocabulary_used,
                ma.created_at
            FROM motif_activations ma
            JOIN motifs m ON ma.motif_id = m.id
        """
        
        params = []
        if motif_name:
            query += " WHERE m.name = %s"
            params.append(motif_name)
        
        query += " ORDER BY ma.page_number"
        
        results = self.db.fetch_all(query, tuple(params) if params else None)
        
        return {
            'activations': [
                {
                    'motif': r['name'],
                    'layer': r['foundation_layer'],
                    'page': r['page_number'],
                    'type': r['activation_type'],
                    'target_intensity': r['target_intensity'],
                    'actual_intensity': r['actual_intensity'],
                    'vocabulary': r['vocabulary_used'],
                    'timestamp': str(r['created_at'])
                }
                for r in results
            ],
            'total_activations': len(results)
        }
    
    def get_approaching_convergences(self, pages_ahead: int = 200) -> Dict[str, Any]:
        """Get motifs approaching convergence"""
        query = """
            SELECT 
                name,
                foundation_layer,
                planting_page,
                convergence_page,
                last_activation_page,
                current_status,
                convergence_page - COALESCE(last_activation_page, planting_page) as pages_remaining
            FROM motifs
            WHERE current_status IN ('reinforcing', 'approaching')
            AND convergence_page - COALESCE(last_activation_page, planting_page) <= %s
            ORDER BY pages_remaining ASC
        """
        
        results = self.db.fetch_all(query, (pages_ahead,))
        
        return {
            'approaching': [
                {
                    'name': r['name'],
                    'layer': r['foundation_layer'],
                    'convergence_page': r['convergence_page'],
                    'pages_remaining': r['pages_remaining'],
                    'status': r['current_status']
                }
                for r in results
            ],
            'count': len(results)
        }
    
    def calculate_trajectory_health(self, motif_id: int) -> Dict[str, Any]:
        """Calculate health of a motif's trajectory"""
        motif = self.db.fetch_one("SELECT * FROM motifs WHERE id = %s", (motif_id,))
        
        if not motif:
            return {'error': 'Motif not found'}
        
        # Get activations
        activations = self.db.fetch_all("""
            SELECT * FROM motif_activations 
            WHERE motif_id = %s 
            ORDER BY page_number
        """, (motif_id,))
        
        # Calculate expected vs actual positions
        planting = motif['planting_page']
        convergence = motif['convergence_page']
        distance = convergence - planting
        
        expected_positions = [
            planting,
            planting + int(distance * 0.5),
            planting + int(distance * 0.833),
            planting + int(distance * 0.9375),
            convergence
        ]
        
        actual_positions = [a['page_number'] for a in activations]
        
        # Calculate deviation
        deviations = []
        for expected in expected_positions[:len(actual_positions)]:
            closest = min(actual_positions, key=lambda x: abs(x - expected)) if actual_positions else expected
            deviations.append(abs(closest - expected))
        
        avg_deviation = sum(deviations) / len(deviations) if deviations else 0
        
        # Health score (lower deviation = better health)
        health_score = max(0, 1.0 - (avg_deviation / 100))
        
        return {
            'motif_name': motif['name'],
            'layer': motif['foundation_layer'],
            'expected_positions': expected_positions,
            'actual_positions': actual_positions,
            'activation_count': len(activations),
            'average_deviation': avg_deviation,
            'health_score': health_score,
            'status': 'healthy' if health_score >= 0.8 else 'needs_attention' if health_score >= 0.5 else 'critical'
        }


# ============================================================================
# TYPOLOGICAL ANALYTICS
# ============================================================================

class TypologicalAnalytics:
    """Analytics for typological correspondences"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def get_correspondence_network(self) -> Dict[str, Any]:
        """Get network of typological correspondences"""
        query = """
            SELECT 
                tc.*,
                v1.verse_reference as type_ref,
                v2.verse_reference as antitype_ref,
                cb1.name as type_book,
                cb2.name as antitype_book
            FROM typological_correspondences tc
            LEFT JOIN verses v1 ON tc.type_verse_id = v1.id
            LEFT JOIN verses v2 ON tc.antitype_verse_id = v2.id
            LEFT JOIN canonical_books cb1 ON v1.book_id = cb1.id
            LEFT JOIN canonical_books cb2 ON v2.book_id = cb2.id
            WHERE tc.status != 'failed'
        """
        
        results = self.db.fetch_all(query)
        
        # Build network
        nodes = set()
        edges = []
        
        for r in results:
            if r['type_ref']:
                nodes.add(r['type_ref'])
            if r['antitype_ref']:
                nodes.add(r['antitype_ref'])
            
            if r['type_ref'] and r['antitype_ref']:
                edges.append({
                    'source': r['type_ref'],
                    'target': r['antitype_ref'],
                    'type': r['correspondence_type'],
                    'distance': r['distance']
                })
        
        return {
            'nodes': list(nodes),
            'edges': edges,
            'node_count': len(nodes),
            'edge_count': len(edges)
        }
    
    def get_most_connected_verses(self, limit: int = 20) -> Dict[str, Any]:
        """Get verses with most typological connections"""
        query = """
            SELECT 
                v.verse_reference,
                cb.name as book_name,
                (
                    SELECT COUNT(*) FROM typological_correspondences 
                    WHERE type_verse_id = v.id OR antitype_verse_id = v.id
                ) as connection_count
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            ORDER BY connection_count DESC
            LIMIT %s
        """
        
        results = self.db.fetch_all(query, (limit,))
        
        return {
            'top_connected': [
                {
                    'reference': r['verse_reference'],
                    'book': r['book_name'],
                    'connections': r['connection_count']
                }
                for r in results if r['connection_count'] > 0
            ]
        }


# ============================================================================
# ANALYTICS DASHBOARD GENERATOR
# ============================================================================

class AnalyticsDashboard:
    """Generate comprehensive analytics dashboard"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.processing = ProcessingAnalytics(self.db)
        self.content = ContentAnalytics(self.db)
        self.motif = MotifAnalytics(self.db)
        self.typology = TypologicalAnalytics(self.db)
    
    def generate_full_report(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        logger.info("Generating analytics report...")
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'sections': {}
        }
        
        # Processing analytics
        report['sections']['processing'] = {
            'velocity': self.processing.get_processing_velocity(),
            'status_distribution': self.processing.get_status_distribution(),
            'failures': self.processing.get_failure_analysis()
        }
        
        # Content analytics
        report['sections']['content'] = {
            'book_completion': self.content.get_book_completion_stats(),
            'category_analysis': self.content.get_category_analysis(),
            'matrix_distribution': self.content.get_matrix_distribution()
        }
        
        # Motif analytics
        report['sections']['motifs'] = {
            'status_overview': self.motif.get_motif_status_overview(),
            'approaching_convergences': self.motif.get_approaching_convergences()
        }
        
        # Typology analytics
        report['sections']['typology'] = {
            'network': self.typology.get_correspondence_network(),
            'top_connected': self.typology.get_most_connected_verses()
        }
        
        logger.info("Analytics report generated")
        return report
    
    def export_to_json(self, output_path: Path) -> Path:
        """Export analytics to JSON file"""
        report = self.generate_full_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Analytics exported to {output_path}")
        return output_path
    
    def export_to_markdown(self, output_path: Path) -> Path:
        """Export analytics to Markdown file"""
        report = self.generate_full_report()
        
        md = f"""# ΒΊΒΛΟΣ ΛΌΓΟΥ Analytics Report

**Generated:** {report['generated_at']}

---

## Processing Analytics

### Velocity (Last 7 Days)
"""
        
        velocity = report['sections']['processing']['velocity']
        if 'error' not in velocity:
            md += f"""
- **Total Processed:** {velocity.get('total_processed', 0):,}
- **Average Per Day:** {velocity.get('average_per_day', 0):.1f}
- **Trend:** {velocity.get('trend', 'N/A')}
"""
        
        md += """
### Status Distribution

| Status | Count | Percentage |
|--------|-------|------------|
"""
        
        for item in report['sections']['processing']['status_distribution'].get('distribution', []):
            md += f"| {item['status']} | {item['count']:,} | {item['percentage']}% |\n"
        
        md += """
---

## Content Analytics

### Category Analysis

| Category | Books | Verses | Avg Emotional | Avg Theological |
|----------|-------|--------|---------------|-----------------|
"""
        
        for cat in report['sections']['content']['category_analysis'].get('categories', []):
            md += f"| {cat['category']} | {cat['book_count']} | {cat['verse_count']:,} | "
            md += f"{cat['averages']['emotional_valence']:.3f} | {cat['averages']['theological_weight']:.3f} |\n"
        
        md += """
---

## Motif Analytics

### Approaching Convergences
"""
        
        approaching = report['sections']['motifs']['approaching_convergences'].get('approaching', [])
        if approaching:
            md += "\n| Motif | Layer | Convergence Page | Pages Remaining |\n"
            md += "|-------|-------|------------------|------------------|\n"
            for m in approaching[:10]:
                md += f"| {m['name']} | {m['layer']} | {m['convergence_page']} | {m['pages_remaining']} |\n"
        else:
            md += "\nNo motifs approaching convergence within next 200 pages.\n"
        
        md += """
---

## Typological Network

"""
        network = report['sections']['typology']['network']
        md += f"- **Total Nodes (Verses):** {network.get('node_count', 0)}\n"
        md += f"- **Total Edges (Connections):** {network.get('edge_count', 0)}\n"
        
        md += """
### Most Connected Verses

| Reference | Book | Connections |
|-----------|------|-------------|
"""
        
        for v in report['sections']['typology']['top_connected'].get('top_connected', [])[:10]:
            md += f"| {v['reference']} | {v['book']} | {v['connections']} |\n"
        
        md += "\n---\n\n*End of Analytics Report*\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        logger.info(f"Analytics exported to {output_path}")
        return output_path


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for analytics"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Analytics System')
    parser.add_argument('--report', action='store_true', help='Generate full report')
    parser.add_argument('--format', choices=['json', 'markdown', 'both'], default='markdown')
    parser.add_argument('--output', type=Path, help='Output directory')
    parser.add_argument('--processing', action='store_true', help='Show processing analytics')
    parser.add_argument('--motifs', action='store_true', help='Show motif analytics')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    from scripts.database import init_db
    from config.settings import OUTPUT_DIR
    
    if not init_db():
        print("Failed to initialize database")
        return 1
    
    dashboard = AnalyticsDashboard()
    output_dir = args.output or OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.report:
        if args.format in ['json', 'both']:
            dashboard.export_to_json(output_dir / 'analytics_report.json')
        if args.format in ['markdown', 'both']:
            dashboard.export_to_markdown(output_dir / 'Analytics_Report.md')
        print(f"Reports exported to {output_dir}")
    
    elif args.processing:
        analytics = ProcessingAnalytics()
        velocity = analytics.get_processing_velocity()
        print("\nProcessing Velocity:")
        print(json.dumps(velocity, indent=2, default=str))
    
    elif args.motifs:
        analytics = MotifAnalytics()
        overview = analytics.get_motif_status_overview()
        print("\nMotif Status Overview:")
        print(json.dumps(overview, indent=2))
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
