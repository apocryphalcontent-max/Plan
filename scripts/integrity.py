#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ System Integrity Module
Validates data quality, ensures consistency, and maintains system health.
Every operation is justified. Every check earns its place.
"""

import sys
import logging
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Issue severity levels."""
    CRITICAL = 1  # System cannot function
    ERROR = 2     # Data corruption or loss
    WARNING = 3   # Suboptimal but functional
    INFO = 4      # Informational only


@dataclass
class IntegrityIssue:
    """A single integrity issue."""
    severity: Severity
    category: str
    message: str
    affected_item: str
    suggestion: str = ""


@dataclass
class IntegrityReport:
    """Complete integrity check report."""
    timestamp: datetime
    issues: List[IntegrityIssue] = field(default_factory=list)
    checks_run: int = 0
    checks_passed: int = 0
    
    @property
    def health_score(self) -> float:
        """Calculate system health score (0.0 to 1.0)."""
        if self.checks_run == 0:
            return 1.0
        
        # Weight issues by severity
        penalty = 0.0
        for issue in self.issues:
            if issue.severity == Severity.CRITICAL:
                penalty += 0.25
            elif issue.severity == Severity.ERROR:
                penalty += 0.10
            elif issue.severity == Severity.WARNING:
                penalty += 0.02
        
        return max(0.0, 1.0 - penalty)
    
    @property
    def is_healthy(self) -> bool:
        """Check if system is healthy (no critical/error issues)."""
        return not any(i.severity in (Severity.CRITICAL, Severity.ERROR) for i in self.issues)


# ============================================================================
# VERSE REFERENCE VALIDATOR
# ============================================================================

