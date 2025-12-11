#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Cross-Reference Intelligence System
Advanced cross-reference analysis and typological network building.

This module provides:
- Cross-reference type definitions and weights
- Typological pair management
- Network analysis for verse connections
- Strength calculation for reference chains
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set, FrozenSet
from dataclasses import dataclass, field
from collections import defaultdict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER
from scripts.database import get_db, DatabaseManager, DatabaseError, QueryError

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class CrossReferenceError(Exception):
    """Base exception for cross-reference operations."""
    pass


class ReferenceNotFoundError(CrossReferenceError):
    """Raised when a reference cannot be found."""
    pass


class NetworkError(CrossReferenceError):
    """Raised when network analysis fails."""
    pass


# ============================================================================
# CROSS-REFERENCE TYPES AND WEIGHTS
# ============================================================================

@dataclass(frozen=True)
class ReferenceType:
    """Definition of a cross-reference type."""
    name: str
    description: str
    weight: float
    bidirectional: bool


REFERENCE_TYPES: Dict[str, Dict[str, Any]] = {
    'quotation': {
        'description': 'Direct quotation from OT in NT',
        'weight': 1.0,
        'bidirectional': False
    },
    'allusion': {
        'description': 'Clear allusion without direct quote',
        'weight': 0.8,
        'bidirectional': True
    },
    'echo': {
        'description': 'Verbal or thematic echo',
        'weight': 0.6,
        'bidirectional': True
    },
    'type_antitype': {
        'description': 'Typological correspondence',
        'weight': 0.9,
        'bidirectional': False
    },
    'parallel': {
        'description': 'Parallel passage (synoptic, etc.)',
        'weight': 0.7,
        'bidirectional': True
    },
    'thematic': {
        'description': 'Shared theme or concept',
        'weight': 0.5,
        'bidirectional': True
    },
    'linguistic': {
        'description': 'Shared vocabulary (Hebrew/Greek)',
        'weight': 0.4,
        'bidirectional': True
    },
    'structural': {
        'description': 'Structural parallel in narrative',
        'weight': 0.6,
        'bidirectional': True
    }
}

# Key typological pairs per Orthodox exegesis
TYPOLOGICAL_PAIRS: List[Tuple[str, str, str, str]] = [
    # Creation/New Creation
    ('Genesis 1:1-3', 'John 1:1-5', 'type_antitype', 'Creation and Word'),
    ('Genesis 2:7', '1 Corinthians 15:45', 'type_antitype', 'First and Last Adam'),
    
    # Sacrifice/Redemption
    ('Genesis 22:1-14', 'John 19:17-18', 'type_antitype', 'Binding of Isaac / Crucifixion'),
    ('Exodus 12:1-13', 'John 1:29', 'type_antitype', 'Passover Lamb'),
    ('Leviticus 16:1-34', 'Hebrews 9:1-14', 'type_antitype', 'Day of Atonement'),
    
    # Deliverance
    ('Exodus 14:21-22', 'Matthew 3:13-17', 'type_antitype', 'Red Sea / Baptism'),
    ('Jonah 1:17', 'Matthew 12:40', 'type_antitype', 'Three Days in Fish/Tomb'),
    ('Numbers 21:8-9', 'John 3:14-15', 'type_antitype', 'Bronze Serpent / Lifted Up'),
    
    # Bread/Manna
    ('Exodus 16:14-15', 'John 6:31-35', 'type_antitype', 'Manna / Bread of Life'),
    
    # Temple/Body
    ('Exodus 25-27', 'John 2:19-21', 'type_antitype', 'Tabernacle / Body of Christ'),
    ('1 Kings 8:10-11', 'John 1:14', 'type_antitype', 'Glory Filling Temple / Word Dwelling'),
    
    # Shepherd
    ('Psalm 23:1', 'John 10:11', 'type_antitype', 'Divine Shepherd'),
    ('Ezekiel 34:11-16', 'Luke 15:3-7', 'type_antitype', 'Seeking Lost Sheep'),
    
    # Suffering Servant
    ('Isaiah 53:1-12', 'Mark 15:1-39', 'type_antitype', 'Suffering Servant / Passion'),
    ('Psalm 22:1-31', 'Matthew 27:35-46', 'type_antitype', 'Psalm of Dereliction'),
    
    # King/Kingdom
    ('2 Samuel 7:12-16', 'Luke 1:32-33', 'type_antitype', 'Davidic Covenant'),
    ('Daniel 7:13-14', 'Revelation 1:7', 'type_antitype', 'Son of Man Coming'),
    
    # Covenant
    ('Jeremiah 31:31-34', 'Luke 22:20', 'type_antitype', 'New Covenant'),
    ('Genesis 17:1-14', 'Colossians 2:11-12', 'type_antitype', 'Circumcision / Baptism')
]


