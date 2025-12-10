#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Sensory Vocabulary System
Comprehensive sensory vocabulary management per Stratified Foundation System
"""

import sys
import random
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# SENSORY VOCABULARY CODEX
# ============================================================================

# Complete sensory vocabulary organized by category and modality
SENSORY_CODEX = {
    'pentateuch': {
        'visual': [
            'primordial darkness giving way to light',
            'pillar of fire illuminating wilderness',
            'mountain shrouded in smoke and glory',
            'burning bush unconsumed by flame',
            'tabernacle gold gleaming in lamplight',
            'cloud of presence descending',
            'rainbow arcing across rain-washed sky',
            'stars scattered like sand across the firmament',
            'blood-marked doorposts in Egyptian night',
            'waters standing as walls of crystal',
            'manna glistening on morning ground',
            'serpent bronze lifted against desert sun',
            'face radiant with borrowed glory',
            'curtain woven in crimson and blue'
        ],
        'auditory': [
            'thunderous divine voice from Sinai',
            'still whisper in sacred silence',
            'trumpet blast announcing presence',
            'shofar blast piercing dawn',
            'voice like many waters',
            'words spoken into void',
            'cry of firstborn piercing night',
            'song rising from far shore',
            'murmuring of discontent',
            'blessing pronounced over bowed head'
        ],
        'tactile': [
            'dust shaped by divine fingers',
            'breath entering clay nostrils',
            'rough hemp biting into wrists',
            'grain of wood against shoulder',
            'water parting at staff-touch',
            'tablets cold and heavy with command',
            'oil anointing running warm',
            'bread unleavened and flat on tongue',
            'lamb warm beneath knife'
        ],
        'olfactory': [
            'smoke of sacrifice ascending',
            'incense cloud filling holy space',
            'blood copper-sharp in morning air',
            'manna sweet as honey cakes',
            'cedar and acacia fresh-cut',
            'burning flesh on altar stones'
        ],
        'kinesthetic': [
            'walking in garden cool',
            'falling prostrate before presence',
            'wrestling through the night',
            'climbing toward smoking summit',
            'wandering through wilderness years',
            'crossing on dry ground'
        ]
    },
    'gospel': {
        'visual': [
            'Jesus face shining transfigured',
            'crowd pressing close in streets',
            'cross silhouetted against darkness',
            'empty tomb in morning light',
            'water becoming wine-dark',
            'bread broken in weathered hands',
            'blood and water flowing',
            'seamless robe lying folded',
            'nets straining with catch',
            'fig tree withered overnight',
            'temple veil torn from top',
            'soldiers casting lots',
            'women weeping at distance',
            'risen Lord unrecognized'
        ],
        'auditory': [
            'voice crying in wilderness',
            'crowds shouting hosanna',
            'silence before accusers',
            'rooster crow piercing denial',
            'words spoken from cross',
            'thunder answering prayer',
            'weeping at beloved tomb',
            'greeting of peace offered',
            'command to lazarus come forth',
            'whisper calling by name'
        ],
        'tactile': [
            'water poured over head',
            'mud on blind eyes',
            'garment hem brushed',
            'feet washed with tears',
            'bread placed in hand',
            'nails driven through flesh',
            'spear piercing side',
            'linen wrapping body',
            'wounds offered to touch',
            'fish and bread shared'
        ],
        'olfactory': [
            'perfume filling the house',
            'nard poured in abundance',
            'burial spices prepared',
            'fish grilling on shore',
            'garden blooming at dawn'
        ],
        'gustatory': [
            'wine tasted new and good',
            'bread broken and shared',
            'bitter cup not passing',
            'vinegar offered on sponge',
            'fish eaten to prove flesh'
        ]
    },
    'poetic': {
        'visual': [
            'heavens declaring glory',
            'sun like bridegroom emerging',
            'moon marking seasons',
            'stars telling their story',
            'mountains melting like wax',
            'rivers clapping hands',
            'trees of field rejoicing',
            'darkness covering the deep',
            'light dwelling in splendor',
            'dove wings silver-shining'
        ],
        'auditory': [
            'voice of the Lord thundering',
            'praise echoing from hills',
            'groaning too deep for words',
            'song rising in the night',
            'harp strings trembling',
            'cymbals crashing praise',
            'whisper of wisdom calling',
            'silence saying everything'
        ],
        'tactile': [
            'rod and staff comforting',
            'oil overflowing cup',
            'tears stored in bottle',
            'dust returning to dust',
            'bones dried in valley',
            'heart broken and contrite',
            'feet set upon rock'
        ],
        'olfactory': [
            'incense prayer ascending',
            'myrrh and aloes fragrant',
            'garden spices breathing',
            'sacrifice smoke rising'
        ]
    },
    'major_prophet': {
        'visual': [
            'throne high and lifted up',
            'seraphim covering face and feet',
            'coal taken from altar',
            'scroll unrolling with woe',
            'watchman on the wall',
            'valley of dry bones',
            'wheel within wheel turning',
            'glory departing from temple',
            'branch growing from stump',
            'suffering servant marred',
            'new heavens and earth'
        ],
        'auditory': [
            'holy holy holy proclaimed',
            'voice like trumpet calling',
            'rattling of bones assembling',
            'word like hammer breaking',
            'lamentation rising',
            'comfort comfort spoken'
        ],
        'tactile': [
            'coal burning lips clean',
            'yoke heavy on shoulders',
            'chains binding prophet',
            'scroll eaten sweet then bitter',
            'breath entering the slain'
        ]
    },
    'apocalyptic': {
        'visual': [
            'throne room glory blazing',
            'Lamb standing as slain',
            'New Jerusalem descending',
            'sea of glass like crystal',
            'seven torches burning',
            'living creatures covered with eyes',
            'scroll with seven seals',
            'riders on colored horses',
            'woman clothed with sun',
            'dragon swept third of stars',
            'beast rising from sea',
            'city of pure gold transparent',
            'river of life crystal-clear',
            'tree bearing twelve fruits',
            'no more night nor sun'
        ],
        'auditory': [
            'voice like trumpet speaking',
            'thunder of many waters',
            'silence in heaven for half hour',
            'trumpets sounding judgment',
            'new song before the throne',
            'hallelujah rising',
            'come Lord Jesus whispered'
        ],
        'olfactory': [
            'incense of prayers ascending',
            'smoke of torment rising',
            'brimstone burning'
        ]
    },
    'pauline': {
        'visual': [
            'light brighter than sun striking',
            'scales falling from eyes',
            'mirror dimly showing',
            'face to face revealing',
            'body broken for you',
            'baptism burial-rising',
            'armor of God gleaming',
            'cloud of witnesses surrounding'
        ],
        'auditory': [
            'groaning of creation',
            'tongues of angels speaking',
            'trumpet of resurrection',
            'word rightly divided',
            'gospel proclaimed'
        ],
        'kinesthetic': [
            'running the race',
            'fighting the fight',
            'pressing toward the goal',
            'standing firm',
            'walking in newness'
        ]
    }
}


# ============================================================================
# VOCABULARY MANAGER
# ============================================================================

class SensoryVocabularyManager:
    """Manage sensory vocabulary selection and tracking"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.usage_tracker: Dict[str, Dict] = defaultdict(lambda: {
            'last_page': 0,
            'total_uses': 0
        })
        self._load_usage_history()
    
    def _load_usage_history(self):
        """Load usage history from database"""
        try:
            results = self.db.fetch_all("""
                SELECT term, last_used_page, usage_count
                FROM sensory_vocabulary
                WHERE usage_count > 0
            """)
            
            for r in results:
                self.usage_tracker[r['term']] = {
                    'last_page': r['last_used_page'] or 0,
                    'total_uses': r['usage_count']
                }
        except Exception as e:
            logger.debug(f"Could not load usage history: {e}")
    
    def get_vocabulary_for_verse(self, category: str, modality: str,
                                 current_page: int,
                                 emotional_weight: str = 'neutral',
                                 count: int = 3) -> List[str]:
        """
        Get appropriate vocabulary for a verse, avoiding recent overuse.
        Maintains minimum 100 pages between uses per Stratified Foundation System.
        """
        # Get available vocabulary
        available = SENSORY_CODEX.get(category, {}).get(modality, [])
        
        if not available:
            # Fallback to generic vocabulary
            available = self._get_fallback_vocabulary(modality)
        
        # Filter by recency (minimum 100 pages between uses)
        min_distance = 100
        filtered = []
        
        for term in available:
            usage = self.usage_tracker.get(term, {'last_page': 0})
            if current_page - usage['last_page'] >= min_distance:
                filtered.append(term)
        
        # If too few options, relax the constraint
        if len(filtered) < count:
            filtered = available
        
        # Prefer less-used terms
        filtered.sort(key=lambda t: self.usage_tracker.get(t, {}).get('total_uses', 0))
        
        # Select with some randomization among top candidates
        top_candidates = filtered[:max(count * 3, 10)]
        selected = random.sample(top_candidates, min(count, len(top_candidates)))
        
        # Record usage
        for term in selected:
            self._record_usage(term, current_page, category, modality)
        
        return selected
    
    def _get_fallback_vocabulary(self, modality: str) -> List[str]:
        """Get generic fallback vocabulary"""
        fallbacks = {
            'visual': [
                'light breaking through',
                'shadow falling',
                'form emerging',
                'color deepening',
                'horizon stretching'
            ],
            'auditory': [
                'voice speaking',
                'silence deepening',
                'sound rising',
                'words falling',
                'echo fading'
            ],
            'tactile': [
                'weight pressing',
                'texture rough',
                'surface smooth',
                'warmth spreading',
                'cold settling'
            ],
            'olfactory': [
                'scent lingering',
                'fragrance rising',
                'air thick',
                'smoke drifting'
            ],
            'gustatory': [
                'taste lingering',
                'sweetness fading',
                'bitterness sharp'
            ],
            'kinesthetic': [
                'movement flowing',
                'stillness holding',
                'effort straining',
                'rest settling'
            ]
        }
        return fallbacks.get(modality, fallbacks['visual'])
    
    def _record_usage(self, term: str, page: int, category: str, modality: str):
        """Record vocabulary usage"""
        self.usage_tracker[term] = {
            'last_page': page,
            'total_uses': self.usage_tracker.get(term, {}).get('total_uses', 0) + 1
        }
        
        try:
            self.db.execute("""
                INSERT INTO sensory_vocabulary (category, sensory_domain, term, usage_count, last_used_page)
                VALUES (%s, %s, %s, 1, %s)
                ON CONFLICT (category, sensory_domain, term) 
                DO UPDATE SET 
                    usage_count = sensory_vocabulary.usage_count + 1,
                    last_used_page = %s
            """, (category, modality, term, page, page))
        except Exception as e:
            logger.debug(f"Could not record usage: {e}")
    
    def get_vocabulary_stats(self) -> Dict[str, Any]:
        """Get statistics on vocabulary usage"""
        stats = {
            'total_terms': 0,
            'used_terms': 0,
            'by_category': {},
            'by_modality': {},
            'most_used': [],
            'never_used': []
        }
        
        # Count total terms
        for category, modalities in SENSORY_CODEX.items():
            stats['by_category'][category] = 0
            for modality, terms in modalities.items():
                stats['total_terms'] += len(terms)
                stats['by_category'][category] += len(terms)
                
                if modality not in stats['by_modality']:
                    stats['by_modality'][modality] = 0
                stats['by_modality'][modality] += len(terms)
        
        # Count used terms
        stats['used_terms'] = len([t for t, u in self.usage_tracker.items() if u['total_uses'] > 0])
        
        # Most used
        sorted_usage = sorted(
            self.usage_tracker.items(),
            key=lambda x: x[1]['total_uses'],
            reverse=True
        )
        stats['most_used'] = [
            {'term': t, 'uses': u['total_uses']}
            for t, u in sorted_usage[:10]
        ]
        
        # Never used
        all_terms = set()
        for modalities in SENSORY_CODEX.values():
            for terms in modalities.values():
                all_terms.update(terms)
        
        used_terms = set(self.usage_tracker.keys())
        stats['never_used'] = list(all_terms - used_terms)[:20]
        
        return stats
    
    def suggest_vocabulary_for_motif(self, motif_name: str, 
                                     modalities: List[str],
                                     current_page: int) -> Dict[str, List[str]]:
        """Suggest vocabulary aligned with a specific motif"""
        # Get motif's core vocabulary
        motif = self.db.fetch_one(
            "SELECT core_vocabulary, sensory_modalities FROM motifs WHERE name = %s",
            (motif_name,)
        )
        
        if not motif:
            return {}
        
        core_vocab = motif.get('core_vocabulary') or []
        preferred_modalities = motif.get('sensory_modalities') or modalities
        
        suggestions = {}
        
        for modality in preferred_modalities:
            # Get general vocabulary for modality
            general = []
            for category in SENSORY_CODEX:
                general.extend(SENSORY_CODEX[category].get(modality, []))
            
            # Filter for terms that resonate with motif vocabulary
            resonant = []
            for term in general:
                term_lower = term.lower()
                for core in core_vocab:
                    if core.lower() in term_lower:
                        resonant.append(term)
                        break
            
            # If no resonant terms, use general with low recent usage
            if not resonant:
                resonant = [t for t in general 
                           if current_page - self.usage_tracker.get(t, {}).get('last_page', 0) >= 100]
            
            suggestions[modality] = resonant[:5] if resonant else general[:5]
        
        return suggestions