class VerseReferenceValidator:
    """Validate verse reference format and existence."""
    
    # Canonical book names with chapter counts
    BOOK_CHAPTERS = {
        'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36,
        'Deuteronomy': 34, 'Joshua': 24, 'Judges': 21, 'Ruth': 4,
        '1 Samuel': 31, '2 Samuel': 24, '1 Kings': 22, '2 Kings': 25,
        '1 Chronicles': 29, '2 Chronicles': 36, 'Ezra': 10, 'Nehemiah': 13,
        'Esther': 10, 'Job': 42, 'Psalms': 150, 'Proverbs': 31,
        'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66,
        'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12,
        'Hosea': 14, 'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4,
        'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3,
        'Haggai': 2, 'Zechariah': 14, 'Malachi': 4,
        # Deuterocanonical
        'Tobit': 14, 'Judith': 16, 'Wisdom': 19, 'Sirach': 51,
        'Baruch': 6, '1 Maccabees': 16, '2 Maccabees': 15,
        # New Testament
        'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21,
        'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13,
        'Galatians': 6, 'Ephesians': 6, 'Philippians': 4, 'Colossians': 4,
        '1 Thessalonians': 5, '2 Thessalonians': 3, '1 Timothy': 6,
        '2 Timothy': 4, 'Titus': 3, 'Philemon': 1, 'Hebrews': 13,
        'James': 5, '1 Peter': 5, '2 Peter': 3, '1 John': 5,
        '2 John': 1, '3 John': 1, 'Jude': 1, 'Revelation': 22,
    }
    
    # Reference pattern: "Book Chapter:Verse" or "1 Book Chapter:Verse"
    REFERENCE_PATTERN = re.compile(
        r'^(\d?\s?[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+):(\d+)(?:-(\d+))?$'
    )
    
    def validate_reference(self, ref: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a verse reference.
        Returns (is_valid, error_message).
        """
        if not ref or not ref.strip():
            return False, "Empty reference"
        
        match = self.REFERENCE_PATTERN.match(ref.strip())
        if not match:
            return False, f"Invalid format: {ref}"
        
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))
        
        # Check book exists
        if book not in self.BOOK_CHAPTERS:
            # Try case-insensitive match
            book_lower = book.lower()
            found = None
            for canonical in self.BOOK_CHAPTERS:
                if canonical.lower() == book_lower:
                    found = canonical
                    break
            if not found:
                return False, f"Unknown book: {book}"
            book = found
        
        # Check chapter range
        max_chapters = self.BOOK_CHAPTERS[book]
        if chapter < 1 or chapter > max_chapters:
            return False, f"{book} has {max_chapters} chapters, not {chapter}"
        
        # Verse validation (basic - just check positive)
        if verse < 1:
            return False, f"Invalid verse number: {verse}"
        
        return True, None
    
    def normalize_reference(self, ref: str) -> Optional[str]:
        """Normalize a reference to canonical format."""
        match = self.REFERENCE_PATTERN.match(ref.strip())
        if not match:
            return None
        
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))
        
        # Normalize book name
        for canonical in self.BOOK_CHAPTERS:
            if canonical.lower() == book.lower():
                book = canonical
                break
        
        return f"{book} {chapter}:{verse}"


# ============================================================================
# TEXT QUALITY VALIDATOR
# ============================================================================

class TextQualityValidator:
    """Validate text quality for verses and commentary."""
    
    # Minimum lengths for different content types
    MIN_LENGTHS = {
        'verse_text': 10,
        'sense_literal': 50,
        'sense_allegorical': 50,
        'sense_tropological': 50,
        'sense_anagogical': 50,
        'refined_explication': 100,
        'patristic_commentary': 30,
    }
    
    # Suspicious patterns that might indicate bad data
    SUSPICIOUS_PATTERNS = [
        (r'\[Text not found\]', 'Placeholder text'),
        (r'TODO|FIXME|XXX', 'Unfinished marker'),
        (r'Lorem ipsum', 'Placeholder text'),
        (r'<[^>]+>', 'HTML tags in text'),
        (r'\{\{[^}]+\}\}', 'Template markers'),
        (r'undefined|null|None', 'Programming artifacts'),
    ]
    
    def validate_text(self, text: str, content_type: str) -> List[IntegrityIssue]:
        """Validate text quality."""
        issues = []
        
        if not text:
            issues.append(IntegrityIssue(
                severity=Severity.WARNING,
                category='text_quality',
                message=f"Empty {content_type}",
                affected_item=content_type,
                suggestion="Provide content or mark as pending"
            ))
            return issues
        
        # Check minimum length
        min_len = self.MIN_LENGTHS.get(content_type, 10)
        if len(text) < min_len:
            issues.append(IntegrityIssue(
                severity=Severity.WARNING,
                category='text_quality',
                message=f"{content_type} too short ({len(text)} < {min_len})",
                affected_item=text[:50],
                suggestion="Expand content"
            ))
        
        # Check for suspicious patterns
        for pattern, description in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(IntegrityIssue(
                    severity=Severity.WARNING,
                    category='text_quality',
                    message=f"{description} found in {content_type}",
                    affected_item=text[:50],
                    suggestion="Review and clean text"
                ))
        
        return issues


# ============================================================================
# DATABASE INTEGRITY CHECKER
# ============================================================================

class DatabaseIntegrityChecker:
    """Check database integrity and consistency."""
    
    def __init__(self, db=None):
        self.db = db
    
    def check_foreign_keys(self) -> List[IntegrityIssue]:
        """Check foreign key integrity."""
        issues = []
        
        if not self.db:
            return issues
        
        # Check verses have valid book_id
        try:
            orphan_verses = self.db.fetch_all("""
                SELECT v.id, v.verse_reference 
                FROM verses v
                LEFT JOIN canonical_books cb ON v.book_id = cb.id
                WHERE cb.id IS NULL
            """)
            
            for verse in orphan_verses:
                issues.append(IntegrityIssue(
                    severity=Severity.ERROR,
                    category='foreign_key',
                    message="Verse with invalid book_id",
                    affected_item=f"Verse ID {verse['id']}",
                    suggestion="Delete or reassign verse"
                ))
        except Exception as e:
            logger.debug(f"FK check failed: {e}")
        
        return issues
    
    def check_duplicates(self) -> List[IntegrityIssue]:
        """Check for duplicate entries."""
        issues = []
        
        if not self.db:
            return issues
        
        try:
            # Check duplicate verse references
            duplicates = self.db.fetch_all("""
                SELECT verse_reference, COUNT(*) as cnt
                FROM verses
                GROUP BY verse_reference
                HAVING COUNT(*) > 1
            """)
            
            for dup in duplicates:
                issues.append(IntegrityIssue(
                    severity=Severity.ERROR,
                    category='duplicate',
                    message=f"Duplicate verse reference ({dup['cnt']} copies)",
                    affected_item=dup['verse_reference'],
                    suggestion="Remove duplicates"
                ))
        except Exception as e:
            logger.debug(f"Duplicate check failed: {e}")
        
        return issues
    
    def check_status_consistency(self) -> List[IntegrityIssue]:
        """Check verse status consistency."""
        issues = []
        
        if not self.db:
            return issues
        
        try:
            # Refined verses should have all senses
            incomplete = self.db.fetch_all("""
                SELECT id, verse_reference, status
                FROM verses
                WHERE status = 'refined'
                AND (sense_literal IS NULL 
                     OR sense_allegorical IS NULL
                     OR sense_tropological IS NULL
                     OR sense_anagogical IS NULL)
            """)
            
            for verse in incomplete:
                issues.append(IntegrityIssue(
                    severity=Severity.WARNING,
                    category='status_consistency',
                    message="Refined verse missing senses",
                    affected_item=verse['verse_reference'],
                    suggestion="Complete all four senses or reset status"
                ))
        except Exception as e:
            logger.debug(f"Status check failed: {e}")
        
        return issues


# ============================================================================
# MOTIF INTEGRITY CHECKER
# ============================================================================

class MotifIntegrityChecker:
    """Check motif configuration integrity."""
    
    def __init__(self, db=None):
        self.db = db
    
    def check_orbital_bounds(self) -> List[IntegrityIssue]:
        """Check motif orbital positions are valid."""
        issues = []
        
        if not self.db:
            return issues
        
        try:
            motifs = self.db.fetch_all("""
                SELECT name, planting_page, convergence_page
                FROM motifs
            """)
            
            for motif in motifs:
                # Convergence should be after planting
                if motif['convergence_page'] <= motif['planting_page']:
                    issues.append(IntegrityIssue(
                        severity=Severity.ERROR,
                        category='motif_bounds',
                        message="Convergence before planting",
                        affected_item=motif['name'],
                        suggestion="Fix page ordering"
                    ))
                
                # Check reasonable bounds
                if motif['planting_page'] < 1:
                    issues.append(IntegrityIssue(
                        severity=Severity.ERROR,
                        category='motif_bounds',
                        message="Invalid planting page",
                        affected_item=motif['name'],
                        suggestion="Set positive page number"
                    ))
        except Exception as e:
            logger.debug(f"Motif check failed: {e}")
        
        return issues
    
    def check_thread_density_config(self) -> List[IntegrityIssue]:
        """Verify thread density configuration is valid."""
        issues = []
        
        try:
            from config.settings import config
            td = config.thread_density
            
            if td.target_minimum >= td.target_maximum:
                issues.append(IntegrityIssue(
                    severity=Severity.ERROR,
                    category='config',
                    message="Thread density min >= max",
                    affected_item='thread_density',
                    suggestion="Fix target bounds in config"
                ))
            
            if td.target_minimum < 0:
                issues.append(IntegrityIssue(
                    severity=Severity.ERROR,
                    category='config',
                    message="Negative thread density minimum",
                    affected_item='thread_density',
                    suggestion="Set non-negative minimum"
                ))
        except Exception as e:
            logger.debug(f"Config check failed: {e}")
        
        return issues


# ============================================================================
# MASTER INTEGRITY CHECKER
# ============================================================================

class SystemIntegrityChecker:
    """
    Master integrity checker coordinating all validation.
    Run this to get a complete system health report.
    """
    
    def __init__(self, db=None):
        self.db = db
        self.ref_validator = VerseReferenceValidator()
        self.text_validator = TextQualityValidator()
        self.db_checker = DatabaseIntegrityChecker(db)
        self.motif_checker = MotifIntegrityChecker(db)
    
    def run_full_check(self) -> IntegrityReport:
        """Run all integrity checks and return comprehensive report."""
        report = IntegrityReport(timestamp=datetime.now())
        
        # Database checks
        report.checks_run += 1
        issues = self.db_checker.check_foreign_keys()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        report.checks_run += 1
        issues = self.db_checker.check_duplicates()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        report.checks_run += 1
        issues = self.db_checker.check_status_consistency()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        # Motif checks
        report.checks_run += 1
        issues = self.motif_checker.check_orbital_bounds()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        report.checks_run += 1
        issues = self.motif_checker.check_thread_density_config()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        # Offline data checks
        report.checks_run += 1
        issues = self._check_offline_data()
        report.issues.extend(issues)
        if not issues:
            report.checks_passed += 1
        
        return report
    
    def _check_offline_data(self) -> List[IntegrityIssue]:
        """Check offline data modules are available and valid."""
        issues = []
        
        # Check offline Bible provider
        try:
            from data.offline_bible import get_offline_provider
            provider = get_offline_provider()
            stats = provider.get_statistics()
            
            if stats['total_verses'] < 100:
                issues.append(IntegrityIssue(
                    severity=Severity.WARNING,
                    category='offline_data',
                    message=f"Low offline verse count: {stats['total_verses']}",
                    affected_item='offline_bible',
                    suggestion="Add more verses to offline database"
                ))
        except ImportError:
            issues.append(IntegrityIssue(
                severity=Severity.WARNING,
                category='offline_data',
                message="Offline Bible provider not available",
                affected_item='offline_bible',
                suggestion="Check data/offline_bible.py exists"
            ))
        except Exception as e:
            issues.append(IntegrityIssue(
                severity=Severity.ERROR,
                category='offline_data',
                message=f"Offline Bible error: {e}",
                affected_item='offline_bible',
                suggestion="Fix offline_bible.py"
            ))
        
        # Check patristic database
        try:
            from data.patristic_data import get_patristic_database
            db = get_patristic_database()
            stats = db.get_statistics()
            
            if stats['total_entries'] < 10:
                issues.append(IntegrityIssue(
                    severity=Severity.WARNING,
                    category='offline_data',
                    message=f"Low patristic entry count: {stats['total_entries']}",
                    affected_item='patristic_data',
                    suggestion="Add more patristic commentary"
                ))
        except ImportError:
            issues.append(IntegrityIssue(
                severity=Severity.WARNING,
                category='offline_data',
                message="Patristic database not available",
                affected_item='patristic_data',
                suggestion="Check data/patristic_data.py exists"
            ))
        except Exception as e:
            issues.append(IntegrityIssue(
                severity=Severity.ERROR,
                category='offline_data',
                message=f"Patristic database error: {e}",
                affected_item='patristic_data',
                suggestion="Fix patristic_data.py"
            ))
        
        # Check liturgical calendar
        try:
            from data.liturgical_calendar import get_liturgical_calendar
            cal = get_liturgical_calendar()
            # Quick sanity check
            from datetime import date
            day = cal.get_liturgical_day(date.today())
            if not day.season:
                issues.append(IntegrityIssue(
                    severity=Severity.ERROR,
                    category='offline_data',
                    message="Liturgical calendar returning invalid data",
                    affected_item='liturgical_calendar',
                    suggestion="Check calendar calculations"
                ))
        except ImportError:
            issues.append(IntegrityIssue(
                severity=Severity.WARNING,
                category='offline_data',
                message="Liturgical calendar not available",
                affected_item='liturgical_calendar',
                suggestion="Check data/liturgical_calendar.py exists"
            ))
        except Exception as e:
            issues.append(IntegrityIssue(
                severity=Severity.ERROR,
                category='offline_data',
                message=f"Liturgical calendar error: {e}",
                affected_item='liturgical_calendar',
                suggestion="Fix liturgical_calendar.py"
            ))
        
        return issues
    
    def validate_verse_reference(self, ref: str) -> Tuple[bool, Optional[str]]:
        """Validate a single verse reference."""
        return self.ref_validator.validate_reference(ref)
    
    def normalize_verse_reference(self, ref: str) -> Optional[str]:
        """Normalize a verse reference to canonical format."""
        return self.ref_validator.normalize_reference(ref)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for integrity checking."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ System Integrity Checker')
    parser.add_argument('--full', action='store_true', help='Run full integrity check')
    parser.add_argument('--validate-ref', type=str, help='Validate a verse reference')
    parser.add_argument('--normalize-ref', type=str, help='Normalize a verse reference')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Try to get database connection
    db = None
    try:
        from scripts.database import init_db, get_db
        if init_db():
            db = get_db()
    except Exception as e:
        logger.debug(f"Database not available: {e}")
    
    checker = SystemIntegrityChecker(db)
    
    if args.full:
        report = checker.run_full_check()
        
        print("\n" + "=" * 60)
        print("ΒΊΒΛΟΣ ΛΌΓΟΥ SYSTEM INTEGRITY REPORT")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print(f"Checks Run: {report.checks_run}")
        print(f"Checks Passed: {report.checks_passed}")
        print(f"Health Score: {report.health_score:.1%}")
        print(f"Status: {'HEALTHY' if report.is_healthy else 'ISSUES FOUND'}")
        
        if report.issues:
            print("\nISSUES:")
            print("-" * 60)
            
            # Group by severity
            for severity in Severity:
                severity_issues = [i for i in report.issues if i.severity == severity]
                if severity_issues:
                    print(f"\n{severity.name}:")
                    for issue in severity_issues:
                        print(f"  [{issue.category}] {issue.message}")
                        print(f"    Affected: {issue.affected_item}")
                        if issue.suggestion:
                            print(f"    Suggestion: {issue.suggestion}")
        else:
            print("\n✓ All checks passed!")
        
        return 0 if report.is_healthy else 1
    
    elif args.validate_ref:
        is_valid, error = checker.validate_verse_reference(args.validate_ref)
        if is_valid:
            print(f"✓ Valid: {args.validate_ref}")
        else:
            print(f"✗ Invalid: {error}")
        return 0 if is_valid else 1
    
    elif args.normalize_ref:
        normalized = checker.normalize_verse_reference(args.normalize_ref)
        if normalized:
            print(f"Normalized: {normalized}")
        else:
            print(f"Could not normalize: {args.normalize_ref}")
        return 0 if normalized else 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
