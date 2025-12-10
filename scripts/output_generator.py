#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Output Generation System
Generate formatted output in multiple formats (Markdown, JSON, HTML, LaTeX)
"""

import sys
import json
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
# MASTER OUTPUT ORCHESTRATOR
# ============================================================================

class OutputOrchestrator:
    """Orchestrate all output generation"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.markdown = MarkdownGenerator(self.db)
        self.json_gen = JSONGenerator(self.db)
    
    def export_all(self, formats: List[str] = None) -> Dict[str, List[Path]]:
        """Export all available outputs"""
        formats = formats or ['markdown', 'json']
        results = {'markdown': [], 'json': []}
        
        # Always generate dashboard
        results['markdown'].append(self.markdown.export_progress_dashboard())
        
        if 'markdown' in formats:
            # Export hermeneutical arrangement
            results['markdown'].append(self.markdown.export_hermeneutical_arrangement())
            
            # Export motif registry
            results['markdown'].append(self.markdown.export_motif_registry())
        
        if 'json' in formats:
            # Export full database
            results['json'].append(self.json_gen.export_full_database())
        
        return results
    
    def export_book(self, book_name: str, formats: List[str] = None) -> Dict[str, Path]:
        """Export a specific book in requested formats"""
        formats = formats or ['markdown']
        results = {}
        
        if 'markdown' in formats:
            results['markdown'] = self.markdown.export_book(book_name)
        
        if 'json' in formats:
            results['json'] = self.json_gen.export_book(book_name)
        
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
    parser.add_argument('--format', choices=['markdown', 'json', 'both'], default='markdown')
    
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
    
    formats = ['markdown', 'json'] if args.format == 'both' else [args.format]
    
    if args.dashboard:
        orchestrator.markdown.export_progress_dashboard()
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
