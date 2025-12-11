#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Liturgical Calendar System
Orthodox liturgical calendar integration for anagogical sense processing
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import date, datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


class LiturgicalSeason(Enum):
    """Orthodox liturgical seasons"""
    TRIODION = "triodion"                    # Pre-Lenten
    GREAT_LENT = "great_lent"                # 40 days before Pascha
    HOLY_WEEK = "holy_week"                  # Week before Pascha
    PASCHA = "pascha"                        # Resurrection
    BRIGHT_WEEK = "bright_week"              # Week after Pascha
    PENTECOSTARION = "pentecostarion"        # Pascha to Pentecost
    PENTECOST = "pentecost"                  # Descent of Holy Spirit
    APOSTLES_FAST = "apostles_fast"          # After Pentecost
    DORMITION_FAST = "dormition_fast"        # August 1-14
    NATIVITY_FAST = "nativity_fast"          # Nov 15 - Dec 24
    NATIVITY = "nativity"                    # Christmas season
    THEOPHANY = "theophany"                  # January 6 season
    ORDINARY = "ordinary"                    # Regular time


class FeastRank(Enum):
    """Ranking of feast days"""
    GREAT_FEAST = 1          # 12 Great Feasts
    FEAST_OF_LORD = 2        # Feasts of the Lord
    THEOTOKOS_FEAST = 3      # Feasts of Theotokos
    MAJOR_SAINT = 4          # Major Saints
    MINOR_SAINT = 5          # Minor commemorations
    ORDINARY = 6             # Regular days


@dataclass
class LiturgicalDay:
    """Represents a single liturgical day"""
    date: date
    season: LiturgicalSeason
    feast_rank: FeastRank
    feast_name: Optional[str] = None
    gospel_readings: List[str] = field(default_factory=list)
    epistle_readings: List[str] = field(default_factory=list)
    old_testament_readings: List[str] = field(default_factory=list)
    tone: int = 1  # 1-8 Octoechos
    fasting: str = "none"  # none, wine_oil, fish, strict
    commemoration: Optional[str] = None


# ============================================================================
# PASCHA CALCULATION (Computus)
# ============================================================================

def calculate_orthodox_pascha(year: int) -> date:
    """
    Calculate Orthodox Pascha (Easter) using the Julian calendar computation
    then convert to Gregorian date.
    
    Uses the Meeus/Jones/Butcher algorithm for Julian Easter.
    """
    # Julian Easter calculation
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    
    # Julian date
    julian_date = date(year, month, day)
    
    # Convert to Gregorian (add 13 days for 20th-21st century)
    # Adjustment varies by century
    if year >= 1900 and year < 2100:
        gregorian_adjustment = 13
    elif year >= 2100 and year < 2200:
        gregorian_adjustment = 14
    else:
        gregorian_adjustment = 13  # Default
    
    return julian_date + timedelta(days=gregorian_adjustment)


# ============================================================================
# GREAT FEASTS OF THE ORTHODOX CHURCH
# ============================================================================

GREAT_FEASTS = {
    # Fixed feasts (month, day)
    (9, 8): {
        'name': 'Nativity of the Theotokos',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 10:38-42', 'Luke 11:27-28'],
            'epistle': ['Philippians 2:5-11'],
        }
    },
    (9, 14): {
        'name': 'Exaltation of the Holy Cross',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['John 19:6-11', 'John 19:13-20', 'John 19:25-28', 'John 19:30-35'],
            'epistle': ['1 Corinthians 1:18-24'],
        }
    },
    (11, 21): {
        'name': 'Entry of the Theotokos into the Temple',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 10:38-42', 'Luke 11:27-28'],
            'epistle': ['Hebrews 9:1-7'],
        }
    },
    (12, 25): {
        'name': 'Nativity of Christ',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Matthew 2:1-12'],
            'epistle': ['Galatians 4:4-7'],
        }
    },
    (1, 6): {
        'name': 'Theophany (Baptism of Christ)',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Matthew 3:13-17'],
            'epistle': ['Titus 2:11-14', 'Titus 3:4-7'],
        }
    },
    (2, 2): {
        'name': 'Meeting of the Lord (Presentation)',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 2:22-40'],
            'epistle': ['Hebrews 7:7-17'],
        }
    },
    (3, 25): {
        'name': 'Annunciation',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 1:24-38'],
            'epistle': ['Hebrews 2:11-18'],
        }
    },
    (8, 6): {
        'name': 'Transfiguration',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Matthew 17:1-9'],
            'epistle': ['2 Peter 1:10-19'],
        }
    },
    (8, 15): {
        'name': 'Dormition of the Theotokos',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 10:38-42', 'Luke 11:27-28'],
            'epistle': ['Philippians 2:5-11'],
        }
    },
}

