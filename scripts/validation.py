#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Quality Assurance and Validation System
Comprehensive validation for invisibility, density, and content quality
"""

import sys
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import Counter
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# INVISIBILITY CHECKER
# ============================================================================

class InvisibilityChecker:
    """
    Verify that motifs and patterns remain invisible per Stratified Foundation System.
    "The foundation operates beneath the surface, supporting content generation 
    without becoming visible in the output."
    """
    
    # Words that indicate explicit pattern naming (should be avoided)
    EXPLICIT_PATTERN_WORDS = [
        'foreshadow', 'foreshadowing', 'prefigure', 'prefiguration',
        'type', 'antitype', 'typology', 'typological',
        'symbol', 'symbolic', 'symbolize', 'symbolism',
        'represent', 'representation', 'allegorize',
        'motif', 'pattern', 'echo', 'parallel'
    ]
    
    # Phrases that break invisibility
    EXPLICIT_PHRASES = [
        'this prefigures', 'this foreshadows', 'this is a type of',
        'as we will see', 'as we saw earlier', 'recall that',
        'this pattern', 'notice the parallel', 'the motif of',
        'symbolically represents', 'allegorically speaking'
    ]
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def check_text_invisibility(self, text: str) -> Dict[str, Any]:
        """Check if text maintains invisibility"""
        if not text:
            return {'passes': True, 'violations': [], 'score': 1.0}
        
        text_lower = text.lower()
        violations = []
        
        # Check for explicit pattern words
        for word in self.EXPLICIT_PATTERN_WORDS:
            if word in text_lower:
                violations.append({
                    'type': 'explicit_word',
                    'word': word,
                    'context': self._extract_context(text, word)
                })
        
        # Check for explicit phrases
        for phrase in self.EXPLICIT_PHRASES:
            if phrase in text_lower:
                violations.append({
                    'type': 'explicit_phrase',
                    'phrase': phrase,
                    'context': self._extract_context(text, phrase)
                })
        
        # Calculate score (1.0 = perfect invisibility)
        score = max(0.0, 1.0 - (len(violations) * 0.1))
        
        return {
            'passes': len(violations) == 0,
            'violations': violations,
            'score': score
        }
    
    def check_motif_variation(self, motif_id: int, new_vocabulary: List[str]) -> Dict[str, Any]:
        """
        Check if new activation has sufficient variation from previous.
        Per config: minimum 10% variation between activations.
        """
        # Get previous activations
        query = """
            SELECT vocabulary_used 
            FROM motif_activations 
            WHERE motif_id = %s 
            ORDER BY page_number DESC 
            LIMIT 3
        """
        previous = self.db.fetch_all(query, (motif_id,))
        
        if not previous:
            return {'passes': True, 'variation': 1.0, 'details': 'First activation'}
        
        # Calculate variation from most recent
        prev_vocab = set(previous[0].get('vocabulary_used') or [])
        new_vocab = set(new_vocabulary)
        
        if not prev_vocab:
            return {'passes': True, 'variation': 1.0, 'details': 'No previous vocabulary'}
        
        # Jaccard distance for variation
        intersection = len(prev_vocab & new_vocab)
        union = len(prev_vocab | new_vocab)
        similarity = intersection / union if union > 0 else 0
        variation = 1.0 - similarity
        
        threshold = config.orbital_resonance.minimum_variation_between_activations
        
        return {
            'passes': variation >= threshold,
            'variation': variation,
            'threshold': threshold,
            'previous_vocab': list(prev_vocab),
            'new_vocab': list(new_vocab),
            'shared_words': list(prev_vocab & new_vocab)
        }
    
    def _extract_context(self, text: str, target: str, window: int = 50) -> str:
        """Extract context around a target word/phrase"""
        idx = text.lower().find(target.lower())
        if idx == -1:
            return ""
        
        start = max(0, idx - window)
        end = min(len(text), idx + len(target) + window)
        
        context = text[start:end]
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        
        return context
    
    def verify_verse(self, verse_id: int) -> Dict[str, Any]:
        """Run full invisibility verification on a verse"""
        verse = self.db.fetch_one("""
            SELECT * FROM verses WHERE id = %s
        """, (verse_id,))
        
        if not verse:
            return {'error': 'Verse not found'}
        
        results = {
            'verse_id': verse_id,
            'verse_reference': verse['verse_reference'],
            'checks': {}
        }
        
        # Check each text field
        text_fields = [
            'refined_explication', 'sense_literal', 'sense_allegorical',
            'sense_tropological', 'sense_anagogical'
        ]
        
        all_pass = True
        for field in text_fields:
            if verse.get(field):
                check = self.check_text_invisibility(verse[field])
                results['checks'][field] = check
                if not check['passes']:
                    all_pass = False
        
        results['passes'] = all_pass
        results['overall_score'] = sum(
            c['score'] for c in results['checks'].values()
        ) / len(results['checks']) if results['checks'] else 1.0
        
        return results


# ============================================================================
# THREAD DENSITY VALIDATOR
# ============================================================================

class ThreadDensityValidator:
    """
    Validate thread density stays within bounds (18-22).
    "Target: 18-22 active thread-points per 50-page span"
    """
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.config = config.thread_density
    
    def validate_page_range(self, start_page: int, end_page: int) -> Dict[str, Any]:
        """Validate density across a page range"""
        results = []
        
        for page in range(start_page, end_page + 1, 50):
            density = self._calculate_density_at_page(page)
            results.append({
                'page': page,
                'density': density['total'],
                'within_bounds': self.config.target_minimum <= density['total'] <= self.config.target_maximum,
                'breakdown': density['breakdown']
            })
        
        # Summary
        out_of_bounds = [r for r in results if not r['within_bounds']]
        
        return {
            'start_page': start_page,
            'end_page': end_page,
            'total_checkpoints': len(results),
            'passing': len(results) - len(out_of_bounds),
            'failing': len(out_of_bounds),
            'pass_rate': (len(results) - len(out_of_bounds)) / len(results) if results else 1.0,
            'violations': out_of_bounds,
            'details': results
        }
    
    def _calculate_density_at_page(self, page: int) -> Dict[str, Any]:
        """Calculate detailed density at a page"""
        breakdown = {}
        total = 0.0
        
        # Count by layer
        for layer in ['layer_one', 'layer_two', 'layer_three', 'layer_four', 'layer_five']:
            query = """
                SELECT COUNT(*) as count FROM motifs
                WHERE foundation_layer = %s
                AND %s BETWEEN planting_page AND convergence_page
            """
            result = self.db.fetch_one(query, (layer, page))
            count = result['count'] if result else 0
            
            weight = self.config.layer_weights.get(layer, 1.0)
            if layer == 'layer_four':
                weight = self.config.layer_weights.get('layer_four_approach', 1.0)
            elif layer == 'layer_five':
                weight = self.config.layer_weights.get('layer_five_resonance', 3.0)
            
            weighted = count * weight
            breakdown[layer] = {'count': count, 'weight': weight, 'weighted': weighted}
            total += weighted
        
        return {'total': total, 'breakdown': breakdown}
    
    def get_density_recommendations(self, page: int) -> List[str]:
        """Get recommendations for adjusting density at a page"""
        density = self._calculate_density_at_page(page)
        total = density['total']
        recommendations = []
        
        if total < self.config.target_minimum:
            deficit = self.config.target_minimum - total
            recommendations.append(f"Density is {deficit:.1f} below minimum.")
            recommendations.append("Consider: Activating dormant Layer 1-3 motifs")
            recommendations.append("Consider: Adding typological correspondence")
            recommendations.append("Consider: Introducing new short-arc motif")
        
        elif total > self.config.target_maximum:
            excess = total - self.config.target_maximum
            recommendations.append(f"Density is {excess:.1f} above maximum.")
            recommendations.append("Consider: Suspending lowest-priority active motif")
            recommendations.append("Consider: Extending motif arc to spread density")
            recommendations.append("Consider: Delaying approaching convergence")
        
        else:
            recommendations.append("Density is within optimal bounds.")
        
        return recommendations


# ============================================================================
# FOURFOLD SENSE VALIDATOR
# ============================================================================

class FourfoldSenseValidator:
    """Validate fourfold sense content quality"""
    
    MIN_LENGTH = 50
    MAX_LENGTH = 2000
    
    # Required elements per sense type
    SENSE_MARKERS = {
        'literal': ['context', 'meaning', 'text', 'passage', 'historical'],
        'allegorical': ['christ', 'type', 'fulfillment', 'prefigure', 'anticipate'],
        'tropological': ['moral', 'virtue', 'practice', 'formation', 'character'],
        'anagogical': ['heaven', 'eternal', 'eschatological', 'consummation', 'hope']
    }
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def validate_sense(self, sense_type: str, content: str) -> Dict[str, Any]:
        """Validate a single sense"""
        if not content:
            return {
                'valid': False,
                'errors': ['Content is empty'],
                'warnings': [],
                'score': 0.0
            }
        
        errors = []
        warnings = []
        
        # Length checks
        if len(content) < self.MIN_LENGTH:
            errors.append(f'Content too short ({len(content)} < {self.MIN_LENGTH})')
        if len(content) > self.MAX_LENGTH:
            warnings.append(f'Content may be too long ({len(content)} > {self.MAX_LENGTH})')
        
        # Check for sense-appropriate markers
        markers = self.SENSE_MARKERS.get(sense_type, [])
        content_lower = content.lower()
        found_markers = [m for m in markers if m in content_lower]
        
        if len(found_markers) < 2:
            warnings.append(f'Few {sense_type} sense markers found: {found_markers}')
        
        # Check for inappropriate content
        invisibility = InvisibilityChecker()
        invis_check = invisibility.check_text_invisibility(content)
        if not invis_check['passes']:
            for v in invis_check['violations']:
                warnings.append(f"Invisibility violation: {v['type']} - {v.get('word') or v.get('phrase')}")
        
        # Calculate score
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, min(1.0, score))
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': score,
            'length': len(content),
            'markers_found': found_markers
        }
    
    def validate_verse_senses(self, verse_id: int) -> Dict[str, Any]:
        """Validate all four senses for a verse"""
        verse = self.db.fetch_one("SELECT * FROM verses WHERE id = %s", (verse_id,))
        
        if not verse:
            return {'error': 'Verse not found'}
        
        results = {
            'verse_id': verse_id,
            'verse_reference': verse['verse_reference'],
            'senses': {}
        }
        
        sense_fields = {
            'literal': 'sense_literal',
            'allegorical': 'sense_allegorical',
            'tropological': 'sense_tropological',
            'anagogical': 'sense_anagogical'
        }
        
        all_valid = True
        total_score = 0.0
        
        for sense_type, field in sense_fields.items():
            content = verse.get(field)
            validation = self.validate_sense(sense_type, content)
            results['senses'][sense_type] = validation
            
            if not validation['valid']:
                all_valid = False
            total_score += validation['score']
        
        results['all_valid'] = all_valid
        results['average_score'] = total_score / 4
        
        return results


# ============================================================================
# CONTENT QUALITY ANALYZER
# ============================================================================

class ContentQualityAnalyzer:
    """Analyze overall content quality metrics"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
    
    def analyze_vocabulary_diversity(self, book_name: str = None) -> Dict[str, Any]:
        """Analyze vocabulary diversity across content"""
        query = """
            SELECT refined_explication FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.refined_explication IS NOT NULL
        """
        params = []
        
        if book_name:
            query += " AND cb.name = %s"
            params.append(book_name)
        
        verses = self.db.fetch_all(query, tuple(params) if params else None)
        
        # Collect all words
        all_words = []
        for verse in verses:
            text = verse['refined_explication'] or ''
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            all_words.extend(words)
        
        # Calculate metrics
        word_counts = Counter(all_words)
        unique_words = len(word_counts)
        total_words = len(all_words)
        
        # Type-token ratio
        ttr = unique_words / total_words if total_words > 0 else 0
        
        # Most common words
        most_common = word_counts.most_common(20)
        
        # Hapax legomena (words appearing only once)
        hapax = [w for w, c in word_counts.items() if c == 1]
        
        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'type_token_ratio': ttr,
            'hapax_legomena_count': len(hapax),
            'most_common_words': most_common,
            'verses_analyzed': len(verses)
        }
    
    def analyze_sense_balance(self) -> Dict[str, Any]:
        """Analyze balance of fourfold sense content"""
        query = """
            SELECT 
                AVG(LENGTH(COALESCE(sense_literal, ''))) as avg_literal,
                AVG(LENGTH(COALESCE(sense_allegorical, ''))) as avg_allegorical,
                AVG(LENGTH(COALESCE(sense_tropological, ''))) as avg_tropological,
                AVG(LENGTH(COALESCE(sense_anagogical, ''))) as avg_anagogical,
                COUNT(*) as total_verses,
                SUM(CASE WHEN sense_literal IS NOT NULL THEN 1 ELSE 0 END) as has_literal,
                SUM(CASE WHEN sense_allegorical IS NOT NULL THEN 1 ELSE 0 END) as has_allegorical,
                SUM(CASE WHEN sense_tropological IS NOT NULL THEN 1 ELSE 0 END) as has_tropological,
                SUM(CASE WHEN sense_anagogical IS NOT NULL THEN 1 ELSE 0 END) as has_anagogical
            FROM verses
        """
        result = self.db.fetch_one(query)
        
        if not result:
            return {'error': 'No data'}
        
        # Calculate expected weights
        expected = {
            'literal': config.fourfold_sense.literal_weight,
            'allegorical': config.fourfold_sense.allegorical_weight,
            'tropological': config.fourfold_sense.tropological_weight,
            'anagogical': config.fourfold_sense.anagogical_weight
        }
        
        # Calculate actual proportions
        total_length = (
            (result['avg_literal'] or 0) +
            (result['avg_allegorical'] or 0) +
            (result['avg_tropological'] or 0) +
            (result['avg_anagogical'] or 0)
        )
        
        actual = {}
        if total_length > 0:
            actual = {
                'literal': (result['avg_literal'] or 0) / total_length,
                'allegorical': (result['avg_allegorical'] or 0) / total_length,
                'tropological': (result['avg_tropological'] or 0) / total_length,
                'anagogical': (result['avg_anagogical'] or 0) / total_length
            }
        
        return {
            'average_lengths': {
                'literal': result['avg_literal'],
                'allegorical': result['avg_allegorical'],
                'tropological': result['avg_tropological'],
                'anagogical': result['avg_anagogical']
            },
            'completion_rates': {
                'literal': result['has_literal'] / result['total_verses'] if result['total_verses'] else 0,
                'allegorical': result['has_allegorical'] / result['total_verses'] if result['total_verses'] else 0,
                'tropological': result['has_tropological'] / result['total_verses'] if result['total_verses'] else 0,
                'anagogical': result['has_anagogical'] / result['total_verses'] if result['total_verses'] else 0
            },
            'expected_weights': expected,
            'actual_weights': actual,
            'total_verses': result['total_verses']
        }


