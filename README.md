# ΒΊΒΛΟΣ ΛΌΓΟΥ

## Orthodox Exegetical Commentary System

A comprehensive database-driven system for generating scholarly Orthodox Christian biblical commentary, implementing the Stratified Foundation System and Fourfold Sense methodology.

---

## 🏗️ System Architecture

```
ΒΊΒΛΟΣ ΛΌΓΟΥ/
├── main.py                    # Central CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment configuration template
├── bible_refinement_db.sql   # PostgreSQL database schema
│
├── config/
│   └── settings.py           # Central configuration management
│
├── scripts/
│   ├── __init__.py
│   ├── database.py           # Database connection & repositories
│   ├── ingestion.py          # Data ingestion pipeline
│   ├── processing.py         # Verse processing pipeline
│   └── output_generator.py   # Output generation (MD, JSON, HTML)
│
├── tools/
│   ├── ai_integration.py     # AI provider integration
│   └── bible_api.py          # Bible API integration
│
├── docs/
│   └── (documentation files)
│
├── data/                     # Input data files
├── output/                   # Generated output files
└── logs/                     # Log files
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 14+
- (Optional) OpenAI or Anthropic API key for AI-enhanced generation

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/biblos-logou.git
cd biblos-logou

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Database Setup

```bash
# Create the database
createdb biblos_logou

# Initialize schema and data
python main.py init --schema bible_refinement_db.sql --all
```

### 4. Basic Usage

```bash
# Check system status
python main.py status

# Process verses
python main.py process --batch 100