# Moveable feasts (days relative to Pascha)
MOVEABLE_FEASTS = {
    -7: {
        'name': 'Palm Sunday (Entry into Jerusalem)',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['John 12:1-18'],
            'epistle': ['Philippians 4:4-9'],
        }
    },
    0: {
        'name': 'Pascha (Resurrection)',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['John 1:1-17'],
            'epistle': ['Acts 1:1-8'],
        }
    },
    39: {
        'name': 'Ascension',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['Luke 24:36-53'],
            'epistle': ['Acts 1:1-12'],
        }
    },
    49: {
        'name': 'Pentecost',
        'rank': FeastRank.GREAT_FEAST,
        'readings': {
            'gospel': ['John 7:37-52', 'John 8:12'],
            'epistle': ['Acts 2:1-11'],
        }
    },
}


# ============================================================================
# HOLY WEEK READINGS
# ============================================================================

HOLY_WEEK_READINGS = {
    -6: {  # Holy Monday
        'name': 'Holy Monday',
        'gospel': ['Matthew 21:18-43'],
        'theme': 'Cursing of the fig tree; cleansing of temple'
    },
    -5: {  # Holy Tuesday
        'name': 'Holy Tuesday',
        'gospel': ['Matthew 22:15-46', 'Matthew 23:1-39'],
        'theme': 'Parables; denunciation of Pharisees'
    },
    -4: {  # Holy Wednesday
        'name': 'Holy Wednesday',
        'gospel': ['Matthew 26:6-16'],
        'theme': 'Anointing at Bethany; Judas agreement'
    },
    -3: {  # Holy Thursday
        'name': 'Holy Thursday',
        'gospel': ['Matthew 26:1-20', 'John 13:3-17', 'Matthew 26:21-39'],
        'theme': 'Mystical Supper; washing of feet; Gethsemane'
    },
    -2: {  # Holy Friday
        'name': 'Holy Friday',
        'gospel': ['John 18:1-28', 'John 18:28-40', 'John 19:1-37', 'Matthew 27:1-56'],
        'theme': 'Passion and Crucifixion'
    },
    -1: {  # Holy Saturday
        'name': 'Holy Saturday',
        'gospel': ['Matthew 28:1-20'],
        'theme': 'Descent into Hades; Resurrection'
    },
}


# ============================================================================
# LECTIONARY - GOSPEL READINGS BY WEEK
# ============================================================================