# ============================================================================
# TEMPORAL FOLDING VOCABULARY
# ============================================================================

class TemporalFoldingVocabulary:
    """
    Manage vocabulary for temporal folding technique.
    "The language does not explain the connection but creates it."
    """
    
    # Key phrases that create temporal echoes
    FOLDING_PHRASES = {
        'binding': [
            'rough hemp biting into wrists',
            'cord wrapped tight',
            'bound hand and foot',
            'ropes cutting flesh'
        ],
        'wood': [
            'grain of wood against shoulder',
            'timber heavy with purpose',
            'beam shouldered up the hill',
            'tree bearing its burden'
        ],
        'sacrifice': [
            'knife catching sun',
            'blade raised',
            'offering upon the altar',
            'blood spilling down'
        ],
        'silence': [
            'silence before the act',
            'wordless walking',
            'no plea escaping lips',
            'quiet acceptance'
        ],
        'ascent': [
            'climbing toward the place',
            'walking upward',
            'summit waiting',
            'height approached'
        ],
        'lamb': [
            'lamb walking unknowing',
            'creature led',
            'offering without blemish',
            'one set apart'
        ]
    }
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.echo_tracker: Dict[str, List[int]] = defaultdict(list)
    
    def plant_phrase(self, theme: str, page: int) -> Optional[str]:
        """Plant a phrase that will echo later"""
        phrases = self.FOLDING_PHRASES.get(theme, [])
        if not phrases:
            return None
        
        # Select least recently used
        usage_counts = {p: len(self.echo_tracker.get(p, [])) for p in phrases}
        sorted_phrases = sorted(phrases, key=lambda p: usage_counts[p])
        
        selected = sorted_phrases[0]
        self.echo_tracker[selected].append(page)
        
        return selected
    
    def create_echo(self, original_phrase: str, variation_level: float = 0.3) -> str:
        """
        Create an echo of a planted phrase with variation.
        Per invisibility requirements: must vary but still resonate.
        """
        # Simple variation strategies
        variations = [
            # Word substitution
            lambda p: p.replace('rough', 'coarse').replace('biting', 'pressing'),
            # Perspective shift
            lambda p: p.replace('wrists', 'His wrists').replace('shoulder', 'His shoulder'),
            # Intensity modulation
            lambda p: p.replace('heavy', 'crushing').replace('tight', 'strangling'),
            # Slight reordering (where grammatically sensible)
            lambda p: p
        ]
        
        # Apply variation
        varied = random.choice(variations)(original_phrase)
        return varied
    
    def find_echo_opportunities(self, current_page: int, 
                                min_distance: int = 500) -> List[Dict]:
        """Find phrases planted earlier that could echo now"""
        opportunities = []
        
        for phrase, pages in self.echo_tracker.items():
            for plant_page in pages:
                distance = current_page - plant_page
                if distance >= min_distance:
                    opportunities.append({
                        'phrase': phrase,
                        'planted_at': plant_page,
                        'distance': distance,
                        'echo': self.create_echo(phrase)
                    })
        
        return sorted(opportunities, key=lambda x: x['distance'], reverse=True)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for sensory vocabulary management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Sensory Vocabulary System')
    parser.add_argument('--stats', action='store_true', help='Show vocabulary statistics')
    parser.add_argument('--get', nargs=3, metavar=('CATEGORY', 'MODALITY', 'PAGE'),
                       help='Get vocabulary for category/modality at page')
    parser.add_argument('--motif', type=str, help='Get vocabulary for motif')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    from scripts.database import init_db
    init_db()
    
    manager = SensoryVocabularyManager()
    
    if args.stats:
        stats = manager.get_vocabulary_stats()
        print("\nSensory Vocabulary Statistics:")
        print("=" * 50)
        print(f"Total Terms: {stats['total_terms']}")
        print(f"Used Terms: {stats['used_terms']}")
        print(f"\nBy Category:")
        for cat, count in stats['by_category'].items():
            print(f"  {cat}: {count}")
        print(f"\nMost Used:")
        for item in stats['most_used']:
            print(f"  {item['term'][:50]}: {item['uses']} uses")
    
    elif args.get:
        category, modality, page = args.get
        vocab = manager.get_vocabulary_for_verse(category, modality, int(page))
        print(f"\nVocabulary for {category}/{modality} at page {page}:")
        for term in vocab:
            print(f"  • {term}")
    
    elif args.motif:
        suggestions = manager.suggest_vocabulary_for_motif(
            args.motif, ['visual', 'auditory', 'tactile'], 500
        )
        print(f"\nVocabulary suggestions for motif '{args.motif}':")
        for modality, terms in suggestions.items():
            print(f"\n  {modality.upper()}:")
            for term in terms:
                print(f"    • {term}")
    
    elif args.list_categories:
        print("\nAvailable Categories:")
        for category in SENSORY_CODEX:
            modalities = list(SENSORY_CODEX[category].keys())
            print(f"  {category}: {', '.join(modalities)}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