# Export results
python main.py export --dashboard
python main.py export --book "Genesis" --format markdown
```

---

## 📖 Core Concepts

### Fourfold Sense of Scripture

The system implements the traditional fourfold hermeneutical method:

| Sense | Weight | Description |
|-------|--------|-------------|
| **Literal** | 30% | Historical-grammatical meaning |
| **Allegorical** | 25% | Christological-typological significance |
| **Tropological** | 25% | Moral-formational application |
| **Anagogical** | 20% | Eschatological-heavenly meaning |

### Stratified Foundation System

Seven layers of narrative depth:

1. **Layer One** (Surface Adjacency): 0-50 pages
2. **Layer Two** (Near Foundation): 50-200 pages
3. **Layer Three** (Mid-Foundation): 200-500 pages
4. **Layer Four** (Deep Foundation): 500-1200 pages
5. **Layer Five** (Bedrock Foundation): 1200-2500 pages
6. **Layer Six** (Structural Undercurrent): Continuous
7. **Layer Seven** (Theological Bedrock): Eternal

### Nine-Matrix Elements

Each verse is analyzed across nine dimensions:

1. Emotional Valence (0.0-1.0)
2. Theological Weight (0.0-1.0)
3. Narrative Function
4. Sensory Intensity (0.0-1.0)
5. Grammatical Complexity (0.0-1.0)
6. Lexical Rarity (0.0-1.0)
7. Breath Rhythm
8. Register Baseline
9. Tonal Weight

### Orbital Resonance

Motifs follow harmonic trajectories:
- **Planting** (95% intensity)
- **Reinforcement at 1/2** (90%)
- **Reinforcement at 5/6** (60%)
- **Reinforcement at 15/16** (30%)
- **Convergence** (100%)

### Thread Density

Target: **18-22** active thread-points per 50-page span

---

## 🔧 CLI Commands

### `init` - Initialize Database

```bash
python main.py init --schema bible_refinement_db.sql --all
python main.py init --motifs  # Initialize motifs only
```

### `ingest` - Ingest Data

```bash
python main.py ingest --verses data/verses.txt
```

### `process` - Process Verses

```bash
python main.py process --batch 100          # Process batch
python main.py process --continuous         # Process all
python main.py process --verse-id 1234      # Process specific verse
```

### `export` - Generate Output

```bash
python main.py export --dashboard           # Progress dashboard
python main.py export --book "Genesis"      # Export single book
python main.py export --all --format both   # Export everything
```

### `status` - System Status

```bash
python main.py status
```

### `fetch` - Fetch Verse Text

```bash
python main.py fetch --verse "Genesis 1:1"
python main.py fetch --populate --limit 100
```

---

## 🗄️ Database Schema

### Core Tables

| Table | Description |
|-------|-------------|
| `canonical_books` | 73 Orthodox canonical books |
| `verses` | 37,454+ verses with fourfold senses |
| `events` | Biblical events for tonal arrangement |
| `motifs` | Orbital and standard motifs |
| `motif_activations` | Individual motif appearances |
| `typological_correspondences` | Type-antitype relationships |
| `sensory_vocabulary` | Sensory vocabulary codex |
| `patristic_sources` | Church Fathers commentary |
| `hermeneutical_principles` | Tonal ordering principles |
| `cross_references` | Scripture cross-references |

### Key Views

- `vw_next_processing_batch` - Verses ready for processing
- `vw_current_density` - Thread density status
- `vw_approaching_convergences` - Motifs nearing convergence
- `vw_fourfold_completion` - Sense completion status

---

## 🤖 AI Integration

The system supports multiple AI providers:

### OpenAI

```python
# In .env
AI_PROVIDER=openai
AI_API_KEY=sk-your-key
AI_MODEL=gpt-4
```

### Claude (Anthropic)

```python
# In .env
AI_PROVIDER=claude
AI_API_KEY=sk-ant-your-key
AI_MODEL=claude-3-sonnet-20240229
```

### Local (Template-based)

```python
# In .env (default, no API needed)
AI_PROVIDER=local
```

---

## 📤 Output Formats

### Markdown

Full commentary with:
- Fourfold sense analysis
- Nine-matrix elements
- Tonal characteristics
- Table of contents

### JSON

Structured data export for:
- Integration with other systems
- API consumption
- Data analysis

### Progress Dashboard

Real-time status including:
- Completion percentage
- Book-by-book progress
- Processing statistics

---

## 🎯 Primary Motifs

The system tracks 10 primary orbital motifs:

1. **The Lamb** - Sacrificial imagery (Genesis → Revelation)
2. **Wood** - Tree/Cross imagery (Eden → Golgotha)
3. **Silence** - Divine silence and still voice
4. **The Binding** - Bondage and release
5. **Water** - Creation through baptism
6. **Fire** - Divine fire (Burning bush → Pentecost)
7. **Blood** - Blood covenant
8. **Bread** - Manna to Eucharist
9. **Shepherd** - Shepherd imagery
10. **Stone** - Bethel to cornerstone

---

## 📚 Hermeneutical Principles

From Hermeneutical.txt:

1. **Inevitable Judgment** - Constant background sense of approaching catastrophe
2. **Emotional Honesty** - Preserve each event's native mood
3. **Anti-Flattening** - Don't darken individual scenes
4. **Pattern Pressure** - Let recognition do the work
5. **Temporal Dislocation** - Memory as dread carrier
6. **Load-Bearing Contrast** - Sharp contrasts at structural joints
7. **Haunting over Foreshadowing** - Feel followed by what's been seen

---

## 🔒 Configuration

All settings in `config/settings.py`:

```python
from config.settings import config

# Database
config.database.host
config.database.port

# Fourfold sense weights
config.fourfold_sense.literal_weight      # 0.30
config.fourfold_sense.allegorical_weight  # 0.25

# Thread density
config.thread_density.target_minimum      # 18
config.thread_density.target_maximum      # 22

# Orbital resonance
config.orbital_resonance.harmonic_ratios  # [0.5, 0.833, 0.9375]
```

---

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black scripts/ tools/ config/

# Lint
flake8 scripts/ tools/ config/
```

---

## 📝 License

[Your License Here]

---

## 🙏 Acknowledgments

Based on the Orthodox Christian exegetical tradition, drawing from:
- Patristic commentaries (Augustine, Chrysostom, Origen, etc.)
- Liturgical hermeneutics
- The Stratified Foundation System methodology
- MASTER_PLAN.md specifications

---

*"The blood-red sky comes from the whole arrangement, not from repainting each star."*
