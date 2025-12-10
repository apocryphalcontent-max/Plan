"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Config Package
Central configuration management for Orthodox Exegetical Commentary System
"""

__version__ = "2.0.0"

from config.settings import (
    config,
    MasterConfig,
    DatabaseConfig,
    FourfoldSenseConfig,
    ThreadDensityConfig,
    OrbitalResonanceConfig,
    ProcessingConfig,
    HermeneuticalConfig,
    APIConfig,
    LoggingConfig,
    FoundationLayer,
    PRIMARY_MOTIFS,
    CANONICAL_ORDER,
    BASE_DIR,
    CONFIG_DIR,
    SCRIPTS_DIR,
    TOOLS_DIR,
    DOCS_DIR,
    OUTPUT_DIR,
    DATA_DIR,
    LOGS_DIR
)

__all__ = [
    'config',
    'MasterConfig',
    'DatabaseConfig',
    'FourfoldSenseConfig',
    'ThreadDensityConfig',
    'OrbitalResonanceConfig',
    'ProcessingConfig',
    'HermeneuticalConfig',
    'APIConfig',
    'LoggingConfig',
    'FoundationLayer',
    'PRIMARY_MOTIFS',
    'CANONICAL_ORDER',
    'BASE_DIR',
    'CONFIG_DIR',
    'SCRIPTS_DIR',
    'TOOLS_DIR',
    'DOCS_DIR',
    'OUTPUT_DIR',
    'DATA_DIR',
    'LOGS_DIR'
]
