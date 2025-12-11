#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Configuration Settings
Central configuration for all system components.

This module provides centralized configuration management for the entire system.
Configuration values are loaded from environment variables where available,
with sensible defaults for development use.

Environment Variables:
    BIBLOS_DB_HOST - PostgreSQL host (default: localhost)
    BIBLOS_DB_PORT - PostgreSQL port (default: 5432)
    BIBLOS_DB_NAME - Database name (default: biblos_logou)
    BIBLOS_DB_USER - Database user (default: postgres)
    BIBLOS_DB_PASSWORD - Database password (default: empty)
    AI_PROVIDER - AI provider (openai, claude, local) (default: openai)
    AI_API_KEY - API key for AI provider
    AI_MODEL - AI model name (default: gpt-4)
    BIBLE_API_KEY - API key for Bible API
    LOG_LEVEL - Logging level (default: INFO)

Usage:
    from config.settings import config, BASE_DIR, OUTPUT_DIR

    # Access database settings
    db_host = config.database.host

    # Access fourfold sense weights
    literal_weight = config.fourfold_sense.literal_weight

    # Validate configuration
    errors = config.validate()
    if errors:
        print("Configuration errors:", errors)
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

# ============================================================================
# BASE PATHS
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
SCRIPTS_DIR = BASE_DIR / "scripts"
TOOLS_DIR = BASE_DIR / "tools"
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [OUTPUT_DIR, DATA_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

@dataclass
class DatabaseConfig:
    """
    PostgreSQL database configuration.

    Attributes:
        host: Database server hostname.
        port: Database server port.
        database: Database name.
        user: Database username.
        password: Database password.
        min_connections: Minimum connections in pool.
        max_connections: Maximum connections in pool.
        connect_timeout: Connection timeout in seconds.
        statement_timeout: Query timeout in milliseconds.
    """
    host: str = field(default_factory=lambda: os.getenv("BIBLOS_DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("BIBLOS_DB_PORT", "5432")))
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
        """Get PostgreSQL connection string (password masked in logs)."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def connection_string_safe(self) -> str:
        """Get connection string with masked password for logging."""
        masked = "***" if self.password else "(none)"
        return f"postgresql://{self.user}:{masked}@{self.host}:{self.port}/{self.database}"

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

    def reload_from_env(self) -> None:
        """Reload configuration from environment variables."""
        self.host = os.getenv("BIBLOS_DB_HOST", "localhost")
        self.port = int(os.getenv("BIBLOS_DB_PORT", "5432"))
        self.database = os.getenv("BIBLOS_DB_NAME", "biblos_logou")
        self.user = os.getenv("BIBLOS_DB_USER", "postgres")
        self.password = os.getenv("BIBLOS_DB_PASSWORD", "")


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

    This is the main configuration object that should be imported and used
    throughout the application. It provides access to all subsystem configurations.

    Example:
        from config.settings import config

        # Check database settings
        print(config.database.host)

        # Validate all settings
        errors = config.validate()
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
            List of error messages. Empty list means configuration is valid.
        """
        errors = []

        # Validate fourfold sense weights
        if not self.fourfold_sense.validate():
            total = (self.fourfold_sense.literal_weight +
                    self.fourfold_sense.allegorical_weight +
                    self.fourfold_sense.tropological_weight +
                    self.fourfold_sense.anagogical_weight)
            errors.append(f"Fourfold sense weights sum to {total:.3f}, should be 1.0")

        # Validate thread density bounds
        if self.thread_density.target_minimum >= self.thread_density.target_maximum:
            errors.append("Thread density minimum must be less than maximum")

        if self.thread_density.target_minimum < 0:
            errors.append("Thread density minimum cannot be negative")

        # Validate orbital resonance ratios
        for ratio in self.orbital_resonance.harmonic_ratios:
            if not 0.0 < ratio < 1.0:
                errors.append(f"Harmonic ratio {ratio} must be between 0 and 1")

        # Validate processing settings
        if self.processing.batch_size < 1:
            errors.append("Batch size must be at least 1")

        if self.processing.minimum_sense_length >= self.processing.maximum_sense_length:
            errors.append("Minimum sense length must be less than maximum")

        # Validate hermeneutical settings
        emotional_sum = sum(self.hermeneutical.emotional_distribution.values())
        if abs(emotional_sum - 1.0) > 0.01:
            errors.append(f"Emotional distribution sums to {emotional_sum:.3f}, should be 1.0")

        return errors

    def reload_from_env(self) -> None:
        """Reload all environment-based configuration values."""
        self.database.reload_from_env()
        # Recreate API config to pick up new env vars
        self.api = APIConfig()

    def is_valid(self) -> bool:
        """Check if configuration is valid without getting error details."""
        return len(self.validate()) == 0

    def print_summary(self) -> None:
        """Print a summary of current configuration (safe for logs)."""
        print("=" * 50)
        print("ΒΊΒΛΟΣ ΛΌΓΟΥ Configuration Summary")
        print("=" * 50)
        print(f"Database:     {self.database.connection_string_safe}")
        print(f"AI Provider:  {self.api.ai_provider}")
        print(f"AI Model:     {self.api.ai_model}")
        print(f"Batch Size:   {self.processing.batch_size}")
        print(f"Max Workers:  {self.processing.max_workers}")
        print(f"Log Level:    {self.logging.level}")
        print("=" * 50)


# Global configuration instance
config = MasterConfig()


def get_config() -> MasterConfig:
    """Get the global configuration instance."""
    return config


def reload_config() -> MasterConfig:
    """Reload configuration from environment and return updated config."""
    config.reload_from_env()
    return config
