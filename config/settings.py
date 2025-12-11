#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Configuration Settings
Central configuration for all system components.

This module provides:
- Centralized configuration dataclasses for all components
- Environment variable integration
- Type-safe configuration access
- Validation utilities

All configuration is loaded once at module import and can be accessed
via the global `config` object.
"""

import os
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum

# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class ValidationError(ConfigurationError):
    """Raised when configuration validation fails."""
    pass


# ============================================================================
# BASE PATHS
# ============================================================================

BASE_DIR: Path = Path(__file__).parent.parent
CONFIG_DIR: Path = BASE_DIR / "config"
SCRIPTS_DIR: Path = BASE_DIR / "scripts"
TOOLS_DIR: Path = BASE_DIR / "tools"
DOCS_DIR: Path = BASE_DIR / "docs"
OUTPUT_DIR: Path = BASE_DIR / "output"
DATA_DIR: Path = BASE_DIR / "data"
LOGS_DIR: Path = BASE_DIR / "logs"

# Create directories if they don't exist
for _directory in [OUTPUT_DIR, DATA_DIR, LOGS_DIR]:
    _directory.mkdir(parents=True, exist_ok=True)


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

def _get_env_int(key: str, default: int) -> int:
    """Safely get an integer from environment variable."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def _get_env_float(key: str, default: float) -> float:
    """Safely get a float from environment variable."""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default