# ============================================================================
# CROSS-REFERENCE ANALYZER
# ============================================================================

class CrossReferenceAnalyzer:
    """
    Analyze and build cross-reference networks.
    
    Provides methods for finding related verses, building
    typological networks, and calculating reference strengths.
    """
    
    def __init__(self, db: Optional[DatabaseManager] = None) -> None:
        """
        Initialize the analyzer.
        
        Args:
            db: Optional database manager. Uses global if not provided.
        """
        self.db = db or get_db()
        self._verse_cache: Dict[str, int] = {}
    
    def _get_verse_id(self, verse_ref: str) -> Optional[int]:
        """
        Get verse ID from reference with caching.
        
        Args:
            verse_ref: Verse reference string.
            
        Returns:
            Verse ID or None if not found.
        """
        if not verse_ref:
            return None
            
        if verse_ref in self._verse_cache:
            return self._verse_cache[verse_ref]
        
        try:
            verse = self.db.fetch_one(
                "SELECT id FROM verses WHERE verse_reference = %s",
                (verse_ref,)
            )
            if verse:
                self._verse_cache[verse_ref] = verse['id']
                return verse['id']
        except (DatabaseError, QueryError) as e:
            logger.error(f"Failed to get verse ID for {verse_ref}: {e}")
        
        return None
    
    def find_references_for_verse(self, verse_ref: str) -> Dict[str, Any]:
        """
        Find all cross-references for a verse.
        
        Args:
            verse_ref: Verse reference string.
            
        Returns:
            Dictionary with incoming, outgoing references and typological info.
            
        Raises:
            ReferenceNotFoundError: If the verse is not found.
        """
        if not verse_ref:
            raise ValueError("verse_ref cannot be empty")
            
        verse_id = self._get_verse_id(verse_ref)
        
        if not verse_id:
            raise ReferenceNotFoundError(f'Verse not found: {verse_ref}')
        
        try:
            # Get outgoing references (this verse references others)
            outgoing = self.db.fetch_all("""
                SELECT 
                    v.verse_reference as target,
                    cr.relationship_type,
                    cr.confidence_score,
                    cr.notes
                FROM cross_references cr
                JOIN verses v ON cr.to_verse_id = v.id
                WHERE cr.from_verse_id = %s
                ORDER BY cr.confidence_score DESC
            """, (verse_id,))
            
            # Get incoming references (others reference this verse)
            incoming = self.db.fetch_all("""
                SELECT 
                    v.verse_reference as source,
                    cr.relationship_type,
                    cr.confidence_score,
                    cr.notes
                FROM cross_references cr
                JOIN verses v ON cr.from_verse_id = v.id
                WHERE cr.to_verse_id = %s
                ORDER BY cr.confidence_score DESC
            """, (verse_id,))
            
            return {
                'verse': verse_ref,
                'outgoing': [dict(r) for r in outgoing],
                'incoming': [dict(r) for r in incoming],
                'total_references': len(outgoing) + len(incoming)
            }
        except (DatabaseError, QueryError) as e:
            logger.error(f"Failed to find references for {verse_ref}: {e}")
            raise CrossReferenceError(f"Failed to find references: {e}") from e
    
    def calculate_verse_centrality(self, verse_ref: str) -> float:
        """
        Calculate how central a verse is in the reference network.
        
        Args:
            verse_ref: Verse reference string.
            
        Returns:
            Centrality score (higher = more central).
        """
        try:
            refs = self.find_references_for_verse(verse_ref)
        except (ReferenceNotFoundError, CrossReferenceError):
            return 0.0
        
        # Simple centrality: weighted count of references
        total_weight = 0.0
        
        for ref in refs['outgoing']:
            ref_type = ref.get('relationship_type', 'thematic')
            weight = REFERENCE_TYPES.get(ref_type, {}).get('weight', 0.5)
            confidence = ref.get('confidence_score', 0.5)
            total_weight += weight * confidence
        
        for ref in refs['incoming']:
            ref_type = ref.get('relationship_type', 'thematic')
            weight = REFERENCE_TYPES.get(ref_type, {}).get('weight', 0.5)
            confidence = ref.get('confidence_score', 0.5)
            total_weight += weight * confidence
        
        return total_weight
    
    def build_reference_chain(
        self, 
        start_ref: str, 
        max_depth: int = 3
    ) -> Dict[str, Any]:
        """
        Build a chain of references starting from a verse.
        
        Args:
            start_ref: Starting verse reference.
            max_depth: Maximum depth of reference chain.
            
        Returns:
            Dictionary with root, nodes, and edges.
        """
        if max_depth < 1:
            max_depth = 1
            
        visited: Set[str] = set()
        chain: Dict[str, Any] = {
            'root': start_ref,
            'nodes': [],
            'edges': []
        }
        
        def traverse(verse_ref: str, depth: int):
            if depth > max_depth or verse_ref in visited:
                return
            
            visited.add(verse_ref)
            chain['nodes'].append({
                'ref': verse_ref,
                'depth': depth
            })
            
            refs = self.find_references_for_verse(verse_ref)
            if 'error' in refs:
                return
            
            for ref in refs['outgoing'][:5]:  # Limit branching
                target = ref['target']
                chain['edges'].append({
                    'source': verse_ref,
                    'target': target,
                    'type': ref['relationship_type']
                })
                traverse(target, depth + 1)
        
        traverse(start_ref, 0)
        return chain
    
    def find_typological_clusters(self) -> List[Dict[str, Any]]:
        """Find clusters of typologically related verses"""
        clusters = []
        
        # Get all type-antitype relationships
        type_refs = self.db.fetch_all("""
            SELECT 
                tc.id,
                v1.verse_reference as type_ref,
                v2.verse_reference as antitype_ref,
                tc.correspondence_type,
                tc.narrative_description
            FROM typological_correspondences tc
            JOIN verses v1 ON tc.type_verse_id = v1.id
            JOIN verses v2 ON tc.antitype_verse_id = v2.id
            WHERE tc.status = 'verified'
        """)
        
        # Group by theme
        by_theme = defaultdict(list)
        for ref in type_refs:
            theme = ref.get('correspondence_type', 'general')
            by_theme[theme].append(ref)
        
        for theme, refs in by_theme.items():
            if len(refs) >= 2:
                clusters.append({
                    'theme': theme,
                    'size': len(refs),
                    'type_verses': list(set(r['type_ref'] for r in refs)),
                    'antitype_verses': list(set(r['antitype_ref'] for r in refs))
                })
        
        return sorted(clusters, key=lambda c: c['size'], reverse=True)


