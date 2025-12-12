#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Web Application
Flask-based web interface for the Orthodox Exegetical Commentary System

Provides:
- Dashboard with system status and progress
- Verse browsing and search
- Book commentary viewer
- Patristic commentary access
- Motif registry viewer
- API endpoints for JSON data
"""

import sys
import html
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, render_template, jsonify, request, abort

from config.settings import config, BASE_DIR, OUTPUT_DIR
from scripts.database import init_db, close_db, get_db, DatabaseManager

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent / 'templates'),
            static_folder=str(Path(__file__).parent / 'static'))

app.config['SECRET_KEY'] = 'biblos-logou-secret-key-change-in-production'


# ============================================================================
# DATABASE HELPERS
# ============================================================================

def get_database() -> Optional[DatabaseManager]:
    """Get database connection, initializing if needed."""
    db = get_db()
    if not db.is_initialized:
        if not init_db():
            return None
    return db


def html_escape(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(str(text) if text is not None else '', quote=True)


# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('escape_html')
def escape_html_filter(text):
    """Template filter for HTML escaping."""
    return html_escape(text)


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page - Dashboard with system overview."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        # Get completion stats
        stats_query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM verses
            GROUP BY status
        """
        status_rows = db.fetch_all(stats_query)
        status_counts = {row['status']: row['count'] for row in status_rows}
        total_verses = sum(status_counts.values())
        refined = status_counts.get('refined', 0)
        completion_pct = (refined / total_verses * 100) if total_verses > 0 else 0
        
        # Get book stats
        book_query = """
            SELECT 
                cb.name,
                cb.category,
                COUNT(v.id) as total,
                SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.id, cb.name, cb.category, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        book_stats = db.fetch_all(book_query)
        
        # Get motif count
        motif_count = db.fetch_one("SELECT COUNT(*) as count FROM motifs")
        motif_total = motif_count['count'] if motif_count else 0
        
        # Get event count
        event_count = db.fetch_one("SELECT COUNT(*) as count FROM events")
        event_total = event_count['count'] if event_count else 0
        
        return render_template('index.html',
                               status_counts=status_counts,
                               total_verses=total_verses,
                               completion_pct=completion_pct,
                               book_stats=book_stats,
                               motif_total=motif_total,
                               event_total=event_total,
                               generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/books')
def books_list():
    """List all canonical books."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        query = """
            SELECT 
                cb.id, cb.name, cb.abbreviation, cb.category,
                COUNT(v.id) as verse_count,
                SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined_count
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.id, cb.name, cb.abbreviation, cb.category, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        books = db.fetch_all(query)
        
        # Group by category
        categories = {}
        for book in books:
            cat = book['category'] or 'Other'
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(book)
        
        return render_template('books.html', categories=categories)
    except Exception as e:
        logger.error(f"Error loading books: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/book/<book_name>')
def book_detail(book_name: str):
    """View a specific book's commentary."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        # Get book info
        book_query = """
            SELECT id, name, abbreviation, category
            FROM canonical_books
            WHERE name = %s
        """
        book = db.fetch_one(book_query, (book_name,))
        if not book:
            abort(404)
        
        # Get chapters
        chapters_query = """
            SELECT DISTINCT chapter
            FROM verses
            WHERE book_id = %s
            ORDER BY chapter
        """
        chapters = db.fetch_all(chapters_query, (book['id'],))
        
        return render_template('book.html', book=book, chapters=chapters)
    except Exception as e:
        logger.error(f"Error loading book {book_name}: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/book/<book_name>/chapter/<int:chapter>')
def chapter_detail(book_name: str, chapter: int):
    """View a specific chapter's verses."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        # Get book info
        book_query = """
            SELECT id, name, abbreviation, category
            FROM canonical_books
            WHERE name = %s
        """
        book = db.fetch_one(book_query, (book_name,))
        if not book:
            abort(404)
        
        # Get verses for this chapter
        verses_query = """
            SELECT *
            FROM verses
            WHERE book_id = %s AND chapter = %s
            ORDER BY verse_number
        """
        verses = db.fetch_all(verses_query, (book['id'], chapter))
        
        # Get chapter list for navigation
        chapters_query = """
            SELECT DISTINCT chapter
            FROM verses
            WHERE book_id = %s
            ORDER BY chapter
        """
        chapters = db.fetch_all(chapters_query, (book['id'],))
        
        return render_template('chapter.html', 
                               book=book, 
                               chapter=chapter, 
                               verses=verses,
                               chapters=chapters)
    except Exception as e:
        logger.error(f"Error loading chapter {book_name} {chapter}: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/verse/<int:verse_id>')
def verse_detail(verse_id: int):
    """View a specific verse's complete analysis."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        verse_query = """
            SELECT v.*, cb.name as book_name, cb.category
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.id = %s
        """
        verse = db.fetch_one(verse_query, (verse_id,))
        if not verse:
            abort(404)
        
        return render_template('verse.html', verse=verse)
    except Exception as e:
        logger.error(f"Error loading verse {verse_id}: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/motifs')
def motifs_list():
    """View the motif registry."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        query = "SELECT * FROM motifs ORDER BY foundation_layer, name"
        motifs = db.fetch_all(query)
        
        # Group by layer
        layers = {}
        layer_names = {
            'layer_one': 'Surface Adjacency (0-50 pages)',
            'layer_two': 'Near Foundation (50-200 pages)',
            'layer_three': 'Mid-Foundation (200-500 pages)',
            'layer_four': 'Deep Foundation (500-1200 pages)',
            'layer_five': 'Bedrock Foundation (1200-2500 pages)',
            'layer_six': 'Structural Undercurrent (continuous)',
            'layer_seven': 'Theological Bedrock (eternal)'
        }
        
        for motif in motifs:
            layer = motif.get('foundation_layer', 'unknown')
            if layer not in layers:
                layers[layer] = {'name': layer_names.get(layer, layer), 'motifs': []}
            layers[layer]['motifs'].append(motif)
        
        return render_template('motifs.html', layers=layers)
    except Exception as e:
        logger.error(f"Error loading motifs: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/patristic')
def patristic_list():
    """View Church Fathers and patristic commentary."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        # Import patristic data
        from tools.patristic_integration import CHURCH_FATHERS
        from data.patristic_data import CHURCH_FATHERS_META
        
        return render_template('patristic.html', 
                               fathers=CHURCH_FATHERS,
                               fathers_meta=CHURCH_FATHERS_META)
    except Exception as e:
        logger.error(f"Error loading patristic data: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/events')
def events_list():
    """View hermeneutical events."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    try:
        query = """
            SELECT e.*, v.verse_reference, v.text_kjv
            FROM events e
            LEFT JOIN verses v ON e.primary_verse_id = v.id
            ORDER BY e.part_number, e.event_number
        """
        events = db.fetch_all(query)
        
        # Group by part
        parts = {}
        for event in events:
            part = event.get('part_number', 0)
            if part not in parts:
                parts[part] = {'title': event.get('part_title', f'Part {part}'), 'events': []}
            parts[part]['events'].append(event)
        
        return render_template('events.html', parts=parts)
    except Exception as e:
        logger.error(f"Error loading events: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/search')
def search():
    """Search verses by text or reference."""
    db = get_database()
    if not db:
        return render_template('error.html', error="Database connection failed"), 500
    
    query_text = request.args.get('q', '').strip()
    if not query_text:
        return render_template('search.html', results=[], query='')
    
    try:
        # Search in verse text and reference
        search_query = """
            SELECT v.*, cb.name as book_name
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.verse_reference ILIKE %s 
               OR v.text_kjv ILIKE %s
            ORDER BY cb.canonical_order, v.chapter, v.verse_number
            LIMIT 100
        """
        search_pattern = f'%{query_text}%'
        results = db.fetch_all(search_query, (search_pattern, search_pattern))
        
        return render_template('search.html', results=results, query=query_text)
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return render_template('error.html', error=str(e)), 500


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/status')
def api_status():
    """API endpoint for system status."""
    db = get_database()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        stats_query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM verses
            GROUP BY status
        """
        status_rows = db.fetch_all(stats_query)
        status_counts = {row['status']: row['count'] for row in status_rows}
        total = sum(status_counts.values())
        
        return jsonify({
            'total_verses': total,
            'status_breakdown': status_counts,
            'completion_percentage': (status_counts.get('refined', 0) / total * 100) if total > 0 else 0,
            'generated_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/books')
def api_books():
    """API endpoint for book list."""
    db = get_database()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        query = """
            SELECT 
                cb.id, cb.name, cb.abbreviation, cb.category,
                COUNT(v.id) as verse_count
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.id, cb.name, cb.abbreviation, cb.category, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        books = db.fetch_all(query)
        return jsonify({'books': books})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/book/<book_name>')
def api_book(book_name: str):
    """API endpoint for book data."""
    db = get_database()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        # Get book info
        book_query = """
            SELECT id, name, abbreviation, category
            FROM canonical_books
            WHERE name = %s
        """
        book = db.fetch_one(book_query, (book_name,))
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Get verses
        verses_query = """
            SELECT *
            FROM verses
            WHERE book_id = %s
            ORDER BY chapter, verse_number
        """
        verses = db.fetch_all(verses_query, (book['id'],))
        
        return jsonify({
            'book': book,
            'verses': verses,
            'total_verses': len(verses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verse/<int:verse_id>')
def api_verse(verse_id: int):
    """API endpoint for verse data."""
    db = get_database()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        verse_query = """
            SELECT v.*, cb.name as book_name, cb.category
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.id = %s
        """
        verse = db.fetch_one(verse_query, (verse_id,))
        if not verse:
            return jsonify({'error': 'Verse not found'}), 404
        
        return jsonify({'verse': verse})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/motifs')
def api_motifs():
    """API endpoint for motif data."""
    db = get_database()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        query = "SELECT * FROM motifs ORDER BY foundation_layer, name"
        motifs = db.fetch_all(query)
        return jsonify({'motifs': motifs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error='Internal server error'), 500


# ============================================================================
# APPLICATION RUNNER
# ============================================================================

def run_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    """Run the web server."""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting ΒΊΒΛΟΣ ΛΌΓΟΥ Web Server on {host}:{port}")
    
    # Initialize database
    if not init_db():
        logger.warning("Database connection failed - some features may be unavailable")
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Web Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    run_server(host=args.host, port=args.port, debug=args.debug)