@dataclass
class DatabaseConfig:
    """
    PostgreSQL database configuration.
    
    All settings can be overridden via environment variables:
    - BIBLOS_DB_HOST: Database host
    - BIBLOS_DB_PORT: Database port
    - BIBLOS_DB_NAME: Database name
    - BIBLOS_DB_USER: Database user
    - BIBLOS_DB_PASSWORD: Database password
    """
    host: str = field(default_factory=lambda: os.getenv("BIBLOS_DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: _get_env_int("BIBLOS_DB_PORT", 5432))
    database: str = field(default_factory=lambda: os.getenv("BIBLOS_DB_NAME", "biblos_logou"))
    user: str = field(default_factory=lambda: os.getenv("BIBLOS_DB_USER", "postgres"))
    password: str = field(default_factory=lambda: os.getenv("BIBLOS_DB_PASSWORD", ""))
    
    # Connection pool settings
    min_connections: int = 2
    max_connections: int = 10
    
    # Timeouts
    connect_timeout: int = 30
    statement_timeout: int = 300000  # 5 minutes for complex queries
    
    @property
    def connection_string(self) -> str:
        """Get the PostgreSQL connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def dsn(self) -> Dict[str, Any]:
        """Get connection parameters as dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password
        }
    
    def validate(self) -> bool:
        """
        Validate the database configuration.
        
        Returns:
            True if configuration is valid.
            
        Raises:
            ValidationError: If configuration is invalid.
        """
        if not self.host:
            raise ValidationError("Database host is required")
        if self.port < 1 or self.port > 65535:
            raise ValidationError(f"Invalid port: {self.port}")
        if not self.database:
            raise ValidationError("Database name is required")
        if not self.user:
            raise ValidationError("Database user is required")
        return True


# ============================================================================
# FOURFOLD SENSE CONFIGURATION
# ============================================================================

@dataclass
class FourfoldSenseConfig:
    """Configuration for fourfold sense percentages per MASTER_PLAN.md"""
    literal_weight: float = 0.30      # 30% - Historical-grammatical
    allegorical_weight: float = 0.25  # 25% - Christological-typological
    tropological_weight: float = 0.25 # 25% - Moral-formational
    anagogical_weight: float = 0.20   # 20% - Eschatological-heavenly
    
    def validate(self) -> bool:
        """Ensure weights sum to 1.0"""
        total = (self.literal_weight + self.allegorical_weight + 
                self.tropological_weight + self.anagogical_weight)
        return abs(total - 1.0) < 0.001


# ============================================================================
# STRATIFIED FOUNDATION CONFIGURATION
# ============================================================================

class FoundationLayer(Enum):
    """Seven foundation layers per Stratified Foundation System"""
    SURFACE_ADJACENCY = ("layer_one", 0, 50)       # 0-50 pages
    NEAR_FOUNDATION = ("layer_two", 50, 200)       # 50-200 pages
    MID_FOUNDATION = ("layer_three", 200, 500)     # 200-500 pages
    DEEP_FOUNDATION = ("layer_four", 500, 1200)    # 500-1200 pages
    BEDROCK_FOUNDATION = ("layer_five", 1200, 2500) # 1200-2500 pages
    STRUCTURAL_UNDERCURRENT = ("layer_six", 0, -1)  # Continuous
    THEOLOGICAL_BEDROCK = ("layer_seven", 0, -1)    # Eternal
    
    @property
    def db_value(self) -> str:
        return self.value[0]
    
    @property
    def min_pages(self) -> int:
        return self.value[1]
    
    @property
    def max_pages(self) -> int:
        return self.value[2]


@dataclass
class ThreadDensityConfig:
    """Thread density bounds per Stratified Foundation System"""
    target_minimum: int = 18
    target_maximum: int = 22
    warning_threshold_low: int = 16
    warning_threshold_high: int = 24
    critical_threshold_low: int = 14
    critical_threshold_high: int = 26
    
    # Layer weights for density calculation
    layer_weights: Dict[str, float] = field(default_factory=lambda: {
        "layer_one": 1.0,
        "layer_two": 1.0,
        "layer_three": 1.0,
        "layer_four_approach": 1.0,
        "layer_four_resonance": 2.0,
        "layer_five_resonance": 3.0,
        "temporal_folding": 0.5,
        "typological": 0.5
    })


# ============================================================================
# ORBITAL RESONANCE CONFIGURATION
# ============================================================================

@dataclass
class OrbitalResonanceConfig:
    """Harmonic ratios for orbital resonance calculations"""
    harmonic_ratios: List[float] = field(default_factory=lambda: [
        0.5,      # 1/2 - First reinforcement
        0.833,    # 5/6 - Second reinforcement
        0.9375    # 15/16 - Final approach
    ])
    
    # Intensity curve: 95% → 90% → 60% → 30% → 100%
    intensity_curve: Dict[str, float] = field(default_factory=lambda: {
        "planting": 0.95,
        "early_reinforcement": 0.90,
        "mid_trajectory": 0.60,
        "low_point": 0.30,
        "convergence": 1.00
    })
    
    # Variation requirements for invisibility
    minimum_variation_between_activations: float = 0.10
    vocabulary_variation_threshold: int = 3  # Min unique words per activation


# ============================================================================
# PROCESSING CONFIGURATION
# ============================================================================

@dataclass
class ProcessingConfig:
    """Configuration for verse processing pipeline"""
    batch_size: int = 100
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    # Parallel processing
    max_workers: int = 4
    
    # Quality thresholds
    minimum_sense_length: int = 50  # Minimum characters per sense
    maximum_sense_length: int = 2000
    uniqueness_threshold: float = 0.10  # 10% minimum variation
    
    # Output formats
    output_formats: List[str] = field(default_factory=lambda: [
        "markdown", "json", "html", "latex"
    ])


# ============================================================================
# HERMENEUTICAL CONFIGURATION
# ============================================================================

@dataclass 
class HermeneuticalConfig:
    """Configuration for tonal/hermeneutical processing"""
    
    # Emotional weight distribution targets
    emotional_distribution: Dict[str, float] = field(default_factory=lambda: {
        "light": 0.15,
        "neutral": 0.40,
        "unsettling": 0.20,
        "heavy": 0.15,
        "transcendent": 0.10
    })
    
    # Dread amplification settings
    base_dread_level: float = 0.30
    max_dread_amplification: float = 1.0
    dread_decay_rate: float = 0.05  # Per 50 pages
    
    # Contrast intensity settings
    maximum_contrast_intensity: float = 0.95
    load_bearing_contrast_threshold: float = 0.80


# ============================================================================
# API CONFIGURATION (for external integrations)
# ============================================================================

@dataclass
class APIConfig:
    """Configuration for external API integrations"""
    
    # OpenAI/Claude for content generation
    ai_provider: str = os.getenv("AI_PROVIDER", "openai")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_model: str = os.getenv("AI_MODEL", "gpt-4")
    ai_max_tokens: int = 4000
    ai_temperature: float = 0.7
    
    # Bible API for verse text
    bible_api_key: str = os.getenv("BIBLE_API_KEY", "")
    bible_api_base_url: str = "https://api.scripture.api.bible/v1"
    
    # Request settings
    request_timeout: int = 60
    max_retries: int = 3
    retry_backoff: float = 2.0


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Path = LOGS_DIR / "biblos_logou.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    # Component-specific logging
    component_levels: Dict[str, str] = field(default_factory=lambda: {
        "ingestion": "INFO",
        "processing": "INFO",
        "output": "INFO",
        "database": "WARNING",
        "api": "INFO"
    })


# ============================================================================
# PRIMARY MOTIFS CONFIGURATION
# ============================================================================

PRIMARY_MOTIFS = [
    {
        "name": "The Lamb",
        "description": "Sacrificial lamb imagery from Abel through Passover to Revelation",
        "layer": "layer_five",
        "planting_page": 50,
        "convergence_page": 2400,
        "vocabulary": ["lamb", "sacrifice", "blood", "offering", "altar", "slain", "spotless", "firstborn"],
        "modalities": ["visual", "tactile", "olfactory"]
    },
    {
        "name": "Wood",
        "description": "Wood/tree imagery from Eden through the Cross",
        "layer": "layer_five",
        "planting_page": 20,
        "convergence_page": 2200,
        "vocabulary": ["tree", "wood", "branch", "vine", "root", "fruit", "cross", "beam"],
        "modalities": ["visual", "tactile"]
    },
    {
        "name": "Silence",
        "description": "Divine silence and the still small voice",
        "layer": "layer_five",
        "planting_page": 100,
        "convergence_page": 2200,
        "vocabulary": ["silence", "still", "quiet", "whisper", "peace", "rest", "wait"],
        "modalities": ["auditory"]
    },
    {
        "name": "The Binding",
        "description": "Binding/bondage imagery from Isaac to Christ",
        "layer": "layer_five",
        "planting_page": 700,
        "convergence_page": 2200,
        "vocabulary": ["bind", "bound", "cord", "rope", "chain", "loose", "free", "release"],
        "modalities": ["tactile", "kinesthetic"]
    },
    {
        "name": "Water",
        "description": "Water imagery from creation through baptism",
        "layer": "layer_four",
        "planting_page": 10,
        "convergence_page": 1800,
        "vocabulary": ["water", "sea", "river", "flood", "well", "spring", "baptize", "wash"],
        "modalities": ["visual", "tactile", "auditory"]
    },
    {
        "name": "Fire",
        "description": "Divine fire from burning bush to Pentecost",
        "layer": "layer_four",
        "planting_page": 300,
        "convergence_page": 2050,
        "vocabulary": ["fire", "flame", "burn", "consume", "kindle", "torch", "light", "blaze"],
        "modalities": ["visual", "tactile", "olfactory"]
    },
    {
        "name": "Blood",
        "description": "Blood covenant from Abel to the Cross",
        "layer": "layer_five",
        "planting_page": 50,
        "convergence_page": 2200,
        "vocabulary": ["blood", "life", "covenant", "sprinkle", "pour", "shed", "redeem"],
        "modalities": ["visual", "tactile"]
    },
    {
        "name": "Bread",
        "description": "Bread/manna imagery to Eucharist",
        "layer": "layer_four",
        "planting_page": 400,
        "convergence_page": 2100,
        "vocabulary": ["bread", "manna", "grain", "wheat", "flour", "leaven", "unleavened", "eat"],
        "modalities": ["tactile", "gustatory", "olfactory"]
    },
    {
        "name": "Shepherd",
        "description": "Shepherd imagery from Abel to Good Shepherd",
        "layer": "layer_four",
        "planting_page": 50,
        "convergence_page": 1900,
        "vocabulary": ["shepherd", "sheep", "flock", "pasture", "staff", "rod", "fold", "lamb"],
        "modalities": ["visual", "auditory"]
    },
    {
        "name": "Stone",
        "description": "Stone imagery from Bethel to cornerstone",
        "layer": "layer_four",
        "planting_page": 750,
        "convergence_page": 2000,
        "vocabulary": ["stone", "rock", "pillar", "altar", "cornerstone", "foundation", "tablet"],
        "modalities": ["visual", "tactile"]
    }
]


# ============================================================================
# CANONICAL BOOK ORDER
# ============================================================================

CANONICAL_ORDER = {
    # Pentateuch
    "Genesis": 1, "Exodus": 2, "Leviticus": 3, "Numbers": 4, "Deuteronomy": 5,
    # Historical
    "Joshua": 6, "Judges": 7, "Ruth": 8, "1 Samuel": 9, "2 Samuel": 10,
    "1 Kings": 11, "2 Kings": 12, "1 Chronicles": 13, "2 Chronicles": 14,
    "Ezra": 15, "Nehemiah": 16, "Esther": 17,
    # Poetic
    "Job": 18, "Psalms": 19, "Proverbs": 20, "Ecclesiastes": 21, "Song of Solomon": 22,
    # Major Prophets
    "Isaiah": 23, "Jeremiah": 24, "Lamentations": 25, "Ezekiel": 26, "Daniel": 27,
    # Minor Prophets
    "Hosea": 28, "Joel": 29, "Amos": 30, "Obadiah": 31, "Jonah": 32,
    "Micah": 33, "Nahum": 34, "Habakkuk": 35, "Zephaniah": 36,
    "Haggai": 37, "Zechariah": 38, "Malachi": 39,
    # Deuterocanonical
    "Tobit": 39.1, "Judith": 39.2, "1 Maccabees": 39.3, "2 Maccabees": 39.4,
    "Wisdom": 39.5, "Sirach": 39.6, "Baruch": 39.7,
    # Gospels
    "Matthew": 40, "Mark": 41, "Luke": 42, "John": 43,
    # Acts
    "Acts": 44,
    # Pauline Epistles
    "Romans": 45, "1 Corinthians": 46, "2 Corinthians": 47, "Galatians": 48,
    "Ephesians": 49, "Philippians": 50, "Colossians": 51,
    "1 Thessalonians": 52, "2 Thessalonians": 53,
    "1 Timothy": 54, "2 Timothy": 55, "Titus": 56, "Philemon": 57,
    "Hebrews": 58,
    # General Epistles
    "James": 59, "1 Peter": 60, "2 Peter": 61,
    "1 John": 62, "2 John": 63, "3 John": 64, "Jude": 65,
    # Apocalyptic
    "Revelation": 66
}


# ============================================================================
# MASTER CONFIGURATION INSTANCE
# ============================================================================

@dataclass
class MasterConfig:
    """
    Master configuration aggregating all settings.
    
    Provides a unified interface for accessing all configuration
    settings with validation support.
    """
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    fourfold_sense: FourfoldSenseConfig = field(default_factory=FourfoldSenseConfig)
    thread_density: ThreadDensityConfig = field(default_factory=ThreadDensityConfig)
    orbital_resonance: OrbitalResonanceConfig = field(default_factory=OrbitalResonanceConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    hermeneutical: HermeneuticalConfig = field(default_factory=HermeneuticalConfig)
    api: APIConfig = field(default_factory=APIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    def validate(self) -> List[str]:
        """
        Validate all configuration settings.
        
        Returns:
            List of error messages. Empty list if all valid.
        """
        errors: List[str] = []
        
        if not self.fourfold_sense.validate():
            errors.append("Fourfold sense weights do not sum to 1.0")
        
        if self.thread_density.target_minimum >= self.thread_density.target_maximum:
            errors.append("Thread density minimum must be less than maximum")
        
        try:
            self.database.validate()
        except ValidationError as e:
            errors.append(str(e))
        
        return errors
    
    def validate_or_raise(self) -> None:
        """
        Validate configuration and raise if invalid.
        
        Raises:
            ConfigurationError: If any configuration is invalid.
        """
        errors = self.validate()
        if errors:
            raise ConfigurationError(f"Configuration errors: {'; '.join(errors)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of all settings.
        """
        return {
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'database': self.database.database,
                'user': self.database.user,
                # Note: password is not included for security
            },
            'processing': {
                'batch_size': self.processing.batch_size,
                'max_workers': self.processing.max_workers,
            },
            'api': {
                'ai_provider': self.api.ai_provider,
                'ai_model': self.api.ai_model,
            }
        }


# ============================================================================
# GLOBAL CONFIGURATION INSTANCE
# ============================================================================

# Singleton configuration instance
_config: Optional[MasterConfig] = None


def get_config() -> MasterConfig:
    """
    Get the global configuration instance.
    
    Returns:
        The singleton MasterConfig instance.
    """
    global _config
    if _config is None:
        _config = MasterConfig()
    return _config


def reload_config() -> MasterConfig:
    """
    Reload configuration from environment.
    
    This is useful for testing or when environment variables change.
    
    Returns:
        A fresh MasterConfig instance.
    """
    global _config
    _config = MasterConfig()
    return _config


# Default global config for backward compatibility
config = get_config()