# ============================================================================
# TYPOLOGICAL NETWORK BUILDER
# ============================================================================

class TypologicalNetworkBuilder:
    """Build and manage the typological correspondence network"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def initialize_core_typologies(self) -> int:
        """Initialize core typological pairs from Orthodox tradition"""
        inserted = 0
        
        for type_ref, antitype_ref, rel_type, description in TYPOLOGICAL_PAIRS:
            success = self.add_correspondence(
                type_ref, antitype_ref, rel_type, description
            )
            if success:
                inserted += 1
        
        logger.info(f"Initialized {inserted} core typological correspondences")
        return inserted
    
    def add_correspondence(self, type_ref: str, antitype_ref: str,
                          correspondence_type: str,
                          narrative_description: str = None) -> bool:
        """Add a typological correspondence"""
        # Get verse IDs
        type_verse = self.db.fetch_one(
            "SELECT id FROM verses WHERE verse_reference LIKE %s",
            (f"{type_ref.split(':')[0]}%",)  # Match book and chapter
        )
        antitype_verse = self.db.fetch_one(
            "SELECT id FROM verses WHERE verse_reference LIKE %s",
            (f"{antitype_ref.split(':')[0]}%",)
        )
        
        if not type_verse or not antitype_verse:
            logger.warning(f"Could not find verses for: {type_ref} -> {antitype_ref}")
            return False
        
        # Calculate distance
        distance = self._calculate_canonical_distance(type_ref, antitype_ref)
        
        try:
            self.db.execute("""
                INSERT INTO typological_correspondences
                (type_verse_id, antitype_verse_id, correspondence_type,
                 narrative_description, distance, status)
                VALUES (%s, %s, %s, %s, %s, 'verified')
                ON CONFLICT DO NOTHING
            """, (
                type_verse['id'], antitype_verse['id'],
                correspondence_type, narrative_description, distance
            ))
            return True
        except Exception as e:
            logger.error(f"Failed to add correspondence: {e}")
            return False
    
    def _calculate_canonical_distance(self, ref1: str, ref2: str) -> int:
        """Calculate canonical distance between two references"""
        # Extract book names
        book1 = ref1.split()[0] if ' ' in ref1 else ref1.split(':')[0]
        book2 = ref2.split()[0] if ' ' in ref2 else ref2.split(':')[0]
        
        # Handle numbered books
        for prefix in ['1', '2', '3']:
            if ref1.startswith(prefix + ' '):
                book1 = ' '.join(ref1.split()[:2])
            if ref2.startswith(prefix + ' '):
                book2 = ' '.join(ref2.split()[:2])
        
        order1 = CANONICAL_ORDER.get(book1, 0)
        order2 = CANONICAL_ORDER.get(book2, 0)
        
        return abs(int(order2) - int(order1))
    
    def find_potential_correspondences(self, verse_ref: str) -> List[Dict[str, Any]]:
        """Find potential typological correspondences for a verse"""
        verse = self.db.fetch_one("""
            SELECT v.*, cb.category, cb.testament
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.verse_reference = %s
        """, (verse_ref,))
        
        if not verse:
            return []
        
        potentials = []
        
        # If OT, look for NT fulfillments
        if verse['testament'] == 'old':
            candidates = self.db.fetch_all("""
                SELECT v.verse_reference, v.text_kjv, cb.category
                FROM verses v
                JOIN canonical_books cb ON v.book_id = cb.id
                WHERE cb.testament = 'new'
                AND v.text_kjv IS NOT NULL
                LIMIT 100
            """)
            
            # Simple keyword matching for demonstration
            verse_text = (verse.get('text_kjv') or '').lower()
            keywords = set(verse_text.split()) - {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'it', 'for'}
            
            for candidate in candidates:
                candidate_text = (candidate.get('text_kjv') or '').lower()
                candidate_keywords = set(candidate_text.split()) - {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'it', 'for'}
                
                overlap = keywords & candidate_keywords
                if len(overlap) >= 3:
                    potentials.append({
                        'reference': candidate['verse_reference'],
                        'category': candidate['category'],
                        'shared_keywords': list(overlap),
                        'confidence': len(overlap) / max(len(keywords), 1)
                    })
        
        return sorted(potentials, key=lambda p: p['confidence'], reverse=True)[:10]
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Get statistics about the typological network"""
        stats = {}
        
        # Total correspondences
        total = self.db.fetch_one(
            "SELECT COUNT(*) as count FROM typological_correspondences"
        )
        stats['total_correspondences'] = total['count'] if total else 0
        
        # By type
        by_type = self.db.fetch_all("""
            SELECT correspondence_type, COUNT(*) as count
            FROM typological_correspondences
            GROUP BY correspondence_type
            ORDER BY count DESC
        """)
        stats['by_type'] = {r['correspondence_type']: r['count'] for r in by_type}
        
        # Average distance
        avg_dist = self.db.fetch_one(
            "SELECT AVG(distance) as avg FROM typological_correspondences"
        )
        stats['average_distance'] = round(avg_dist['avg'], 2) if avg_dist and avg_dist['avg'] else 0
        
        # Most connected verses
        most_connected = self.db.fetch_all("""
            SELECT 
                v.verse_reference,
                (
                    SELECT COUNT(*) FROM typological_correspondences 
                    WHERE type_verse_id = v.id OR antitype_verse_id = v.id
                ) as connections
            FROM verses v
            ORDER BY connections DESC
            LIMIT 10
        """)
        stats['most_connected'] = [
            {'verse': r['verse_reference'], 'connections': r['connections']}
            for r in most_connected if r['connections'] > 0
        ]
        
        return stats


