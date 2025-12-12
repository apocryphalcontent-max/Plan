#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Output Generation System
Generate formatted output in multiple formats (Markdown, JSON, HTML, LaTeX)
"""

import sys
import json
import html
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, OUTPUT_DIR
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

@dataclass
class OutputConfig:
    """Configuration for output generation"""
    output_dir: Path = OUTPUT_DIR
    include_matrix: bool = True
    include_tonal: bool = True
    include_fourfold: bool = True
    page_break_between_chapters: bool = True
    include_table_of_contents: bool = True


# ============================================================================
# BASE OUTPUT GENERATOR
# ============================================================================

class BaseOutputGenerator:
    """Base class for output generators"""
    
    def __init__(self, db: DatabaseManager = None, config: OutputConfig = None):
        self.db = db or get_db()
        self.config = config or OutputConfig()
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_book_data(self, book_name: str) -> Dict[str, Any]:
        """Get all data for a book"""
        query = """
            SELECT v.*, cb.name as book_name, cb.category, cb.abbreviation
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE cb.name = %s
            ORDER BY v.chapter, v.verse_number
        """
        verses = self.db.fetch_all(query, (book_name,))
        
        if not verses:
            return {}
        
        return {
            'book_name': book_name,
            'category': verses[0]['category'] if verses else '',
            'abbreviation': verses[0]['abbreviation'] if verses else '',
            'verses': verses,
            'total_verses': len(verses),
            'chapters': self._group_by_chapter(verses)
        }
    
    def _group_by_chapter(self, verses: List[Dict]) -> Dict[int, List[Dict]]:
        """Group verses by chapter"""
        chapters = {}
        for verse in verses:
            ch = verse['chapter']
            if ch not in chapters:
                chapters[ch] = []
            chapters[ch].append(verse)
        return chapters
    
    def get_all_events(self) -> List[Dict]:
        """Get all events in hermeneutical order"""
        query = """
            SELECT e.*, v.verse_reference, v.text_kjv
            FROM events e
            LEFT JOIN verses v ON e.primary_verse_id = v.id
            ORDER BY e.part_number, e.event_number
        """
        return self.db.fetch_all(query)
    
    def get_all_motifs(self) -> List[Dict]:
        """Get all motifs"""
        return self.db.fetch_all("SELECT * FROM motifs ORDER BY foundation_layer, name")
    
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
        status_counts = {row['status']: row['count'] for row in rows}
        
        total = sum(status_counts.values())
        refined = status_counts.get('refined', 0)
        
        return {
            'total_verses': total,
            'refined': refined,
            'completion_percentage': (refined / total * 100) if total > 0 else 0,
            'status_breakdown': status_counts
        }


# ============================================================================
# MARKDOWN GENERATOR
# ============================================================================

class MarkdownGenerator(BaseOutputGenerator):
    """Generate Markdown output"""
    
    def generate_verse_entry(self, verse: Dict) -> str:
        """Generate formatted entry for a single verse"""
        output = f"""
{'='*80}
## {verse['verse_reference']}
{'='*80}

### Text

**KJV:** {verse.get('text_kjv') or '[Text not available]'}

"""
        
        if self.config.include_fourfold:
            output += """### Fourfold Analysis

#### Literal Sense (30%)
{literal}

#### Allegorical Sense (25%)
{allegorical}

#### Tropological Sense (25%)
{tropological}

#### Anagogical Sense (20%)
{anagogical}

""".format(
                literal=verse.get('sense_literal') or '[Analysis pending]',
                allegorical=verse.get('sense_allegorical') or '[Analysis pending]',
                tropological=verse.get('sense_tropological') or '[Analysis pending]',
                anagogical=verse.get('sense_anagogical') or '[Analysis pending]'
            )
        
        if self.config.include_matrix:
            output += """### Nine Matrix Elements

| Element | Value |
|---------|-------|
| Emotional Valence | {emotional} |
| Theological Weight | {theological} |
| Narrative Function | {narrative} |
| Sensory Intensity | {sensory} |
| Grammatical Complexity | {grammatical} |
| Lexical Rarity | {lexical} |
| Breath Rhythm | {breath} |
| Register Baseline | {register} |

""".format(
                emotional=verse.get('emotional_valence', 'N/A'),
                theological=verse.get('theological_weight', 'N/A'),
                narrative=verse.get('narrative_function', 'N/A'),
                sensory=verse.get('sensory_intensity', 'N/A'),
                grammatical=verse.get('grammatical_complexity', 'N/A'),
                lexical=verse.get('lexical_rarity', 'N/A'),
                breath=verse.get('breath_rhythm', 'N/A'),
                register=verse.get('register_baseline', 'N/A')
            )
        
        if self.config.include_tonal:
            output += """### Tonal Characteristics

- **Tonal Weight:** {tonal}
- **Dread Amplification:** {dread}
- **Local Emotional Honesty:** {emotional}