# ============================================================================
# MASTER VALIDATION ORCHESTRATOR
# ============================================================================

class ValidationOrchestrator:
    """Orchestrate all validation checks"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.invisibility = InvisibilityChecker(self.db)
        self.density = ThreadDensityValidator(self.db)
        self.fourfold = FourfoldSenseValidator(self.db)
        self.quality = ContentQualityAnalyzer(self.db)
    
    def run_full_validation(self, sample_size: int = 100) -> Dict[str, Any]:
        """Run comprehensive validation suite"""
        logger.info("Starting full validation...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # 1. Invisibility check on sample
        logger.info("Checking invisibility...")
        sample_verses = self.db.fetch_all("""
            SELECT id FROM verses 
            WHERE refined_explication IS NOT NULL 
            ORDER BY RANDOM() 
            LIMIT %s
        """, (sample_size,))
        
        invis_results = []
        for verse in sample_verses:
            check = self.invisibility.verify_verse(verse['id'])
            invis_results.append(check)
        
        passing = sum(1 for r in invis_results if r.get('passes', False))
        results['checks']['invisibility'] = {
            'sample_size': len(invis_results),
            'passing': passing,
            'pass_rate': passing / len(invis_results) if invis_results else 1.0,
            'average_score': sum(r.get('overall_score', 0) for r in invis_results) / len(invis_results) if invis_results else 0
        }
        
        # 2. Thread density validation
        logger.info("Validating thread density...")
        density_check = self.density.validate_page_range(0, 2500)
        results['checks']['thread_density'] = {
            'checkpoints': density_check['total_checkpoints'],
            'passing': density_check['passing'],
            'pass_rate': density_check['pass_rate'],
            'violations': len(density_check['violations'])
        }
        
        # 3. Fourfold sense validation on sample
        logger.info("Validating fourfold senses...")
        fourfold_results = []
        for verse in sample_verses[:50]:  # Smaller sample for detailed check
            check = self.fourfold.validate_verse_senses(verse['id'])
            if 'error' not in check:
                fourfold_results.append(check)
        
        valid_count = sum(1 for r in fourfold_results if r.get('all_valid', False))
        results['checks']['fourfold_sense'] = {
            'sample_size': len(fourfold_results),
            'fully_valid': valid_count,
            'validity_rate': valid_count / len(fourfold_results) if fourfold_results else 0,
            'average_score': sum(r.get('average_score', 0) for r in fourfold_results) / len(fourfold_results) if fourfold_results else 0
        }
        
        # 4. Content quality analysis
        logger.info("Analyzing content quality...")
        vocab_analysis = self.quality.analyze_vocabulary_diversity()
        sense_balance = self.quality.analyze_sense_balance()
        
        results['checks']['content_quality'] = {
            'vocabulary_diversity': vocab_analysis['type_token_ratio'],
            'unique_words': vocab_analysis['unique_words'],
            'sense_balance': sense_balance['actual_weights']
        }
        
        # Overall assessment
        all_pass_rates = [
            results['checks']['invisibility']['pass_rate'],
            results['checks']['thread_density']['pass_rate'],
            results['checks']['fourfold_sense']['validity_rate']
        ]
        
        results['overall'] = {
            'average_pass_rate': sum(all_pass_rates) / len(all_pass_rates),
            'status': 'PASS' if all(r >= 0.9 for r in all_pass_rates) else 'NEEDS_ATTENTION'
        }
        
        logger.info(f"Validation complete. Status: {results['overall']['status']}")
        return results


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Validation System')
    parser.add_argument('--full', action='store_true', help='Run full validation')
    parser.add_argument('--invisibility', action='store_true', help='Check invisibility')
    parser.add_argument('--density', action='store_true', help='Check thread density')
    parser.add_argument('--verse-id', type=int, help='Validate specific verse')
    parser.add_argument('--page', type=int, help='Check density at page')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    from scripts.database import init_db
    if not init_db():
        print("Failed to initialize database")
        return 1
    
    orchestrator = ValidationOrchestrator()
    
    if args.full:
        results = orchestrator.run_full_validation()
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)
        for check_name, check_data in results['checks'].items():
            print(f"\n{check_name.upper()}:")
            for key, value in check_data.items():
                print(f"  {key}: {value}")
        print(f"\nOVERALL STATUS: {results['overall']['status']}")
        print("=" * 60)
    
    elif args.verse_id:
        result = orchestrator.invisibility.verify_verse(args.verse_id)
        print(f"\nVerse {args.verse_id}: {'PASS' if result.get('passes') else 'FAIL'}")
        if result.get('checks'):
            for field, check in result['checks'].items():
                status = '✓' if check['passes'] else '✗'
                print(f"  {status} {field}: score={check['score']:.2f}")
    
    elif args.page:
        recommendations = orchestrator.density.get_density_recommendations(args.page)
        print(f"\nDensity at page {args.page}:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