# ============================================================================
# REFERENCE SUGGESTER
# ============================================================================

class ReferenceSuggester:
    """Suggest cross-references for content enhancement"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.analyzer = CrossReferenceAnalyzer(db)
        self.network = TypologicalNetworkBuilder(db)
    
    def suggest_for_verse(self, verse_ref: str, 
                         max_suggestions: int = 5) -> Dict[str, Any]:
        """Suggest cross-references for enhancing verse commentary"""
        suggestions = {
            'verse': verse_ref,
            'existing_references': [],
            'suggested_additions': [],
            'typological_opportunities': []
        }
        
        # Get existing
        existing = self.analyzer.find_references_for_verse(verse_ref)
        if 'error' not in existing:
            suggestions['existing_references'] = (
                existing['outgoing'][:5] + existing['incoming'][:5]
            )
        
        # Find typological opportunities
        typological = self.network.find_potential_correspondences(verse_ref)
        suggestions['typological_opportunities'] = typological[:max_suggestions]
        
        # Suggest based on shared themes (simplified)
        verse = self.db.fetch_one("""
            SELECT v.*, cb.category FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.verse_reference = %s
        """, (verse_ref,))
        
        if verse:
            # Find verses with similar theological weight
            similar = self.db.fetch_all("""
                SELECT verse_reference, theological_weight, emotional_valence
                FROM verses
                WHERE ABS(theological_weight - %s) < 0.1
                AND verse_reference != %s
                ORDER BY RANDOM()
                LIMIT %s
            """, (verse.get('theological_weight', 0.5), verse_ref, max_suggestions))
            
            suggestions['suggested_additions'] = [
                {
                    'reference': s['verse_reference'],
                    'reason': 'Similar theological weight',
                    'type': 'thematic'
                }
                for s in similar
            ]
        
        return suggestions
    
    def bulk_suggest(self, book_name: str, 
                    min_references: int = 3) -> List[Dict[str, Any]]:
        """Suggest references for verses in a book that have few connections"""
        # Find verses with few references
        verses = self.db.fetch_all("""
            SELECT v.verse_reference
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE cb.name = %s
            AND (
                SELECT COUNT(*) FROM cross_references 
                WHERE from_verse_id = v.id OR to_verse_id = v.id
            ) < %s
            ORDER BY v.chapter, v.verse_number
            LIMIT 50
        """, (book_name, min_references))
        
        suggestions = []
        for verse in verses:
            verse_suggestions = self.suggest_for_verse(verse['verse_reference'])
            if verse_suggestions['suggested_additions'] or verse_suggestions['typological_opportunities']:
                suggestions.append(verse_suggestions)
        
        return suggestions


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for cross-reference system"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Cross-Reference System')
    parser.add_argument('--init-typology', action='store_true', 
                       help='Initialize core typological correspondences')
    parser.add_argument('--analyze', type=str, help='Analyze references for verse')
    parser.add_argument('--chain', type=str, help='Build reference chain from verse')
    parser.add_argument('--suggest', type=str, help='Suggest references for verse')
    parser.add_argument('--stats', action='store_true', help='Show network statistics')
    parser.add_argument('--clusters', action='store_true', help='Find typological clusters')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    from scripts.database import init_db
    if not init_db():
        print("Failed to initialize database")
        return 1
    
    if args.init_typology:
        builder = TypologicalNetworkBuilder()
        count = builder.initialize_core_typologies()
        print(f"Initialized {count} typological correspondences")
    
    elif args.analyze:
        analyzer = CrossReferenceAnalyzer()
        refs = analyzer.find_references_for_verse(args.analyze)
        print(f"\nReferences for {args.analyze}:")
        print(f"  Outgoing: {len(refs.get('outgoing', []))}")
        for r in refs.get('outgoing', [])[:5]:
            print(f"    → {r['target']} ({r['relationship_type']})")
        print(f"  Incoming: {len(refs.get('incoming', []))}")
        for r in refs.get('incoming', [])[:5]:
            print(f"    ← {r['source']} ({r['relationship_type']})")
    
    elif args.chain:
        analyzer = CrossReferenceAnalyzer()
        chain = analyzer.build_reference_chain(args.chain)
        print(f"\nReference chain from {args.chain}:")
        print(f"  Nodes: {len(chain['nodes'])}")
        print(f"  Edges: {len(chain['edges'])}")
        for edge in chain['edges'][:10]:
            print(f"    {edge['source']} → {edge['target']} ({edge['type']})")
    
    elif args.suggest:
        suggester = ReferenceSuggester()
        suggestions = suggester.suggest_for_verse(args.suggest)
        print(f"\nSuggestions for {args.suggest}:")
        print(f"  Existing: {len(suggestions['existing_references'])}")
        print(f"  Suggested additions:")
        for s in suggestions['suggested_additions']:
            print(f"    • {s['reference']} ({s['reason']})")
        print(f"  Typological opportunities:")
        for t in suggestions['typological_opportunities']:
            print(f"    • {t['reference']} (confidence: {t['confidence']:.2f})")
    
    elif args.stats:
        builder = TypologicalNetworkBuilder()
        stats = builder.get_network_statistics()
        print("\nTypological Network Statistics:")
        print(f"  Total Correspondences: {stats['total_correspondences']}")
        print(f"  Average Distance: {stats['average_distance']}")
        print("  By Type:")
        for t, c in stats.get('by_type', {}).items():
            print(f"    {t}: {c}")
        print("  Most Connected Verses:")
        for v in stats.get('most_connected', [])[:5]:
            print(f"    {v['verse']}: {v['connections']} connections")
    
    elif args.clusters:
        analyzer = CrossReferenceAnalyzer()
        clusters = analyzer.find_typological_clusters()
        print("\nTypological Clusters:")
        for cluster in clusters[:10]:
            print(f"\n  {cluster['theme']} ({cluster['size']} correspondences):")
            print(f"    Types: {', '.join(cluster['type_verses'][:3])}")
            print(f"    Antitypes: {', '.join(cluster['antitype_verses'][:3])}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