""".format(
                tonal=verse.get('tonal_weight', 'neutral'),
                dread=verse.get('dread_amplification', 0.5),
                emotional=verse.get('local_emotional_honesty', 'N/A')
            )
        
        if verse.get('refined_explication'):
            output += f"""### Refined Commentary

{verse['refined_explication']}

"""
        
        output += f"""---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Status: {verse.get('status', 'unknown')}*

"""
        return output
    
    def export_book(self, book_name: str) -> Optional[Path]:
        """Export all verses for a book to a Markdown file"""
        logger.info(f"Exporting {book_name} to Markdown...")
        
        data = self.get_book_data(book_name)
        if not data:
            logger.warning(f"No data found for {book_name}")
            return None
        
        output = f"""# ΒΊΒΛΟΣ ΛΌΓΟΥ: {book_name}

## A Comprehensive Orthodox Framework for Exegesis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Verses:** {data['total_verses']}
**Category:** {data['category']}

---

"""
        
        if self.config.include_table_of_contents:
            output += "## Table of Contents\n\n"
            for chapter in sorted(data['chapters'].keys()):
                output += f"- [Chapter {chapter}](#chapter-{chapter})\n"
            output += "\n---\n\n"
        
        # Generate content by chapter
        for chapter in sorted(data['chapters'].keys()):
            if self.config.page_break_between_chapters:
                output += f"\n\\pagebreak\n\n"
            
            output += f"# Chapter {chapter}\n\n"
            
            for verse in data['chapters'][chapter]:
                output += self.generate_verse_entry(verse)
        
        # Write to file
        safe_name = book_name.replace(' ', '_').replace(':', '')
        output_file = self.config.output_dir / f"{safe_name}_Commentary.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logger.info(f"Exported {data['total_verses']} verses to {output_file}")
        return output_file
    
    def export_hermeneutical_arrangement(self) -> Path:
        """Export events in hermeneutical (tonal) order"""
        logger.info("Exporting hermeneutical arrangement...")
        
        events = self.get_all_events()
        
        output = f"""# ΒΊΒΛΟΣ ΛΌΓΟΥ: Hermeneutical Arrangement

## Biblical Events in Tonal Order

*Per Hermeneutical.txt: "Keep a constant background sense of inevitable but not yet 
arrived judgment. Events should feel like fragments drifting toward a catastrophe 
the reader intuits but cannot fully map."*

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Events:** {len(events)}

---

"""
        
        current_part = None
        for event in events:
            if event['part_number'] != current_part:
                current_part = event['part_number']
                output += f"\n# PART {current_part}: {event.get('part_title', '')}\n\n"
            
            weight_indicator = {
                'light': '☀️',
                'neutral': '◯',
                'unsettling': '⚠️',
                'heavy': '⬛',
                'transcendent': '✨'
            }.get(event.get('emotional_weight', 'neutral'), '◯')
            
            load_bearing = '🔷' if event.get('load_bearing') else ''
            
            output += f"""
### {event['event_number']}. {event['event_description']} {weight_indicator} {load_bearing}

**Emotional Weight:** {event.get('emotional_weight', 'neutral')}
**Load Bearing:** {'Yes' if event.get('load_bearing') else 'No'}
**Primary Verse:** {event.get('verse_reference') or 'Not linked'}

{event.get('refined_narrative') or '*Narrative pending refinement*'}

---
"""
        
        output_file = self.config.output_dir / "Hermeneutical_Arrangement.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logger.info(f"Exported {len(events)} events to {output_file}")
        return output_file
    
    def export_motif_registry(self) -> Path:
        """Export complete motif registry"""
        logger.info("Exporting motif registry...")
        
        motifs = self.get_all_motifs()
        
        output = f"""# ΒΊΒΛΟΣ ΛΌΓΟΥ: Master Motif Registry

## Stratified Foundation System Elements

*Per Stratified.txt: "The foundation operates through seven distinct vertical layers, 
measured by proximity to the narrative surface."*

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Motifs:** {len(motifs)}

---

"""
        
        current_layer = None
        layer_descriptions = {
            'layer_one': 'Surface Adjacency (0-50 pages)',
            'layer_two': 'Near Foundation (50-200 pages)',
            'layer_three': 'Mid-Foundation (200-500 pages)',
            'layer_four': 'Deep Foundation (500-1200 pages)',
            'layer_five': 'Bedrock Foundation (1200-2500 pages)',
            'layer_six': 'Structural Undercurrent (continuous)',
            'layer_seven': 'Theological Bedrock (eternal)'
        }
        
        for motif in motifs:
            layer = motif.get('foundation_layer')
            if layer != current_layer:
                current_layer = layer
                layer_desc = layer_descriptions.get(layer, layer)
                output += f"\n# {layer_desc}\n\n"
            
            harmonic_pages = motif.get('reinforcement_pages') or []
            
            output += f"""
