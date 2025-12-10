"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Tools Package
Comprehensive tooling for Orthodox Exegetical Commentary System
"""

__version__ = "2.0.0"
__author__ = "ΒΊΒΛΟΣ ΛΌΓΟΥ Project"

from pathlib import Path

TOOLS_DIR = Path(__file__).parent

# Tool modules
from tools.ai_integration import AIManager, get_ai
from tools.bible_api import BibleAPIClient, VerseFetcher, get_verse_fetcher

__all__ = [
    'AIManager',
    'get_ai',
    'BibleAPIClient', 
    'VerseFetcher',
    'get_verse_fetcher',
    'TOOLS_DIR'
]