GOSPEL_LECTIONARY = {
    # Post-Pascha readings (weeks after Pascha)
    'pascha_1': {'gospel': 'John 1:1-17', 'theme': 'Prologue - Word made flesh'},
    'pascha_2': {'gospel': 'John 20:19-31', 'theme': 'Thomas Sunday'},
    'pascha_3': {'gospel': 'Mark 15:43-47', 'theme': 'Myrrh-bearing Women'},
    'pascha_4': {'gospel': 'John 5:1-15', 'theme': 'Paralytic at Bethesda'},
    'pascha_5': {'gospel': 'John 4:5-42', 'theme': 'Samaritan Woman'},
    'pascha_6': {'gospel': 'John 9:1-38', 'theme': 'Man Born Blind'},
    'pascha_7': {'gospel': 'John 17:1-13', 'theme': 'High Priestly Prayer'},
    
    # Matthew lectionary (weeks after Pentecost)
    'matthew_1': {'gospel': 'Matthew 10:32-33', 'theme': 'All Saints'},
    'matthew_2': {'gospel': 'Matthew 4:18-23', 'theme': 'Calling of disciples'},
    'matthew_3': {'gospel': 'Matthew 6:22-33', 'theme': 'Eye is lamp; seek first kingdom'},
    'matthew_4': {'gospel': 'Matthew 8:5-13', 'theme': 'Centurion faith'},
    'matthew_5': {'gospel': 'Matthew 8:28-34', 'theme': 'Gadarene demoniacs'},
    'matthew_6': {'gospel': 'Matthew 9:1-8', 'theme': 'Paralytic forgiven'},
    'matthew_7': {'gospel': 'Matthew 9:27-35', 'theme': 'Two blind men'},
    'matthew_8': {'gospel': 'Matthew 14:14-22', 'theme': 'Feeding 5000'},
    'matthew_9': {'gospel': 'Matthew 14:22-34', 'theme': 'Walking on water'},
    'matthew_10': {'gospel': 'Matthew 17:14-23', 'theme': 'Epileptic boy'},
    'matthew_11': {'gospel': 'Matthew 18:23-35', 'theme': 'Unforgiving servant'},
    
    # Luke lectionary
    'luke_1': {'gospel': 'Luke 5:1-11', 'theme': 'Miraculous catch'},
    'luke_2': {'gospel': 'Luke 6:31-36', 'theme': 'Love your enemies'},
    'luke_3': {'gospel': 'Luke 7:11-16', 'theme': 'Widow of Nain'},
    'luke_4': {'gospel': 'Luke 8:5-15', 'theme': 'Parable of sower'},
    'luke_5': {'gospel': 'Luke 16:19-31', 'theme': 'Rich man and Lazarus'},
    'luke_6': {'gospel': 'Luke 8:26-39', 'theme': 'Gerasene demoniac'},
    'luke_7': {'gospel': 'Luke 8:41-56', 'theme': 'Jairus daughter'},
    'luke_8': {'gospel': 'Luke 10:25-37', 'theme': 'Good Samaritan'},
    'luke_9': {'gospel': 'Luke 12:16-21', 'theme': 'Rich fool'},
    'luke_10': {'gospel': 'Luke 13:10-17', 'theme': 'Bent woman'},
}


# ============================================================================
# LITURGICAL CALENDAR CLASS
# ============================================================================