## {motif['name']}

**Description:** {motif.get('description') or 'No description'}
**Status:** {motif.get('current_status', 'unknown')}
**Layer:** {motif.get('foundation_layer')}

### Activation Timeline

| Stage | Page | Intensity |
|-------|------|-----------|
| Planting | {motif.get('planting_page') or 'N/A'} | {motif.get('planting_intensity') or 'N/A'} |
| Reinforcement 1 | {harmonic_pages[0] if len(harmonic_pages) > 0 else 'N/A'} | - |
| Reinforcement 2 | {harmonic_pages[1] if len(harmonic_pages) > 1 else 'N/A'} | - |
| Reinforcement 3 | {harmonic_pages[2] if len(harmonic_pages) > 2 else 'N/A'} | - |
| Convergence | {motif.get('convergence_page') or 'N/A'} | {motif.get('convergence_intensity') or 'N/A'} |

### Vocabulary Codex

{', '.join(motif.get('core_vocabulary') or ['Not defined'])}

---
"""
        
        output_file = self.config.output_dir / "Motif_Registry.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logger.info(f"Exported {len(motifs)} motifs to {output_file}")
        return output_file
    
    def export_progress_dashboard(self) -> Path:
        """Export overall progress dashboard"""
        logger.info("Generating progress dashboard...")
        
        stats = self.get_completion_stats()
        
        # Get book completion
        query = """
            SELECT 
                cb.name,
                COUNT(*) as total,
                SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.name, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        book_stats = self.db.fetch_all(query)
        
        completion_pct = stats['completion_percentage']
        
        output = f"""# ΒΊΒΛΟΣ ΛΌΓΟΥ: Progress Dashboard

## Overall Status

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Verse Processing

| Status | Count | Percentage |
|--------|-------|------------|
"""
        
        for status, count in stats['status_breakdown'].items():
            pct = (count / stats['total_verses'] * 100) if stats['total_verses'] > 0 else 0
            output += f"| {status} | {count:,} | {pct:.1f}% |\n"
        
        output += f"| **Total** | **{stats['total_verses']:,}** | **100%** |\n"
        
        # Progress bar
        bar_filled = int(completion_pct / 2)
        bar_empty = 50 - bar_filled
        output += f"""
### Completion Progress

```
[{'█' * bar_filled}{'░' * bar_empty}] {completion_pct:.1f}%
```

---

## Book Completion

| Book | Total | Refined | Progress |
|------|-------|---------|----------|
"""
        
        for book in book_stats:
            total = book['total'] or 0
            refined = book['refined'] or 0
            pct = (refined / total * 100) if total > 0 else 0
            bar = '█' * int(pct / 10) + '░' * (10 - int(pct / 10))
            output += f"| {book['name']} | {total} | {refined} | {bar} {pct:.0f}% |\n"
        
        output += """

---

## Next Actions

1. Process remaining raw verses
2. Link events to verses
3. Activate dormant motifs as processing reaches their pages
4. Verify thread density at each 50-page interval
5. Export completed books for review

"""
        
        output_file = self.config.output_dir / "Progress_Dashboard.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logger.info(f"Exported progress dashboard to {output_file}")
        return output_file


# ============================================================================
# JSON GENERATOR
# ============================================================================

class JSONGenerator(BaseOutputGenerator):
    """Generate JSON output"""
    
    def export_book(self, book_name: str) -> Optional[Path]:
        """Export book data to JSON"""
        data = self.get_book_data(book_name)
        if not data:
            return None
        
        # Convert to serializable format
        output = {
            'book_name': data['book_name'],
            'category': data['category'],
            'total_verses': data['total_verses'],
            'generated_at': datetime.now().isoformat(),
            'chapters': {}
        }
        
        for chapter, verses in data['chapters'].items():
            output['chapters'][str(chapter)] = [
                {
                    'reference': v['verse_reference'],
                    'text': v.get('text_kjv'),
                    'senses': {
                        'literal': v.get('sense_literal'),
                        'allegorical': v.get('sense_allegorical'),
                        'tropological': v.get('sense_tropological'),
                        'anagogical': v.get('sense_anagogical')
                    },
                    'matrix': {
                        'emotional_valence': v.get('emotional_valence'),
                        'theological_weight': v.get('theological_weight'),
                        'narrative_function': v.get('narrative_function'),
                        'sensory_intensity': v.get('sensory_intensity')
                    },
                    'status': v.get('status')
                }
                for v in verses
            ]
        
        safe_name = book_name.replace(' ', '_').replace(':', '')
        output_file = self.config.output_dir / f"{safe_name}_Commentary.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {book_name} to {output_file}")
        return output_file
    
    def export_full_database(self) -> Path:
        """Export full database to JSON"""
        output = {
            'generated_at': datetime.now().isoformat(),
            'stats': self.get_completion_stats(),
            'motifs': self.get_all_motifs(),
            'events': self.get_all_events()
        }
        
        output_file = self.config.output_dir / "full_database_export.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Exported full database to {output_file}")
        return output_file


