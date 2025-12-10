# ΒΊΒΛΟΣ ΛΌΓΟΥ Implementation Guide

## Complete System Documentation

This guide provides detailed instructions for implementing and operating the ΒΊΒΛΟΣ ΛΌΓΟΥ Orthodox Exegetical Commentary System.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Data Ingestion](#data-ingestion)
5. [Verse Processing Pipeline](#verse-processing-pipeline)
6. [Output Generation](#output-generation)
7. [AI Integration](#ai-integration)
8. [Motif Management](#motif-management)
9. [Hermeneutical Principles](#hermeneutical-principles)
10. [Troubleshooting](#troubleshooting)

---

## 1. System Overview

### Purpose

The ΒΊΒΛΟΣ ΛΌΓΟΥ system transforms raw biblical text into richly annotated Orthodox Christian commentary through:

1. **Fourfold Sense Analysis** - Literal, Allegorical, Tropological, Anagogical
2. **Nine-Matrix Processing** - Multi-dimensional verse analysis
3. **Stratified Foundation** - Seven-layer depth structure
4. **Orbital Resonance** - Motif tracking across the narrative
5. **Tonal Adjustment** - Hermeneutical ordering principles

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Interface                         │
│                         (main.py)                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Ingestion│  │Processing│  │  Output  │  │   Tools  │   │
│  │ Pipeline │  │ Pipeline │  │Generator │  │(AI, API) │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
├───────┴─────────────┴─────────────┴─────────────┴──────────┤
│                    Database Layer                           │
│                  (PostgreSQL + SQL Schema)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Installation

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.9 or higher
- **PostgreSQL**: 14 or higher
- **Memory**: 4GB minimum, 8GB recommended
- **Storage**: 10GB for database and outputs

### Step-by-Step Installation

```bash
# 1. Clone repository
git clone https://github.com/your-repo/biblos-logou.git
cd biblos-logou

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Copy environment configuration
cp .env.example .env

# 6. Edit .env with your settings
nano .env  # or your preferred editor
```

### Environment Configuration

Edit `.env` with your settings:

```env
# Database
BIBLOS_DB_HOST=localhost
BIBLOS_DB_PORT=5432
BIBLOS_DB_NAME=biblos_logou
BIBLOS_DB_USER=postgres
BIBLOS_DB_PASSWORD=your_secure_password

# AI Provider (optional)
AI_PROVIDER=local  # or: openai, claude
# AI_API_KEY=your-api-key

# Logging
LOG_LEVEL=INFO
```

---

## 3. Database Setup

### Create PostgreSQL Database

```bash
# Using psql
psql -U postgres
CREATE DATABASE biblos_logou;
\q

# Or using createdb
createdb -U postgres biblos_logou
```

### Initialize Schema

```bash
# Run the complete schema
python main.py init --schema bible_refinement_db.sql --all
```

This creates:
- 16 core tables
- Enumerated types
- Views for common queries
- Functions for calculations
- Triggers for automatic updates
- Initial data (canonical books, motifs, hermeneutical principles)

### Verify Installation

```bash
python main.py status
```

Expected output:
```
==================================================
ΒΊΒΛΟΣ ΛΌΓΟΥ System Status
==================================================

Table Counts:
  canonical_books: 73
  verses: 0
  events: 0
  motifs: 10
  patristic_sources: 0
  cross_references: 0
...
```

---

## 4. Data Ingestion

### Verse Ingestion

#### From Text File

Create a verse file with format:
```
Genesis 1:1 — In the beginning God created the heaven and the earth.
Genesis 1:2 — And the earth was without form, and void...
```

Ingest:
```bash
python main.py ingest --verses data/verses.txt
```

#### From Bible API

```bash
# Fetch specific verse
python main.py fetch --verse "Genesis 1:1"

# Populate missing verses
python main.py fetch --populate --limit 100 --book "Genesis"
```

### Event Ingestion

Events can be ingested programmatically:

```python
from scripts.ingestion import EventIngester
from scripts.database import get_db, init_db

init_db()
ingester = EventIngester(get_db())

events = [
    {
        'part_number': 1,
        'part_title': 'BEFORE ALL THINGS',
        'event_number': 1,
        'event_description': 'Creation of light'
    },
    # ... more events
]

ingester.ingest_events(events)
```

### Patristic Sources

```python
from scripts.ingestion import PatristicIngester
from scripts.database import get_db, init_db

init_db()
ingester = PatristicIngester(get_db())

ingester.ingest_patristic_text(
    father_name='Augustine',
    work_title='Confessions',
    content='Your patristic text here...',
    section_ref='Book XI, Chapter 14'
)
```

---

## 5. Verse Processing Pipeline

### Processing Stages

Each verse passes through these stages:

1. **Raw** → Initial state after ingestion
2. **Parsed** → Text extracted and normalized
3. **Analyzed** → Nine-matrix calculated
4. **Stratified** → Foundation layers assigned
5. **Fleshed Out** → Fourfold senses expanded
6. **Tonally Adjusted** → Hermeneutical ordering applied
7. **Refined** → Final polish complete
8. **Verified** → Passed invisibility checks

### Running Processing

```bash
# Process a batch
python main.py process --batch 100

# Process continuously until complete
python main.py process --continuous

# Process specific verse
python main.py process --verse-id 1234
```

### Processing Components

#### Fourfold Sense Generator

```python
from scripts.processing import FourfoldSenseGenerator

generator = FourfoldSenseGenerator()
senses = generator.generate_all_senses(verse, book_info)

# Result:
# {
#     'literal': 'Historical-grammatical analysis...',
#     'allegorical': 'Christological significance...',
#     'tropological': 'Moral application...',
#     'anagogical': 'Eschatological meaning...'
# }
```

#### Nine-Matrix Calculator

```python
from scripts.processing import NineMatrixCalculator

calculator = NineMatrixCalculator()
matrix = calculator.calculate_all(verse, book_info)

# Result:
# {
#     'emotional_valence': 0.65,
#     'theological_weight': 0.80,
#     'narrative_function': 'scene-setting',
#     'sensory_intensity': 0.70,
#     'grammatical_complexity': 0.55,
#     'lexical_rarity': 0.42,
#     'breath_rhythm': 'sustained',
#     'register_baseline': 'narrative-covenantal'
# }
```

#### Tonal Adjuster

```python
from scripts.processing import TonalAdjuster

adjuster = TonalAdjuster()
tonal = adjuster.apply_tonal_adjustments(verse, book_info)

# Result:
# {
#     'tonal_weight': 'neutral',
#     'dread_amplification': 0.35,
#     'local_emotional_honesty': 'Native character preserved...',
#     'temporal_dislocation_offset': 0
# }
```

---

## 6. Output Generation

### Available Formats

1. **Markdown** - Full commentary with formatting
2. **JSON** - Structured data for APIs
3. **HTML** - Web-ready output (planned)
4. **LaTeX** - Print-ready output (planned)

### Generating Output

```bash
# Progress dashboard
python main.py export --dashboard

# Single book
python main.py export --book "Genesis" --format markdown

# All outputs
python main.py export --all --format both
```

### Output Files

Generated in `output/` directory:

```
output/
├── Progress_Dashboard.md
├── Hermeneutical_Arrangement.md
├── Motif_Registry.md
├── Genesis_Commentary.md
├── Genesis_Commentary.json
└── full_database_export.json
```

### Programmatic Output

```python
from scripts.output_generator import OutputOrchestrator
from scripts.database import get_db, init_db

init_db()
orchestrator = OutputOrchestrator(get_db())

# Export specific book
results = orchestrator.export_book('Genesis', ['markdown', 'json'])

# Export all
results = orchestrator.export_all(['markdown', 'json'])
```

---

## 7. AI Integration

### Provider Configuration

#### Local Provider (Default)

Uses template-based generation without external API:

```env
AI_PROVIDER=local
```

#### OpenAI

```env
AI_PROVIDER=openai
AI_API_KEY=sk-your-openai-key
AI_MODEL=gpt-4
```

#### Claude (Anthropic)

```env
AI_PROVIDER=claude
AI_API_KEY=sk-ant-your-anthropic-key
AI_MODEL=claude-3-sonnet-20240229
```

### Using AI-Enhanced Processing

```python
from tools.ai_integration import AIEnhancedProcessor

processor = AIEnhancedProcessor()

# Generate fourfold senses with AI
senses = processor.generate_fourfold_senses(
    verse_ref='Genesis 1:1',
    verse_text='In the beginning God created...',
    book_category='pentateuch'
)

# Generate refined explication
explication = processor.generate_refined_explication(
    verse_ref='Genesis 1:1',
    verse_text='In the beginning God created...',
    senses=senses,
    matrix=matrix
)
```

### Prompt Templates

The system includes optimized prompts for:

1. **Fourfold Sense Analysis** - Category-specific prompts
2. **Refined Explication** - Integration prompts
3. **Motif Activation** - Invisible incorporation prompts
4. **Tonal Adjustment** - Hermeneutical positioning prompts

---

## 8. Motif Management

### Primary Motifs

The system tracks 10 primary orbital motifs:

| Motif | Layer | Planting | Convergence |
|-------|-------|----------|-------------|
| The Lamb | 5 | p.50 | p.2400 |
| Wood | 5 | p.20 | p.2200 |
| Silence | 5 | p.100 | p.2200 |
| The Binding | 5 | p.700 | p.2200 |
| Water | 4 | p.10 | p.1800 |
| Fire | 4 | p.300 | p.2050 |
| Blood | 5 | p.50 | p.2200 |
| Bread | 4 | p.400 | p.2100 |
| Shepherd | 4 | p.50 | p.1900 |
| Stone | 4 | p.750 | p.2000 |

### Orbital Resonance Calculation

```python
from scripts.processing import OrbitalResonanceCalculator

calc = OrbitalResonanceCalculator()

# Calculate harmonic positions
positions = calc.calculate_harmonic_positions(
    planting_page=50,
    convergence_page=2400
)
# Result: [1225, 2006, 2253]  # at 1/2, 5/6, 15/16

# Calculate intensity at current position
position = calc.calculate_orbital_position(50, 2400, 1000)
intensity = calc.calculate_intensity_at_position(position)
```

### Thread Density Management

```python
from scripts.processing import ThreadDensityManager

manager = ThreadDensityManager()

# Check density at page
density = manager.calculate_density_at_page(500)

# Result:
# {
#     'page': 500,
#     'total_density': 19.5,
#     'within_bounds': True,
#     'recommendation': 'Density optimal.'
# }
```

Target bounds: **18-22** thread-points per 50-page span

---

## 9. Hermeneutical Principles

### Core Principles from Hermeneutical.txt

1. **Inevitable Judgment**
   > "Keep a constant background sense of inevitable but not yet arrived judgment."

2. **Emotional Honesty**
   > "Let each event keep its own mood intact: joy as joy, terror as terror."

3. **Anti-Flattening Guard**
   > "The blood-red sky comes from the whole arrangement, not from repainting each star."

4. **Invisible Machinery**
   > "Let recognition do the work."

5. **Memory as Dread Carrier**
   > "Use non-chronology as emotional shuffling."

6. **Load-Bearing Contrast**
   > "Reserve the sharpest contrasts for points meant to feel load-bearing."

7. **Haunting over Foreshadowing**
   > "The order should make readers feel followed by what they have already seen."

### Implementation

These principles are stored in the `hermeneutical_principles` table and applied during tonal adjustment:

```python
from scripts.processing import TonalAdjuster

adjuster = TonalAdjuster()

# Apply principles to verse processing
tonal = adjuster.apply_tonal_adjustments(verse, book_info)
```

---

## 10. Troubleshooting

### Common Issues

#### Database Connection Failed

```
Error: Failed to initialize database connection
```

**Solution**: Check your `.env` settings and ensure PostgreSQL is running:
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection
psql -U postgres -d biblos_logou -c "SELECT 1;"
```

#### Module Import Errors

```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

#### API Rate Limiting

```
Error: OpenAI rate limit exceeded
```

**Solution**: The system includes automatic rate limiting. Increase delays or use local provider:
```env
AI_PROVIDER=local
```

#### Empty Processing Results

```
Processed: 0, Success: 0
```

**Solution**: Ensure verses are ingested first:
```bash
python main.py ingest --verses data/verses.txt
python main.py status  # Verify verse count
```

### Getting Help

1. Check logs in `logs/biblos_logou.log`
2. Run with verbose flag: `python main.py -v status`
3. Review database status: `python main.py status`

---

## Appendix: SQL Reference

### Useful Queries

```sql
-- Get processing status
SELECT status, COUNT(*) 
FROM verses 
GROUP BY status;

-- Find verses by book
SELECT verse_reference, sense_literal 
FROM verses v
JOIN canonical_books cb ON v.book_id = cb.id
WHERE cb.name = 'Genesis'
LIMIT 10;

-- Check thread density at page
SELECT * FROM check_thread_density(500);

-- Get approaching motif convergences
SELECT * FROM vw_approaching_convergences;

-- Find verses with high theological weight
SELECT verse_reference, theological_weight
FROM verses
WHERE theological_weight > 0.8
ORDER BY theological_weight DESC;
```

---

*Document Version: 2.0*
*Last Updated: December 2024*