class LiturgicalCalendar:
    """
    Complete Orthodox liturgical calendar system.
    Calculates seasons, feasts, readings for any date.
    """
    
    def __init__(self, year: int = None):
        self.year = year or datetime.now().year
        self._pascha_cache: Dict[int, date] = {}
        self._initialize_year(self.year)
    
    def _initialize_year(self, year: int):
        """Pre-calculate key dates for a year."""
        self.pascha = self._get_pascha(year)
        
        # Key dates relative to Pascha
        self.clean_monday = self.pascha - timedelta(days=48)
        self.palm_sunday = self.pascha - timedelta(days=7)
        self.holy_week_start = self.pascha - timedelta(days=6)
        self.bright_week_end = self.pascha + timedelta(days=7)
        self.ascension = self.pascha + timedelta(days=39)
        self.pentecost = self.pascha + timedelta(days=49)
    
    def _get_pascha(self, year: int) -> date:
        """Get Pascha date with caching."""
        if year not in self._pascha_cache:
            self._pascha_cache[year] = calculate_orthodox_pascha(year)
        return self._pascha_cache[year]
    
    def get_season(self, d: date) -> LiturgicalSeason:
        """Determine liturgical season for a date."""
        # Ensure we have the right year's calculations
        if d.year != self.year:
            self._initialize_year(d.year)
        
        days_from_pascha = (d - self.pascha).days
        
        # Check for specific seasons
        if days_from_pascha == 0:
            return LiturgicalSeason.PASCHA
        elif 1 <= days_from_pascha <= 7:
            return LiturgicalSeason.BRIGHT_WEEK
        elif days_from_pascha == 49:
            return LiturgicalSeason.PENTECOST
        elif 1 <= days_from_pascha <= 49:
            return LiturgicalSeason.PENTECOSTARION
        elif -6 <= days_from_pascha <= -1:
            return LiturgicalSeason.HOLY_WEEK
        elif -48 <= days_from_pascha <= -7:
            return LiturgicalSeason.GREAT_LENT
        elif -70 <= days_from_pascha <= -49:
            return LiturgicalSeason.TRIODION
        
        # Fixed seasons
        if d.month == 8 and 1 <= d.day <= 14:
            return LiturgicalSeason.DORMITION_FAST
        elif (d.month == 11 and d.day >= 15) or (d.month == 12 and d.day <= 24):
            return LiturgicalSeason.NATIVITY_FAST
        elif d.month == 12 and 25 <= d.day <= 31:
            return LiturgicalSeason.NATIVITY
        elif d.month == 1 and 1 <= d.day <= 6:
            return LiturgicalSeason.THEOPHANY
        
        return LiturgicalSeason.ORDINARY
    
    def get_feast(self, d: date) -> Optional[Dict[str, Any]]:
        """Get feast information for a date."""
        # Check fixed feasts
        key = (d.month, d.day)
        if key in GREAT_FEASTS:
            return GREAT_FEASTS[key]
        
        # Check moveable feasts
        if d.year != self.year:
            self._initialize_year(d.year)
        
        days_from_pascha = (d - self.pascha).days
        if days_from_pascha in MOVEABLE_FEASTS:
            return MOVEABLE_FEASTS[days_from_pascha]
        
        return None
    
    def get_liturgical_day(self, d: date) -> LiturgicalDay:
        """Get complete liturgical information for a date."""
        season = self.get_season(d)
        feast = self.get_feast(d)
        
        # Determine feast rank
        if feast:
            feast_rank = feast.get('rank', FeastRank.ORDINARY)
            feast_name = feast.get('name')
            gospel = feast.get('readings', {}).get('gospel', [])
            epistle = feast.get('readings', {}).get('epistle', [])
        else:
            feast_rank = FeastRank.ORDINARY
            feast_name = None
            gospel = []
            epistle = []
        
        # Calculate tone (Octoechos - 8-week cycle starting from Pascha)
        if d.year != self.year:
            self._initialize_year(d.year)
        
        weeks_from_pascha = (d - self.pascha).days // 7
        tone = (weeks_from_pascha % 8) + 1
        
        # Determine fasting
        fasting = self._get_fasting(d, season)
        
        return LiturgicalDay(
            date=d,
            season=season,
            feast_rank=feast_rank,
            feast_name=feast_name,
            gospel_readings=gospel if isinstance(gospel, list) else [gospel],
            epistle_readings=epistle if isinstance(epistle, list) else [epistle],
            tone=tone,
            fasting=fasting
        )
    
    def _get_fasting(self, d: date, season: LiturgicalSeason) -> str:
        """Determine fasting discipline for a date."""
        weekday = d.weekday()  # 0=Monday, 6=Sunday
        
        # Strict fasting seasons
        if season in (LiturgicalSeason.GREAT_LENT, LiturgicalSeason.HOLY_WEEK):
            if weekday in (5, 6):  # Saturday, Sunday
                return 'wine_oil'
            return 'strict'
        
        # Other fasting seasons
        if season in (LiturgicalSeason.DORMITION_FAST, LiturgicalSeason.NATIVITY_FAST,
                      LiturgicalSeason.APOSTLES_FAST):
            if weekday in (5, 6):
                return 'fish'
            elif weekday in (1, 3):  # Tuesday, Thursday
                return 'wine_oil'
            return 'strict'
        
        # Regular weeks - Wednesday and Friday
        if weekday in (2, 4):  # Wednesday, Friday
            return 'strict'
        
        return 'none'
    
    def get_readings_for_verse_context(self, verse_ref: str) -> Dict[str, Any]:
        """
        Get liturgical context for when a verse is read.
        Returns information about when this verse appears in the lectionary.
        """
        result = {
            'verse': verse_ref,
            'liturgical_occasions': [],
            'seasons': [],
            'feasts': []
        }
        
        # Check gospel lectionary
        for key, reading in GOSPEL_LECTIONARY.items():
            if verse_ref in reading['gospel'] or reading['gospel'].split()[0] in verse_ref:
                result['liturgical_occasions'].append({
                    'occasion': key,
                    'theme': reading['theme']
                })
        
        # Check great feasts
        for feast_key, feast in GREAT_FEASTS.items():
            readings = feast.get('readings', {})
            for reading_type, refs in readings.items():
                if isinstance(refs, list):
                    for ref in refs:
                        if verse_ref in ref or ref.split()[0] in verse_ref:
                            result['feasts'].append({
                                'feast': feast['name'],
                                'date': f"{feast_key[0]}/{feast_key[1]}",
                                'reading_type': reading_type
                            })
                elif verse_ref in refs:
                    result['feasts'].append({
                        'feast': feast['name'],
                        'date': f"{feast_key[0]}/{feast_key[1]}",
                        'reading_type': reading_type
                    })
        
        return result
    
    def get_anagogical_weight(self, d: date) -> float:
        """
        Calculate anagogical sense weight based on liturgical context.
        Higher during eschatologically-significant seasons.
        """
        season = self.get_season(d)
        feast = self.get_feast(d)
        
        base_weight = 0.20  # Default from MASTER_PLAN.md
        
        # Season modifiers
        season_modifiers = {
            LiturgicalSeason.PASCHA: 0.40,
            LiturgicalSeason.BRIGHT_WEEK: 0.35,
            LiturgicalSeason.HOLY_WEEK: 0.30,
            LiturgicalSeason.GREAT_LENT: 0.25,
            LiturgicalSeason.PENTECOST: 0.35,
            LiturgicalSeason.THEOPHANY: 0.30,
            LiturgicalSeason.NATIVITY: 0.28,
        }
        
        if season in season_modifiers:
            base_weight = season_modifiers[season]
        
        # Feast modifiers
        if feast:
            rank = feast.get('rank', FeastRank.ORDINARY)
            if rank == FeastRank.GREAT_FEAST:
                base_weight = min(0.45, base_weight + 0.15)
            elif rank == FeastRank.FEAST_OF_LORD:
                base_weight = min(0.40, base_weight + 0.10)
        
        return base_weight


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_liturgical_calendar = None