# ============================================================================
# HTML GENERATOR
# ============================================================================

class HTMLGenerator(BaseOutputGenerator):
    """Generate HTML output with embedded CSS styling"""
    
    # Embedded CSS for Orthodox-themed styling
    CSS_STYLES = """
    <style>
        :root {
            --primary-color: #8b0000;
            --secondary-color: #daa520;
            --background-color: #fdf5e6;
            --text-color: #2c1810;
            --border-color: #c9a959;
            --heading-font: 'Georgia', serif;
            --body-font: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--body-font);
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.7;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--heading-font);
            color: var(--primary-color);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        
        h1 {
            font-size: 2.5rem;
            text-align: center;
            border-bottom: 3px double var(--border-color);
        }
        
        h2 {
            font-size: 1.8rem;
        }
        
        h3 {
            font-size: 1.4rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .verse-container {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .verse-reference {
            font-size: 1.3rem;
            color: var(--primary-color);
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        .verse-text {
            font-style: italic;
            font-size: 1.1rem;
            padding: 1rem;
            background: linear-gradient(to right, var(--background-color), white);
            border-left: 4px solid var(--secondary-color);
            margin: 1rem 0;
        }
        
        .fourfold-analysis {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .sense-box {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1rem;
        }
        
        .sense-literal { border-left: 4px solid #4a90a4; }
        .sense-allegorical { border-left: 4px solid #8b4513; }
        .sense-tropological { border-left: 4px solid #228b22; }
        .sense-anagogical { border-left: 4px solid #9932cc; }
        
        .sense-title {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .sense-literal .sense-title { color: #4a90a4; }
        .sense-allegorical .sense-title { color: #8b4513; }
        .sense-tropological .sense-title { color: #228b22; }
        .sense-anagogical .sense-title { color: #9932cc; }
        
        .sense-weight {
            font-size: 0.85rem;
            color: #666;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            background: white;
        }
        
        th, td {
            padding: 0.75rem;
            text-align: left;
            border: 1px solid var(--border-color);
        }
        
        th {
            background: var(--primary-color);
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background: rgba(218, 165, 32, 0.1);
        }
        
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 24px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .progress-fill {
            background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
            height: 100%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .toc {
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        .toc h2 {
            margin-top: 0;
            border-bottom: 2px solid var(--secondary-color);
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc li {
            padding: 0.3rem 0;
        }
        
        .toc a {
            color: var(--primary-color);
            text-decoration: none;
        }
        
        .toc a:hover {
            text-decoration: underline;
            color: var(--secondary-color);
        }
        
        .event-card {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .event-weight-light { border-left: 4px solid #ffd700; }
        .event-weight-neutral { border-left: 4px solid #808080; }
        .event-weight-unsettling { border-left: 4px solid #ff8c00; }
        .event-weight-heavy { border-left: 4px solid #4a0000; }
        .event-weight-transcendent { border-left: 4px solid #9400d3; }
        
        .motif-card {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .layer-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            margin-right: 0.5rem;
        }
        
        .layer-one { background: #e3f2fd; color: #1565c0; }
        .layer-two { background: #e8f5e9; color: #2e7d32; }
        .layer-three { background: #fff3e0; color: #ef6c00; }
        .layer-four { background: #fce4ec; color: #c2185b; }
        .layer-five { background: #f3e5f5; color: #7b1fa2; }
        .layer-six { background: #e0f2f1; color: #00695c; }
        .layer-seven { background: #ede7f6; color: #512da8; }
        
        .vocabulary-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        
        .vocab-tag {
            background: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 0.25rem 0.75rem;
            font-size: 0.85rem;
        }
        
        .meta-info {
            font-size: 0.85rem;
            color: #666;
            text-align: right;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status-raw { background: #ffcdd2; color: #c62828; }
        .status-parsed { background: #fff9c4; color: #f57f17; }
        .status-analyzed { background: #c8e6c9; color: #2e7d32; }
        .status-refined { background: #bbdefb; color: #1565c0; }
        .status-verified { background: #d1c4e9; color: #512da8; }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .verse-container, .event-card, .motif-card {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            
            h1, h2 {
                page-break-after: avoid;
            }
        }
    </style>
    """
    
    def _html_escape(self, text: str) -> str:
        """Escape HTML special characters using standard library"""
        return html.escape(str(text) if text is not None else '', quote=True)
    
    def _wrap_html(self, title: str, content: str) -> str:
        """Wrap content in HTML document structure"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._html_escape(title)}</title>
    {self.CSS_STYLES}
</head>
<body>
{content}
</body>
</html>
"""
    
    def generate_verse_entry(self, verse: Dict) -> str:
        """Generate HTML entry for a single verse"""
        # Safely create status class by escaping and sanitizing
        raw_status = str(verse.get('status', 'unknown'))
        safe_status = self._html_escape(raw_status.lower().replace(' ', '-'))
        status_class = f"status-{safe_status}"
        
        fourfold_html = ""
        if self.config.include_fourfold:
            fourfold_html = f"""
            <div class="fourfold-analysis">
                <div class="sense-box sense-literal">
                    <div class="sense-title">Literal Sense <span class="sense-weight">(30%)</span></div>
                    <p>{self._html_escape(verse.get('sense_literal') or '[Analysis pending]')}</p>
                </div>
                <div class="sense-box sense-allegorical">
                    <div class="sense-title">Allegorical Sense <span class="sense-weight">(25%)</span></div>
                    <p>{self._html_escape(verse.get('sense_allegorical') or '[Analysis pending]')}</p>
                </div>
                <div class="sense-box sense-tropological">
                    <div class="sense-title">Tropological Sense <span class="sense-weight">(25%)</span></div>
                    <p>{self._html_escape(verse.get('sense_tropological') or '[Analysis pending]')}</p>
                </div>
                <div class="sense-box sense-anagogical">
                    <div class="sense-title">Anagogical Sense <span class="sense-weight">(20%)</span></div>
                    <p>{self._html_escape(verse.get('sense_anagogical') or '[Analysis pending]')}</p>
                </div>
            </div>
            """
        
        matrix_html = ""
        if self.config.include_matrix:
            matrix_html = f"""
            <h4>Nine Matrix Elements</h4>
            <table>
                <tr><th>Element</th><th>Value</th></tr>
                <tr><td>Emotional Valence</td><td>{self._html_escape(str(verse.get('emotional_valence', 'N/A')))}</td></tr>
                <tr><td>Theological Weight</td><td>{self._html_escape(str(verse.get('theological_weight', 'N/A')))}</td></tr>
                <tr><td>Narrative Function</td><td>{self._html_escape(str(verse.get('narrative_function', 'N/A')))}</td></tr>
                <tr><td>Sensory Intensity</td><td>{self._html_escape(str(verse.get('sensory_intensity', 'N/A')))}</td></tr>
                <tr><td>Grammatical Complexity</td><td>{self._html_escape(str(verse.get('grammatical_complexity', 'N/A')))}</td></tr>
                <tr><td>Lexical Rarity</td><td>{self._html_escape(str(verse.get('lexical_rarity', 'N/A')))}</td></tr>
                <tr><td>Breath Rhythm</td><td>{self._html_escape(str(verse.get('breath_rhythm', 'N/A')))}</td></tr>
                <tr><td>Register Baseline</td><td>{self._html_escape(str(verse.get('register_baseline', 'N/A')))}</td></tr>
            </table>
            """
        
        tonal_html = ""
        if self.config.include_tonal:
            tonal_html = f"""
            <h4>Tonal Characteristics</h4>
            <ul>
                <li><strong>Tonal Weight:</strong> {self._html_escape(str(verse.get('tonal_weight', 'neutral')))}</li>
                <li><strong>Dread Amplification:</strong> {self._html_escape(str(verse.get('dread_amplification', 0.5)))}</li>
                <li><strong>Local Emotional Honesty:</strong> {self._html_escape(str(verse.get('local_emotional_honesty', 'N/A')))}</li>
            </ul>
            """
        
        refined_html = ""
        if verse.get('refined_explication'):
            refined_html = f"""
            <h4>Refined Commentary</h4>
            <p>{self._html_escape(verse['refined_explication'])}</p>
            """
        
        # Escape verse ID for use in HTML id attribute
        verse_id = self._html_escape(str(verse.get('id', '')))
        
        return f"""
        <div class="verse-container" id="verse-{verse_id}">
            <div class="verse-reference">{self._html_escape(verse['verse_reference'])}</div>
            <div class="verse-text">
                <strong>KJV:</strong> {self._html_escape(verse.get('text_kjv') or '[Text not available]')}
            </div>
            
            <h4>Fourfold Analysis</h4>
            {fourfold_html}
            
            {matrix_html}
            {tonal_html}
            {refined_html}
            
            <div class="meta-info">
                <span class="status-badge {status_class}">{self._html_escape(raw_status)}</span>
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """
    
    def export_book(self, book_name: str) -> Optional[Path]:
        """Export all verses for a book to an HTML file"""
        logger.info(f"Exporting {book_name} to HTML...")
        
        data = self.get_book_data(book_name)
        if not data:
            logger.warning(f"No data found for {book_name}")
            return None
        
        # Build table of contents
        toc_html = ""
        if self.config.include_table_of_contents:
            toc_items = "".join([
                f'<li><a href="#chapter-{ch}">Chapter {ch}</a></li>'
                for ch in sorted(data['chapters'].keys())
            ])
            toc_html = f"""
            <nav class="toc">
                <h2>Table of Contents</h2>
                <ul>{toc_items}</ul>
            </nav>
            """
        
        # Build chapter content
        chapters_html = ""
        for chapter in sorted(data['chapters'].keys()):
            verses_html = "".join([
                self.generate_verse_entry(verse) 
                for verse in data['chapters'][chapter]
            ])
            chapters_html += f"""
            <section id="chapter-{chapter}">
                <h2>Chapter {chapter}</h2>
                {verses_html}
            </section>
            """
        
        content = f"""
        <header>
            <h1>ΒΊΒΛΟΣ ΛΌΓΟΥ: {self._html_escape(book_name)}</h1>
            <p style="text-align: center; font-size: 1.2rem; color: var(--primary-color);">
                A Comprehensive Orthodox Framework for Exegesis
            </p>
            <p style="text-align: center; color: #666;">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                <strong>Total Verses:</strong> {data['total_verses']} |
                <strong>Category:</strong> {self._html_escape(data['category'])}
            </p>
        </header>
        
        {toc_html}
        
        <main>
            {chapters_html}
        </main>
        """
        
        html_output = self._wrap_html(f"ΒΊΒΛΟΣ ΛΌΓΟΥ: {book_name}", content)
        
        # Write to file
        safe_name = book_name.replace(' ', '_').replace(':', '')
        output_file = self.config.output_dir / f"{safe_name}_Commentary.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        logger.info(f"Exported {data['total_verses']} verses to {output_file}")
        return output_file
    
    def export_hermeneutical_arrangement(self) -> Path:
        """Export events in hermeneutical (tonal) order as HTML"""
        logger.info("Exporting hermeneutical arrangement to HTML...")
        
        events = self.get_all_events()
        
        events_html = ""
        current_part = None
        
        for event in events:
            if event['part_number'] != current_part:
                if current_part is not None:
                    events_html += "</section>"
                current_part = event['part_number']
                events_html += f"""
                <section>
                    <h2>PART {current_part}: {self._html_escape(event.get('part_title', ''))}</h2>
                """
            
            weight = event.get('emotional_weight', 'neutral')
            weight_class = f"event-weight-{weight}"
            weight_icon = {
                'light': '☀️',
                'neutral': '◯',
                'unsettling': '⚠️',
                'heavy': '⬛',
                'transcendent': '✨'
            }.get(weight, '◯')
            
            load_bearing = '🔷 Load Bearing' if event.get('load_bearing') else ''
            
            events_html += f"""
            <div class="event-card {weight_class}">
                <h3>{event['event_number']}. {self._html_escape(event['event_description'])} {weight_icon}</h3>
                <p>
                    <strong>Emotional Weight:</strong> {self._html_escape(weight)} 
                    {f'<span style="color: var(--secondary-color);">{load_bearing}</span>' if load_bearing else ''}
                </p>
                <p><strong>Primary Verse:</strong> {self._html_escape(event.get('verse_reference') or 'Not linked')}</p>
                <p>{self._html_escape(event.get('refined_narrative') or 'Narrative pending refinement')}</p>
            </div>
            """
        
        if current_part is not None:
            events_html += "</section>"
        
        content = f"""
        <header>
            <h1>ΒΊΒΛΟΣ ΛΌΓΟΥ: Hermeneutical Arrangement</h1>
            <p style="text-align: center; font-size: 1.1rem; font-style: italic; color: var(--primary-color);">
                Biblical Events in Tonal Order
            </p>
            <blockquote style="text-align: center; margin: 2rem auto; max-width: 800px; color: #666; font-style: italic;">
                "Keep a constant background sense of inevitable but not yet arrived judgment. 
                Events should feel like fragments drifting toward a catastrophe the reader 
                intuits but cannot fully map." — Hermeneutical.txt
            </blockquote>
            <p style="text-align: center; color: #666;">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                <strong>Total Events:</strong> {len(events)}
            </p>
        </header>
        
        <main>
            {events_html}
        </main>
        """
        
        html_output = self._wrap_html("ΒΊΒΛΟΣ ΛΌΓΟΥ: Hermeneutical Arrangement", content)
        
        output_file = self.config.output_dir / "Hermeneutical_Arrangement.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        logger.info(f"Exported {len(events)} events to {output_file}")
        return output_file
    
    def export_motif_registry(self) -> Path:
        """Export complete motif registry as HTML"""
        logger.info("Exporting motif registry to HTML...")
        
        motifs = self.get_all_motifs()
        
        layer_descriptions = {
            'layer_one': 'Surface Adjacency (0-50 pages)',
            'layer_two': 'Near Foundation (50-200 pages)',
            'layer_three': 'Mid-Foundation (200-500 pages)',
            'layer_four': 'Deep Foundation (500-1200 pages)',
            'layer_five': 'Bedrock Foundation (1200-2500 pages)',
            'layer_six': 'Structural Undercurrent (continuous)',
            'layer_seven': 'Theological Bedrock (eternal)'
        }
        
        motifs_html = ""
        current_layer = None
        
        for motif in motifs:
            layer = motif.get('foundation_layer')
            if layer != current_layer:
                if current_layer is not None:
                    motifs_html += "</section>"
                current_layer = layer
                layer_desc = layer_descriptions.get(layer, layer)
                layer_class = layer.replace('_', '-') if layer else 'layer-one'
                motifs_html += f"""
                <section>
                    <h2><span class="layer-badge {layer_class}">{layer_class.replace('-', ' ').title()}</span> {self._html_escape(layer_desc)}</h2>
                """
            
            harmonic_pages = motif.get('reinforcement_pages') or []
            vocab_tags = "".join([
                f'<span class="vocab-tag">{self._html_escape(word)}</span>'
                for word in (motif.get('core_vocabulary') or ['Not defined'])
            ])
            
            motifs_html += f"""
            <div class="motif-card">
                <h3>{self._html_escape(motif['name'])}</h3>
                <p><strong>Description:</strong> {self._html_escape(motif.get('description') or 'No description')}</p>
                <p>
                    <strong>Status:</strong> <span class="status-badge">{self._html_escape(motif.get('current_status', 'unknown'))}</span>
                </p>
                
                <h4>Activation Timeline</h4>
                <table>
                    <tr><th>Stage</th><th>Page</th><th>Intensity</th></tr>
                    <tr><td>Planting</td><td>{motif.get('planting_page') or 'N/A'}</td><td>{motif.get('planting_intensity') or 'N/A'}</td></tr>
                    <tr><td>Reinforcement 1</td><td>{harmonic_pages[0] if len(harmonic_pages) > 0 else 'N/A'}</td><td>-</td></tr>
                    <tr><td>Reinforcement 2</td><td>{harmonic_pages[1] if len(harmonic_pages) > 1 else 'N/A'}</td><td>-</td></tr>
                    <tr><td>Reinforcement 3</td><td>{harmonic_pages[2] if len(harmonic_pages) > 2 else 'N/A'}</td><td>-</td></tr>
                    <tr><td>Convergence</td><td>{motif.get('convergence_page') or 'N/A'}</td><td>{motif.get('convergence_intensity') or 'N/A'}</td></tr>
                </table>
                
                <h4>Vocabulary Codex</h4>
                <div class="vocabulary-tags">
                    {vocab_tags}
                </div>
            </div>
            """
        
        if current_layer is not None:
            motifs_html += "</section>"
        
        content = f"""
        <header>
            <h1>ΒΊΒΛΟΣ ΛΌΓΟΥ: Master Motif Registry</h1>
            <p style="text-align: center; font-size: 1.1rem; font-style: italic; color: var(--primary-color);">
                Stratified Foundation System Elements
            </p>
            <blockquote style="text-align: center; margin: 2rem auto; max-width: 800px; color: #666; font-style: italic;">
                "The foundation operates through seven distinct vertical layers, 
                measured by proximity to the narrative surface." — Stratified.txt
            </blockquote>
            <p style="text-align: center; color: #666;">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                <strong>Total Motifs:</strong> {len(motifs)}
            </p>
        </header>
        
        <main>
            {motifs_html}
        </main>
        """
        
        html_output = self._wrap_html("ΒΊΒΛΟΣ ΛΌΓΟΥ: Master Motif Registry", content)
        
        output_file = self.config.output_dir / "Motif_Registry.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        logger.info(f"Exported {len(motifs)} motifs to {output_file}")
        return output_file
    
    def export_progress_dashboard(self) -> Path:
        """Export overall progress dashboard as HTML"""
        logger.info("Generating HTML progress dashboard...")
        
        stats = self.get_completion_stats()
        
        # Get book completion
        query = """
            SELECT 
                cb.name,
                COUNT(*) as total,
                SUM(CASE WHEN v.status = 'refined' THEN 1 ELSE 0 END) as refined
            FROM canonical_books cb
            LEFT JOIN verses v ON cb.id = v.book_id
            GROUP BY cb.name, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        book_stats = self.db.fetch_all(query)
        
        completion_pct = stats['completion_percentage']
        
        # Status breakdown table
        status_rows = "".join([
            f'<tr><td>{self._html_escape(status)}</td><td>{count:,}</td><td>{(count / stats["total_verses"] * 100) if stats["total_verses"] > 0 else 0:.1f}%</td></tr>'
            for status, count in stats['status_breakdown'].items()
        ])
        
        # Book progress rows
        book_rows = ""
        for book in book_stats:
            total = book['total'] or 0
            refined = book['refined'] or 0
            pct = (refined / total * 100) if total > 0 else 0
            book_rows += f"""
            <tr>
                <td>{self._html_escape(book['name'])}</td>
                <td>{total}</td>
                <td>{refined}</td>
                <td>
                    <div class="progress-bar" style="height: 16px;">
                        <div class="progress-fill" style="width: {pct}%;">{pct:.0f}%</div>
                    </div>
                </td>
            </tr>
            """
        
        content = f"""
        <header>
            <h1>ΒΊΒΛΟΣ ΛΌΓΟΥ: Progress Dashboard</h1>
            <p style="text-align: center; color: #666;">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </header>
        
        <main>
            <section>
                <h2>Verse Processing Status</h2>
                <table>
                    <tr><th>Status</th><th>Count</th><th>Percentage</th></tr>
                    {status_rows}
                    <tr style="font-weight: bold; background: var(--background-color);">
                        <td>Total</td>
                        <td>{stats['total_verses']:,}</td>
                        <td>100%</td>
                    </tr>
                </table>
            </section>
            
            <section>
                <h2>Overall Completion</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_pct}%;">
                        {completion_pct:.1f}% Complete
                    </div>
                </div>
            </section>
            
            <section>
                <h2>Book Completion</h2>
                <table>
                    <tr><th>Book</th><th>Total</th><th>Refined</th><th>Progress</th></tr>
                    {book_rows}
                </table>
            </section>
            
            <section>
                <h2>Next Actions</h2>
                <ol>
                    <li>Process remaining raw verses</li>
                    <li>Link events to verses</li>
                    <li>Activate dormant motifs as processing reaches their pages</li>
                    <li>Verify thread density at each 50-page interval</li>
                    <li>Export completed books for review</li>
                </ol>
            </section>
        </main>
        """
        
        html_output = self._wrap_html("ΒΊΒΛΟΣ ΛΌΓΟΥ: Progress Dashboard", content)
        
        output_file = self.config.output_dir / "Progress_Dashboard.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        logger.info(f"Exported progress dashboard to {output_file}")
        return output_file


# ============================================================================
# MASTER OUTPUT ORCHESTRATOR
# ============================================================================

class OutputOrchestrator:
    """Orchestrate all output generation"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.markdown = MarkdownGenerator(self.db)
        self.json_gen = JSONGenerator(self.db)
        self.html = HTMLGenerator(self.db)
    
    def export_all(self, formats: List[str] = None) -> Dict[str, List[Path]]:
        """Export all available outputs"""
        formats = formats or ['markdown', 'json']
        results = {'markdown': [], 'json': [], 'html': []}
        
        # Always generate dashboard in markdown
        results['markdown'].append(self.markdown.export_progress_dashboard())
        
        if 'markdown' in formats:
            # Export hermeneutical arrangement
            results['markdown'].append(self.markdown.export_hermeneutical_arrangement())
            
            # Export motif registry
            results['markdown'].append(self.markdown.export_motif_registry())
        
        if 'json' in formats:
            # Export full database
            results['json'].append(self.json_gen.export_full_database())
        
        if 'html' in formats:
            # Export HTML versions
            results['html'].append(self.html.export_progress_dashboard())
            results['html'].append(self.html.export_hermeneutical_arrangement())
            results['html'].append(self.html.export_motif_registry())
        
        return results
    
    def export_book(self, book_name: str, formats: List[str] = None) -> Dict[str, Path]:
        """Export a specific book in requested formats"""
        formats = formats or ['markdown']
        results = {}
        
        if 'markdown' in formats:
            results['markdown'] = self.markdown.export_book(book_name)
        
        if 'json' in formats:
            results['json'] = self.json_gen.export_book(book_name)
        
        if 'html' in formats:
            results['html'] = self.html.export_book(book_name)
        
        return results


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main entry point for output generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Output Generation')
    parser.add_argument('--book', type=str, help='Export specific book')
    parser.add_argument('--all', action='store_true', help='Export all outputs')
    parser.add_argument('--dashboard', action='store_true', help='Generate dashboard only')
    parser.add_argument('--format', choices=['markdown', 'json', 'html', 'both', 'all'], default='markdown',
                       help='Output format (markdown, json, html, both for md+json, all for all formats)')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    from scripts.database import init_db
    if not init_db():
        logger.error("Failed to initialize database")
        return 1
    
    orchestrator = OutputOrchestrator()
    
    # Parse format options
    if args.format == 'both':
        formats = ['markdown', 'json']
    elif args.format == 'all':
        formats = ['markdown', 'json', 'html']
    else:
        formats = [args.format]
    
    if args.dashboard:
        orchestrator.markdown.export_progress_dashboard()
        if 'html' in formats:
            orchestrator.html.export_progress_dashboard()
    elif args.book:
        orchestrator.export_book(args.book, formats)
    elif args.all:
        orchestrator.export_all(formats)
    else:
        # Default: generate dashboard
        orchestrator.markdown.export_progress_dashboard()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