def get_liturgical_calendar() -> LiturgicalCalendar:
    """Get the global liturgical calendar instance."""
    global _liturgical_calendar
    if _liturgical_calendar is None:
        _liturgical_calendar = LiturgicalCalendar()
    return _liturgical_calendar


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for liturgical calendar."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Liturgical Calendar')
    parser.add_argument('--date', type=str, help='Get info for date (YYYY-MM-DD)')
    parser.add_argument('--pascha', type=int, help='Calculate Pascha for year')
    parser.add_argument('--year', type=int, help='Show key dates for year')
    parser.add_argument('--verse', type=str, help='Get liturgical context for verse')
    
    args = parser.parse_args()
    
    calendar = get_liturgical_calendar()
    
    if args.date:
        d = datetime.strptime(args.date, '%Y-%m-%d').date()
        day = calendar.get_liturgical_day(d)
        print(f"\nLiturgical Information for {d}:")
        print("=" * 50)
        print(f"  Season: {day.season.value}")
        print(f"  Tone: {day.tone}")
        print(f"  Fasting: {day.fasting}")
        if day.feast_name:
            print(f"  Feast: {day.feast_name}")
            print(f"  Rank: {day.feast_rank.name}")
        if day.gospel_readings:
            print(f"  Gospel: {', '.join(day.gospel_readings)}")
    
    elif args.pascha:
        pascha = calculate_orthodox_pascha(args.pascha)
        print(f"\nOrthodox Pascha {args.pascha}: {pascha}")
    
    elif args.year:
        calendar._initialize_year(args.year)
        print(f"\nKey Dates for {args.year}:")
        print("=" * 50)
        print(f"  Pascha: {calendar.pascha}")
        print(f"  Clean Monday: {calendar.clean_monday}")
        print(f"  Palm Sunday: {calendar.palm_sunday}")
        print(f"  Ascension: {calendar.ascension}")
        print(f"  Pentecost: {calendar.pentecost}")
    
    elif args.verse:
        context = calendar.get_readings_for_verse_context(args.verse)
        print(f"\nLiturgical Context for {args.verse}:")
        print("=" * 50)
        if context['liturgical_occasions']:
            print("  Lectionary Occasions:")
            for occ in context['liturgical_occasions']:
                print(f"    • {occ['occasion']}: {occ['theme']}")
        if context['feasts']:
            print("  Feast Days:")
            for feast in context['feasts']:
                print(f"    • {feast['feast']} ({feast['date']})")
    
    else:
        # Show today
        today = date.today()
        day = calendar.get_liturgical_day(today)
        print(f"\nToday ({today}):")
        print(f"  Season: {day.season.value}")
        print(f"  Tone: {day.tone}")
        if day.feast_name:
            print(f"  Feast: {day.feast_name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
