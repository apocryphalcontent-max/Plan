-- ============================================================================
-- ΒΊΒΛΟΣ ΛΌΓΟΥ DATABASE SCHEMA
-- Complete Orthodox Exegetical Commentary System
-- Version 2.1 - Production Ready (Idempotent)
--
-- Based on MASTER_PLAN.md Stratified Foundation System
-- Designed for PostgreSQL 14+
--
-- This schema is fully idempotent - safe to run multiple times without errors.
-- All CREATE statements use IF NOT EXISTS, inserts use ON CONFLICT DO NOTHING,
-- and triggers use DROP IF EXISTS before creation.
-- ============================================================================

-- Enable required extensions (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text matching

-- ============================================================================
-- ENUMERATED TYPES
-- Create types only if they don't already exist (idempotent)
-- ============================================================================

DO $$ BEGIN
    CREATE TYPE book_category AS ENUM (
        'pentateuch',
        'historical',
        'poetic',
        'major_prophet',
        'minor_prophet',
        'deuterocanonical',
        'gospel',
        'acts',
        'pauline',
        'general_epistle',
        'apocalyptic'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE processing_status AS ENUM (
        'raw',              -- Initial ingestion, no processing
        'parsed',           -- Text extracted and normalized
        'analyzed',         -- Nine-matrix applied
        'stratified',       -- Foundation layers assigned
        'fleshed_out',      -- Fourfold sense expanded
        'tonally_adjusted', -- Hermeneutical ordering applied
        'refined',          -- Final polish complete
        'verified',         -- Passed all invisibility checks
        'failed',           -- Processing failed, needs retry
        'suspended'         -- Temporarily paused
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE foundation_layer AS ENUM (
        'layer_one',        -- Surface Adjacency (0-50 pages)
        'layer_two',        -- Near Foundation (50-200 pages)
        'layer_three',      -- Mid-Foundation (200-500 pages)
        'layer_four',       -- Deep Foundation (500-1200 pages)
        'layer_five',       -- Bedrock Foundation (1200-2500 pages)
        'layer_six',        -- Structural Undercurrent (continuous)
        'layer_seven'       -- Theological Bedrock (eternal)
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE emotional_weight AS ENUM (
        'light',            -- Joy, peace, celebration
        'neutral',          -- Exposition, transition
        'unsettling',       -- Tension building
        'heavy',            -- Dread, judgment, grief
        'transcendent'      -- Glory, theophany, resurrection
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE motif_status AS ENUM (
        'planted',          -- Initial appearance
        'reinforcing',      -- Intermediate appearances
        'approaching',      -- Nearing convergence
        'converging',       -- At detonation point
        'dormant',          -- Between activations
        'suspended',        -- Temporarily inactive
        'completed'         -- Full trajectory complete
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE sense_type AS ENUM (
        'literal',          -- Historical-grammatical
        'allegorical',      -- Christological-typological
        'tropological',     -- Moral-formational
        'anagogical'        -- Eschatological-heavenly
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ============================================================================
-- TABLE 1: CANONICAL_BOOKS
-- Master reference for all 73 Orthodox canonical books
-- ============================================================================

CREATE TABLE IF NOT EXISTS canonical_books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    abbreviation VARCHAR(10) NOT NULL,
    category book_category NOT NULL,
    canonical_order NUMERIC(4,1) NOT NULL,  -- Allows 39.1 for deuterocanonicals
    testament VARCHAR(20) NOT NULL CHECK (testament IN ('old', 'deuterocanonical', 'new')),
    total_chapters INTEGER NOT NULL,
    total_verses INTEGER NOT NULL,
    lxx_name VARCHAR(100),                  -- Septuagint name if different
    hebrew_name VARCHAR(100),               -- Hebrew name for OT books

    -- Volume assignment per MASTER_PLAN.md
    series_volume INTEGER,                  -- Which of the 40 volumes
    estimated_pages INTEGER,                -- Page estimate for this book

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate canonical books (idempotent with ON CONFLICT)
INSERT INTO canonical_books (name, abbreviation, category, canonical_order, testament, total_chapters, total_verses, series_volume) VALUES
-- Pentateuch
('Genesis', 'Gen', 'pentateuch', 1, 'old', 50, 1533, 1),
('Exodus', 'Exod', 'pentateuch', 2, 'old', 40, 1213, 2),
('Leviticus', 'Lev', 'pentateuch', 3, 'old', 27, 859, 3),
('Numbers', 'Num', 'pentateuch', 4, 'old', 36, 1288, 4),
('Deuteronomy', 'Deut', 'pentateuch', 5, 'old', 34, 959, 5),
-- Historical
('Joshua', 'Josh', 'historical', 6, 'old', 24, 658, 6),
('Judges', 'Judg', 'historical', 7, 'old', 21, 618, 6),
('Ruth', 'Ruth', 'historical', 8, 'old', 4, 85, 6),
('1 Samuel', '1Sam', 'historical', 9, 'old', 31, 810, 7),
('2 Samuel', '2Sam', 'historical', 10, 'old', 24, 695, 7),
('1 Kings', '1Kgs', 'historical', 11, 'old', 22, 816, 8),
('2 Kings', '2Kgs', 'historical', 12, 'old', 25, 719, 8),
('1 Chronicles', '1Chr', 'historical', 13, 'old', 29, 942, 9),
('2 Chronicles', '2Chr', 'historical', 14, 'old', 36, 822, 9),
('Ezra', 'Ezra', 'historical', 15, 'old', 10, 280, 10),
('Nehemiah', 'Neh', 'historical', 16, 'old', 13, 406, 10),
('Esther', 'Esth', 'historical', 17, 'old', 10, 167, 10),
-- Poetic/Wisdom
('Job', 'Job', 'poetic', 18, 'old', 42, 1070, 11),
('Psalms', 'Ps', 'poetic', 19, 'old', 150, 2461, 12),
('Proverbs', 'Prov', 'poetic', 20, 'old', 31, 915, 13),
('Ecclesiastes', 'Eccl', 'poetic', 21, 'old', 12, 222, 13),
('Song of Solomon', 'Song', 'poetic', 22, 'old', 8, 117, 13),
-- Major Prophets
('Isaiah', 'Isa', 'major_prophet', 23, 'old', 66, 1292, 14),
('Jeremiah', 'Jer', 'major_prophet', 24, 'old', 52, 1364, 15),
('Lamentations', 'Lam', 'major_prophet', 25, 'old', 5, 154, 15),
('Ezekiel', 'Ezek', 'major_prophet', 26, 'old', 48, 1273, 16),
('Daniel', 'Dan', 'major_prophet', 27, 'old', 12, 357, 16),
-- Minor Prophets
('Hosea', 'Hos', 'minor_prophet', 28, 'old', 14, 197, 17),
('Joel', 'Joel', 'minor_prophet', 29, 'old', 3, 73, 17),
('Amos', 'Amos', 'minor_prophet', 30, 'old', 9, 146, 17),
('Obadiah', 'Obad', 'minor_prophet', 31, 'old', 1, 21, 17),
('Jonah', 'Jonah', 'minor_prophet', 32, 'old', 4, 48, 17),
('Micah', 'Mic', 'minor_prophet', 33, 'old', 7, 105, 17),
('Nahum', 'Nah', 'minor_prophet', 34, 'old', 3, 47, 17),
('Habakkuk', 'Hab', 'minor_prophet', 35, 'old', 3, 56, 17),
('Zephaniah', 'Zeph', 'minor_prophet', 36, 'old', 3, 53, 17),
('Haggai', 'Hag', 'minor_prophet', 37, 'old', 2, 38, 17),
('Zechariah', 'Zech', 'minor_prophet', 38, 'old', 14, 211, 17),
('Malachi', 'Mal', 'minor_prophet', 39, 'old', 4, 55, 17),
-- Deuterocanonical
('Tobit', 'Tob', 'deuterocanonical', 39.1, 'deuterocanonical', 14, 244, 18),
('Judith', 'Jdt', 'deuterocanonical', 39.2, 'deuterocanonical', 16, 340, 18),
('1 Maccabees', '1Macc', 'deuterocanonical', 39.3, 'deuterocanonical', 16, 924, 19),
('2 Maccabees', '2Macc', 'deuterocanonical', 39.4, 'deuterocanonical', 15, 555, 19),
('Wisdom', 'Wis', 'deuterocanonical', 39.5, 'deuterocanonical', 19, 435, 20),
('Sirach', 'Sir', 'deuterocanonical', 39.6, 'deuterocanonical', 51, 1388, 20),
('Baruch', 'Bar', 'deuterocanonical', 39.7, 'deuterocanonical', 6, 213, 20),
-- Gospels
('Matthew', 'Matt', 'gospel', 40, 'new', 28, 1071, 21),
('Mark', 'Mark', 'gospel', 41, 'new', 16, 678, 22),
('Luke', 'Luke', 'gospel', 42, 'new', 24, 1151, 23),
('John', 'John', 'gospel', 43, 'new', 21, 879, 24),
-- Acts
('Acts', 'Acts', 'acts', 44, 'new', 28, 1007, 25),
-- Pauline Epistles
('Romans', 'Rom', 'pauline', 45, 'new', 16, 433, 26),
('1 Corinthians', '1Cor', 'pauline', 46, 'new', 16, 437, 27),
('2 Corinthians', '2Cor', 'pauline', 47, 'new', 13, 257, 27),
('Galatians', 'Gal', 'pauline', 48, 'new', 6, 149, 28),
('Ephesians', 'Eph', 'pauline', 49, 'new', 6, 155, 28),
('Philippians', 'Phil', 'pauline', 50, 'new', 4, 104, 28),
('Colossians', 'Col', 'pauline', 51, 'new', 4, 95, 28),
('1 Thessalonians', '1Thess', 'pauline', 52, 'new', 5, 89, 29),
('2 Thessalonians', '2Thess', 'pauline', 53, 'new', 3, 47, 29),
('1 Timothy', '1Tim', 'pauline', 54, 'new', 6, 113, 29),
('2 Timothy', '2Tim', 'pauline', 55, 'new', 4, 83, 29),
('Titus', 'Titus', 'pauline', 56, 'new', 3, 46, 29),
('Philemon', 'Phlm', 'pauline', 57, 'new', 1, 25, 29),
('Hebrews', 'Heb', 'general_epistle', 58, 'new', 13, 303, 30),
-- General Epistles
('James', 'Jas', 'general_epistle', 59, 'new', 5, 108, 31),
('1 Peter', '1Pet', 'general_epistle', 60, 'new', 5, 105, 31),
('2 Peter', '2Pet', 'general_epistle', 61, 'new', 3, 61, 31),
('1 John', '1John', 'general_epistle', 62, 'new', 5, 105, 32),
('2 John', '2John', 'general_epistle', 63, 'new', 1, 13, 32),
('3 John', '3John', 'general_epistle', 64, 'new', 1, 14, 32),
('Jude', 'Jude', 'general_epistle', 65, 'new', 1, 25, 32),
-- Apocalyptic
('Revelation', 'Rev', 'apocalyptic', 66, 'new', 22, 404, 40)
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- TABLE 2: VERSES
-- Core table for all ~37,454 biblical verses
-- ============================================================================

CREATE TABLE IF NOT EXISTS verses (
    id SERIAL PRIMARY KEY,

    -- Reference identification
    book_id INTEGER NOT NULL REFERENCES canonical_books(id),
    chapter INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    verse_reference VARCHAR(50) NOT NULL,  -- "Genesis 1:1" format

    -- Textual content (multiple versions)
    text_kjv TEXT,                          -- King James Version
    text_lxx TEXT,                          -- Septuagint Greek
    text_mt TEXT,                           -- Masoretic Hebrew
    text_vulgate TEXT,                      -- Latin Vulgate
    text_peshitta TEXT,                     -- Syriac Peshitta

    -- Existing explications (from Verses.txt)
    existing_explication TEXT,

    -- Refined content (generated)
    refined_explication TEXT,

    -- Fourfold sense analyses (per MASTER_PLAN.md percentages)
    sense_literal TEXT,                     -- 30% weight
    sense_allegorical TEXT,                 -- 25% weight
    sense_tropological TEXT,                -- 25% weight
    sense_anagogical TEXT,                  -- 20% weight

    -- Nine-matrix elements (from Stratified.txt)
    emotional_valence NUMERIC(3,2) CHECK (emotional_valence BETWEEN 0 AND 1),
    theological_weight NUMERIC(3,2) CHECK (theological_weight BETWEEN 0 AND 1),
    narrative_function VARCHAR(50),
    sensory_intensity NUMERIC(3,2) CHECK (sensory_intensity BETWEEN 0 AND 1),
    grammatical_complexity NUMERIC(3,2) CHECK (grammatical_complexity BETWEEN 0 AND 1),
    lexical_rarity NUMERIC(3,2) CHECK (lexical_rarity BETWEEN 0 AND 1),
    breath_rhythm VARCHAR(20),              -- 'sustained', 'punctuated', 'flowing'
    register_baseline VARCHAR(30),

    -- Tonal ordering (from Hermeneutical.txt)
    tonal_weight emotional_weight DEFAULT 'neutral',
    dread_amplification NUMERIC(3,2) DEFAULT 0.5,
    local_emotional_honesty TEXT,           -- Preserved native mood
    global_dread_contribution TEXT,         -- How it builds toward catastrophe
    temporal_dislocation_offset INTEGER DEFAULT 0,  -- Non-chronological positioning

    -- Canonical positioning
    canonical_position NUMERIC(10,6),       -- 0.0 to 1.0 across entire canon
    hermeneutical_order INTEGER,            -- Position in tonal arrangement
    estimated_page_number INTEGER,          -- Approximate page in final work

    -- Processing metadata
    status processing_status DEFAULT 'raw',
    failure_log TEXT,
    retry_count INTEGER DEFAULT 0,
    last_processed_at TIMESTAMP,

    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    UNIQUE(book_id, chapter, verse_number),
    UNIQUE(verse_reference)
);

-- Indexes for common queries (IF NOT EXISTS for idempotency)
CREATE INDEX IF NOT EXISTS idx_verses_book_chapter ON verses(book_id, chapter);
CREATE INDEX IF NOT EXISTS idx_verses_status ON verses(status);
CREATE INDEX IF NOT EXISTS idx_verses_tonal_weight ON verses(tonal_weight);
CREATE INDEX IF NOT EXISTS idx_verses_canonical_position ON verses(canonical_position);
CREATE INDEX IF NOT EXISTS idx_verses_hermeneutical_order ON verses(hermeneutical_order);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_verses_text_search ON verses USING gin(to_tsvector('english',
    COALESCE(text_kjv, '') || ' ' ||
    COALESCE(existing_explication, '') || ' ' ||
    COALESCE(refined_explication, '')
));

-- ============================================================================
-- TABLE 3: EVENTS
-- Biblical events for tonal/narrative reorganization (from BIBLICAL EVENTS)
-- ============================================================================

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,

    -- Hierarchical structure
    part_number INTEGER NOT NULL,           -- 1-13 from Hermeneutical.txt
    part_title TEXT NOT NULL,               -- "BEFORE ALL THINGS / THE INFANT BREATHES"
    event_number INTEGER NOT NULL,          -- Sequential within part
    event_description TEXT NOT NULL,        -- "Creation of light"

    -- Detailed event data
    full_narrative TEXT,                    -- Expanded description

    -- Tonal properties (from Hermeneutical.txt)
    emotional_weight emotional_weight NOT NULL DEFAULT 'neutral',
    local_mood TEXT,                        -- Native emotional character
    global_dread_function TEXT,             -- How it amplifies catastrophe intuition
    pattern_pressure_role TEXT,             -- What pattern it reinforces
    temporal_dislocation_rationale TEXT,    -- Why placed out of time
    breath_point BOOLEAN DEFAULT FALSE,     -- Is this a moment of emotional saturation
    load_bearing BOOLEAN DEFAULT FALSE,     -- Is this a structural joint

    -- Verse linkages
    linked_verse_ids INTEGER[],             -- Array of verse IDs
    primary_verse_id INTEGER REFERENCES verses(id),

    -- Narrative position
    load_bearing_score NUMERIC(5,2),        -- Calculated via resonance math
    contrast_intensity NUMERIC(3,2),        -- Sharpness of adjacent contrasts
    memory_echo_targets INTEGER[],          -- Earlier events this should "wake up"

    -- Generated content
    refined_narrative TEXT,                 -- Prose output per MASTER_PLAN.md

    -- Processing
    status processing_status DEFAULT 'raw',
    failure_log TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(part_number, event_number)
);

CREATE INDEX IF NOT EXISTS idx_events_part ON events(part_number);
CREATE INDEX IF NOT EXISTS idx_events_weight ON events(emotional_weight);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);

-- ============================================================================
-- TABLE 4: MOTIFS
-- Orbital and standard motifs (from Stratified.txt layers)
-- ============================================================================

CREATE TABLE IF NOT EXISTS motifs (
    id SERIAL PRIMARY KEY,

    -- Identification
    name VARCHAR(100) NOT NULL UNIQUE,      -- "The Binding", "Wood", "Silence"
    description TEXT,

    -- Layer assignment (from Stratified Foundation System)
    foundation_layer foundation_layer NOT NULL,

    -- Activation timeline
    planting_page INTEGER,
    reinforcement_pages INTEGER[],          -- Array of page numbers
    convergence_page INTEGER,

    -- Intensity gradient (percentages at each appearance)
    planting_intensity NUMERIC(3,2),
    reinforcement_intensities NUMERIC(3,2)[],
    convergence_intensity NUMERIC(3,2),

    -- Orbital resonance (for Layer 4-5)
    orbital_period INTEGER,                 -- Pages between resonances
    harmonic_ratios NUMERIC(5,4)[],         -- [0.5, 0.833, 0.9375] etc.
    current_orbital_position NUMERIC(10,6),

    -- Semantic field
    core_vocabulary TEXT[],                 -- Words in this motif's codex
    sensory_modalities TEXT[],              -- Which senses it engages

    -- Relationships
    reinforcing_motif_ids INTEGER[],        -- Motifs that support this one
    competing_motif_ids INTEGER[],          -- Motifs to separate from

    -- Status
    current_status motif_status DEFAULT 'dormant',
    last_activation_page INTEGER,
    next_activation_page INTEGER,

    -- Verification
    invisibility_verified BOOLEAN DEFAULT FALSE,
    last_verification_date DATE,
    verification_notes TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_motifs_layer ON motifs(foundation_layer);
CREATE INDEX IF NOT EXISTS idx_motifs_status ON motifs(current_status);

-- ============================================================================
-- TABLE 5: MOTIF_ACTIVATIONS
-- Track individual motif appearances across the text
-- ============================================================================

CREATE TABLE IF NOT EXISTS motif_activations (
    id SERIAL PRIMARY KEY,

    motif_id INTEGER NOT NULL REFERENCES motifs(id),
    verse_id INTEGER REFERENCES verses(id),
    event_id INTEGER REFERENCES events(id),

    -- Position
    page_number INTEGER NOT NULL,
    activation_type VARCHAR(20) NOT NULL,   -- 'plant', 'reinforce', 'converge'

    -- Intensity
    target_intensity NUMERIC(3,2),
    actual_intensity NUMERIC(3,2),

    -- Variation tracking (for invisibility)
    vocabulary_used TEXT[],
    sensory_modality_primary VARCHAR(20),
    grammatical_position VARCHAR(30),       -- 'main_clause', 'subordinate', etc.

    -- Verification
    variation_from_previous TEXT,           -- How this differs from last appearance
    invisibility_check_passed BOOLEAN,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_activations_motif ON motif_activations(motif_id);
CREATE INDEX IF NOT EXISTS idx_activations_page ON motif_activations(page_number);

-- ============================================================================
-- TABLE 6: TYPOLOGICAL_CORRESPONDENCES
-- Type-antitype relationships across Testaments
-- ============================================================================

CREATE TABLE IF NOT EXISTS typological_correspondences (
    id SERIAL PRIMARY KEY,

    -- Type (Old Testament)
    type_verse_id INTEGER REFERENCES verses(id),
    type_event_id INTEGER REFERENCES events(id),
    type_description TEXT NOT NULL,

    -- Antitype (New Testament fulfillment)
    antitype_verse_id INTEGER REFERENCES verses(id),
    antitype_event_id INTEGER REFERENCES events(id),
    antitype_description TEXT NOT NULL,

    -- Correspondence details
    correspondence_type VARCHAR(50),        -- 'prefiguration', 'echo', 'fulfillment'
    theological_significance TEXT,
    patristic_support TEXT,                 -- Which Fathers noted this

    -- Activation
    type_page INTEGER,
    antitype_page INTEGER,
    distance INTEGER GENERATED ALWAYS AS (antitype_page - type_page) STORED,

    -- Processing
    status processing_status DEFAULT 'raw',

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_typology_type ON typological_correspondences(type_verse_id);
CREATE INDEX IF NOT EXISTS idx_typology_antitype ON typological_correspondences(antitype_verse_id);

-- ============================================================================
-- TABLE 7: SENSORY_VOCABULARY_CODEX
-- The complete sensory vocabulary system (from Stratified.txt)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sensory_vocabulary (
    id SERIAL PRIMARY KEY,

    -- Categorization
    category book_category NOT NULL,
    sensory_domain VARCHAR(20) NOT NULL,    -- 'visual', 'auditory', 'tactile', etc.

    -- Vocabulary
    term TEXT NOT NULL,                     -- The actual phrase
    variants TEXT[],                        -- Alternative phrasings

    -- Usage constraints
    emotional_contexts emotional_weight[],  -- When this term is appropriate
    register_level INTEGER CHECK (register_level BETWEEN 1 AND 7),

    -- Frequency tracking
    usage_count INTEGER DEFAULT 0,
    last_used_page INTEGER,
    minimum_pages_between_uses INTEGER DEFAULT 100,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sensory_category ON sensory_vocabulary(category, sensory_domain);
CREATE UNIQUE INDEX IF NOT EXISTS idx_sensory_unique_term ON sensory_vocabulary(category, sensory_domain, term);

-- Populate sensory vocabulary (sample entries - idempotent)
INSERT INTO sensory_vocabulary (category, sensory_domain, term, register_level) VALUES
-- Pentateuch Visual
('pentateuch', 'visual', 'primordial darkness giving way to light', 5),
('pentateuch', 'visual', 'pillar of fire illuminating wilderness', 6),
('pentateuch', 'visual', 'mountain shrouded in smoke and glory', 7),
('pentateuch', 'visual', 'burning bush unconsumed', 6),
('pentateuch', 'visual', 'tabernacle gold gleaming', 5),
-- Pentateuch Auditory
('pentateuch', 'auditory', 'thunderous divine voice from Sinai', 7),
('pentateuch', 'auditory', 'still whisper in sacred silence', 5),
('pentateuch', 'auditory', 'trumpet blast announcing presence', 6),
('pentateuch', 'auditory', 'shofar blast announcing', 6),
-- Gospel Visual
('gospel', 'visual', 'Jesus face shining transfigured', 7),
('gospel', 'visual', 'crowd pressing close', 3),
('gospel', 'visual', 'cross silhouetted against darkness', 7),
-- Apocalyptic Visual
('apocalyptic', 'visual', 'throne room glory blazing', 7),
('apocalyptic', 'visual', 'Lamb standing as slain', 7),
('apocalyptic', 'visual', 'New Jerusalem descending', 7)
ON CONFLICT (category, sensory_domain, term) DO NOTHING;

-- ============================================================================
-- TABLE 8: PATRISTIC_SOURCES
-- Commentary from Church Fathers
-- ============================================================================

CREATE TABLE IF NOT EXISTS patristic_sources (
    id SERIAL PRIMARY KEY,

    -- Source identification
    father_name VARCHAR(100) NOT NULL,
    work_title VARCHAR(200),
    section_reference VARCHAR(100),

    -- Content
    original_text TEXT NOT NULL,
    translation TEXT,

    -- Categorization
    theological_topic VARCHAR(100),
    related_book_categories book_category[],
    fourfold_sense sense_type[],            -- Which senses this supports

    -- Relevance scoring
    relevance_keywords TEXT[],
    base_relevance_score INTEGER,

    -- Verse linkages
    directly_referenced_verses INTEGER[],   -- Verses the Father explicitly cites
    thematically_related_verses INTEGER[],  -- Verses with related themes

    -- Processing
    status processing_status DEFAULT 'raw',

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_patristic_father ON patristic_sources(father_name);
CREATE INDEX IF NOT EXISTS idx_patristic_topic ON patristic_sources(theological_topic);
CREATE INDEX IF NOT EXISTS idx_patristic_search ON patristic_sources USING gin(to_tsvector('english',
    COALESCE(original_text, '') || ' ' || COALESCE(translation, '')
));

-- ============================================================================
-- TABLE 9: HERMENEUTICAL_PRINCIPLES
-- Tonal/ordering principles (from Hermeneutical.txt)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hermeneutical_principles (
    id SERIAL PRIMARY KEY,

    -- Identification
    category VARCHAR(100) NOT NULL,         -- "Global Feel", "Local Emotional Honesty"
    principle_name VARCHAR(200),

    -- Content
    principle_text TEXT NOT NULL,
    application_logic TEXT,                 -- How to apply this principle

    -- Examples
    positive_example TEXT,                  -- Correct application
    negative_example TEXT,                  -- What to avoid

    -- Relationships
    applies_to_event_types TEXT[],
    applies_to_verse_categories book_category[],

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Unique constraint for idempotent inserts
    UNIQUE(category, principle_name)
);

-- Populate from Hermeneutical.txt principles (idempotent)
INSERT INTO hermeneutical_principles (category, principle_name, principle_text, application_logic) VALUES
('Global Feel', 'Inevitable Judgment',
 'Keep a constant background sense of inevitable but not yet arrived judgment. Events should feel like fragments drifting toward a catastrophe the reader intuits but cannot fully map.',
 'For each placement, ask: If this were the only thing the reader saw right now, what would they feel, and how will that feeling mutate once the surrounding events are known?'),

('Local vs Global', 'Emotional Honesty Preservation',
 'Let each event keep its own mood intact: joy as joy, terror as terror, banality as banality.',
 'When deciding where an event goes, the question is not "How do I darken this?" but "What do I put before and after it so that its native feeling is still true, yet uneasy in context?"'),

('Local vs Global', 'Anti-Flattening Guard',
 'Guard against flattening: if the internal meter says "This scene now feels less joyful than the text itself," move it until the joy is restored, even if that increases dread elsewhere.',
 'The blood-red sky comes from the whole arrangement, not from repainting each star.'),

('Pattern Pressure', 'Invisible Machinery',
 'Let recognition do the work. The arrangement is not meant to shout "this always goes bad," but to ensure that the reader, on their own, begins to fear the kind of thing they see starting again.',
 'Think in terms of emerging pattern, not formula.'),

('Temporal Dislocation', 'Memory as Dread Carrier',
 'Use non-chronology as emotional shuffling: not solving a puzzle for cleverness sake, but arranging so that memory, not plot, becomes the primary carrier of dread.',
 'When something is moved out of time, ask: Does seeing this now, instead of "when it happened," intensify the readers unease without lying about the scenes own feeling?'),

('Breath and Contrast', 'Load-Bearing Points',
 'Reserve the sharpest contrasts for points meant to feel load-bearing in the moral architecture.',
 'When the gut says "Putting that after this feels almost too much," those are the joints where the blood-red sky thickens.'),

('Memory and Echo', 'Haunting Over Foreshadowing',
 'Think in terms of haunting rather than foreshadowing: the order should make readers feel followed by what they have already seen.',
 'When choosing where to drop a small or obscure event, ask: What earlier feeling do I want this to wake back up?')
ON CONFLICT (category, principle_name) DO NOTHING;

-- ============================================================================
-- TABLE 10: OUTLINE_STRUCTURE
-- Hierarchical outline (from ΒΊΒΛΟΣ ΛΌΓΟΥ REFINED MASTER OUTLINE)
-- ============================================================================

CREATE TABLE IF NOT EXISTS outline_structure (
    id SERIAL PRIMARY KEY,

    -- Hierarchy
    level INTEGER NOT NULL,                 -- 1-7 per project hierarchy
    parent_id INTEGER REFERENCES outline_structure(id),
    sequence_number INTEGER NOT NULL,       -- Order within parent

    -- Content
    title TEXT NOT NULL,
    description TEXT,

    -- Polyglot elements
    greek_text TEXT,
    hebrew_text TEXT,
    latin_text TEXT,
    syriac_text TEXT,

    -- Interdisciplinary connections
    philosophy_connections TEXT[],
    science_connections TEXT[],
    mathematics_connections TEXT[],
    arts_connections TEXT[],

    -- Verse/Event linkages
    linked_verse_ids INTEGER[],
    linked_event_ids INTEGER[],

    -- Page estimates
    estimated_start_page INTEGER,
    estimated_end_page INTEGER,

    -- Content status
    expanded_content TEXT,                  -- Full treatment when expanded
    status processing_status DEFAULT 'raw',

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_outline_parent ON outline_structure(parent_id);
CREATE INDEX IF NOT EXISTS idx_outline_level ON outline_structure(level);

-- ============================================================================
-- TABLE 11: VOCABULARIES
-- Word lists from various vocabulary sources
-- ============================================================================

CREATE TABLE IF NOT EXISTS vocabularies (
    id SERIAL PRIMARY KEY,

    -- Word data
    word VARCHAR(100) NOT NULL,
    normalized_form VARCHAR(100),           -- Lowercase, no diacritics

    -- Sources
    in_ylt BOOLEAN DEFAULT FALSE,
    in_lxx BOOLEAN DEFAULT FALSE,
    in_combined BOOLEAN DEFAULT FALSE,

    -- Polyglot equivalents
    hebrew_equivalent VARCHAR(200),
    greek_equivalent VARCHAR(200),
    latin_equivalent VARCHAR(200),

    -- Semantic information
    semantic_domain VARCHAR(100),
    theological_significance TEXT,

    -- Usage tracking
    verse_occurrences INTEGER[],            -- Array of verse IDs
    usage_count INTEGER DEFAULT 0,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_vocab_word ON vocabularies(normalized_form);
CREATE INDEX IF NOT EXISTS idx_vocab_semantic ON vocabularies(semantic_domain);

-- ============================================================================
-- TABLE 12: THREAD_DENSITY_LOG
-- Track thread density over manuscript (per Stratified.txt bounds: 18-22)
-- ============================================================================

CREATE TABLE IF NOT EXISTS thread_density_log (
    id SERIAL PRIMARY KEY,

    -- Position
    page_start INTEGER NOT NULL,
    page_end INTEGER NOT NULL,

    -- Density calculations
    layer_one_count INTEGER DEFAULT 0,
    layer_two_count INTEGER DEFAULT 0,
    layer_three_count INTEGER DEFAULT 0,
    layer_four_approach_count INTEGER DEFAULT 0,
    layer_four_resonance_count INTEGER DEFAULT 0,
    layer_five_resonance_count INTEGER DEFAULT 0,
    temporal_folding_count INTEGER DEFAULT 0,
    typological_count INTEGER DEFAULT 0,

    -- Calculated total (using weights from Stratified.txt)
    total_density NUMERIC(5,2) GENERATED ALWAYS AS (
        layer_one_count * 1.0 +
        layer_two_count * 1.0 +
        layer_three_count * 1.0 +
        layer_four_approach_count * 1.0 +
        layer_four_resonance_count * 2.0 +
        layer_five_resonance_count * 3.0 +
        temporal_folding_count * 0.5 +
        typological_count * 0.5
    ) STORED,

    -- Bounds check (target: 18-22)
    within_bounds BOOLEAN GENERATED ALWAYS AS (
        (layer_one_count * 1.0 +
         layer_two_count * 1.0 +
         layer_three_count * 1.0 +
         layer_four_approach_count * 1.0 +
         layer_four_resonance_count * 2.0 +
         layer_five_resonance_count * 3.0 +
         temporal_folding_count * 0.5 +
         typological_count * 0.5) BETWEEN 18 AND 22
    ) STORED,

    -- Actions taken
    elements_suspended TEXT[],
    elements_added TEXT[],
    adjustment_notes TEXT,

    -- Audit
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_density_page ON thread_density_log(page_start, page_end);
CREATE INDEX IF NOT EXISTS idx_density_bounds ON thread_density_log(within_bounds);

-- ============================================================================
-- TABLE 13: PROCESSING_BATCHES
-- Track batch processing for resumption
-- ============================================================================

CREATE TABLE IF NOT EXISTS processing_batches (
    id SERIAL PRIMARY KEY,

    -- Batch identification
    batch_number INTEGER NOT NULL,
    batch_type VARCHAR(50) NOT NULL,        -- 'verse', 'event', 'motif', etc.

    -- Scope
    start_verse_id INTEGER,
    end_verse_id INTEGER,
    verse_count INTEGER,

    -- Status
    status processing_status DEFAULT 'raw',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Results
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    failed_verse_ids INTEGER[],

    -- Retry information
    retry_count INTEGER DEFAULT 0,
    last_error TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_batches_status ON processing_batches(status);
CREATE INDEX IF NOT EXISTS idx_batches_type ON processing_batches(batch_type);

-- ============================================================================
-- TABLE 14: CROSS_REFERENCES
-- Scripture cross-references
-- ============================================================================

CREATE TABLE IF NOT EXISTS cross_references (
    id SERIAL PRIMARY KEY,

    -- From verse
    from_verse_id INTEGER NOT NULL REFERENCES verses(id),

    -- To verse
    to_verse_id INTEGER NOT NULL REFERENCES verses(id),

    -- Relationship
    relationship_type VARCHAR(50),          -- 'parallel', 'quotation', 'allusion', 'echo'
    votes INTEGER DEFAULT 0,                -- Confidence score from source

    -- Usage
    used_in_commentary BOOLEAN DEFAULT FALSE,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_xref_from ON cross_references(from_verse_id);
CREATE INDEX IF NOT EXISTS idx_xref_to ON cross_references(to_verse_id);
CREATE INDEX IF NOT EXISTS idx_xref_votes ON cross_references(votes DESC);

-- ============================================================================
-- TABLE 15: METADATA_REGISTRY
-- Scripts, snapshots, failures, and other artifacts
-- ============================================================================

CREATE TABLE IF NOT EXISTS metadata_registry (
    id SERIAL PRIMARY KEY,

    -- Type classification
    item_type VARCHAR(50) NOT NULL,         -- 'script', 'snapshot', 'failure', 'source_file'
    item_name VARCHAR(200) NOT NULL,

    -- Content
    content TEXT,                           -- Full file content for scripts
    description TEXT,

    -- File metadata
    original_path VARCHAR(500),
    file_hash VARCHAR(64),                  -- SHA-256 for deduplication

    -- Status
    status VARCHAR(50) DEFAULT 'active',    -- 'active', 'outdated', 'integrated', 'deprecated'

    -- Relationships
    related_verse_ids INTEGER[],
    related_event_ids INTEGER[],

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metadata_type ON metadata_registry(item_type);
CREATE INDEX IF NOT EXISTS idx_metadata_status ON metadata_registry(status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_metadata_hash ON metadata_registry(file_hash) WHERE file_hash IS NOT NULL;

-- ============================================================================
-- TABLE 16: LITURGICAL_CONNECTIONS
-- Liturgical usage of verses (from Eightfold Methodology)
-- ============================================================================

CREATE TABLE IF NOT EXISTS liturgical_connections (
    id SERIAL PRIMARY KEY,

    verse_id INTEGER NOT NULL REFERENCES verses(id),

    -- Liturgical context
    liturgical_occasion VARCHAR(200),       -- "Paschal Vigil", "Theophany", etc.
    rite_tradition VARCHAR(100),            -- "Byzantine", "Roman", "Syriac", etc.
    lectionary_position VARCHAR(100),

    -- Connection details
    connection_description TEXT NOT NULL,
    theological_significance TEXT,

    -- Source
    source_reference TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_liturgical_verse ON liturgical_connections(verse_id);
CREATE INDEX IF NOT EXISTS idx_liturgical_occasion ON liturgical_connections(liturgical_occasion);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Verses ready for processing (next batch)
CREATE OR REPLACE VIEW vw_next_processing_batch AS
SELECT v.*, cb.name as book_name, cb.category
FROM verses v
JOIN canonical_books cb ON v.book_id = cb.id
WHERE v.status IN ('raw', 'parsed')
ORDER BY cb.canonical_order, v.chapter, v.verse_number
LIMIT 100;

-- View: Current thread density by page range
CREATE OR REPLACE VIEW vw_current_density AS
SELECT
    page_start,
    page_end,
    total_density,
    within_bounds,
    CASE
        WHEN total_density < 18 THEN 'UNDER - can add elements'
        WHEN total_density > 22 THEN 'OVER - must suspend elements'
        ELSE 'OPTIMAL'
    END as density_status
FROM thread_density_log
ORDER BY page_start DESC
LIMIT 50;

-- View: Motifs approaching convergence
CREATE OR REPLACE VIEW vw_approaching_convergences AS
SELECT
    m.*,
    m.convergence_page - m.last_activation_page as pages_to_convergence
FROM motifs m
WHERE m.current_status IN ('reinforcing', 'approaching')
AND m.convergence_page IS NOT NULL
ORDER BY m.convergence_page - m.last_activation_page ASC;

-- View: Hermeneutical event ordering
CREATE OR REPLACE VIEW vw_hermeneutical_order AS
SELECT
    e.id,
    e.part_number,
    e.part_title,
    e.event_number,
    e.event_description,
    e.emotional_weight,
    e.load_bearing,
    v.verse_reference as primary_verse,
    v.text_kjv as verse_text
FROM events e
LEFT JOIN verses v ON e.primary_verse_id = v.id
ORDER BY e.part_number, e.event_number;

-- View: Fourfold sense completion status
CREATE OR REPLACE VIEW vw_fourfold_completion AS
SELECT
    v.verse_reference,
    CASE WHEN v.sense_literal IS NOT NULL THEN 'Complete' ELSE 'Missing' END as literal,
    CASE WHEN v.sense_allegorical IS NOT NULL THEN 'Complete' ELSE 'Missing' END as allegorical,
    CASE WHEN v.sense_tropological IS NOT NULL THEN 'Complete' ELSE 'Missing' END as tropological,
    CASE WHEN v.sense_anagogical IS NOT NULL THEN 'Complete' ELSE 'Missing' END as anagogical,
    (
        (CASE WHEN v.sense_literal IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN v.sense_allegorical IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN v.sense_tropological IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN v.sense_anagogical IS NOT NULL THEN 1 ELSE 0 END)
    ) * 25 as completion_percentage
FROM verses v
ORDER BY v.book_id, v.chapter, v.verse_number;

-- ============================================================================
-- STORED PROCEDURES / FUNCTIONS
-- ============================================================================

-- Function: Calculate canonical position for a verse
CREATE OR REPLACE FUNCTION calculate_canonical_position(
    p_book_order NUMERIC,
    p_chapter INTEGER,
    p_verse INTEGER
) RETURNS NUMERIC AS $$
BEGIN
    RETURN (p_book_order + p_chapter / 100.0 + p_verse / 10000.0) / 67.0;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Calculate orbital resonance position
CREATE OR REPLACE FUNCTION calculate_orbital_position(
    p_planting_page INTEGER,
    p_convergence_page INTEGER,
    p_current_page INTEGER
) RETURNS NUMERIC AS $$
DECLARE
    v_total_distance INTEGER;
    v_current_distance INTEGER;
BEGIN
    v_total_distance := p_convergence_page - p_planting_page;
    v_current_distance := p_current_page - p_planting_page;
    
    IF v_total_distance = 0 THEN
        RETURN 1.0;
    END IF;
    
    RETURN v_current_distance::NUMERIC / v_total_distance::NUMERIC;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Get harmonic reinforcement pages
CREATE OR REPLACE FUNCTION get_harmonic_pages(
    p_planting_page INTEGER,
    p_convergence_page INTEGER
) RETURNS INTEGER[] AS $$
DECLARE
    v_distance INTEGER;
    v_pages INTEGER[];
BEGIN
    v_distance := p_convergence_page - p_planting_page;
    
    -- Per MASTER_PLAN.md: 1/2, 5/6, 15/16 of distance
    v_pages := ARRAY[
        p_planting_page + (v_distance * 0.5)::INTEGER,   -- 1/2
        p_planting_page + (v_distance * 0.833)::INTEGER, -- 5/6
        p_planting_page + (v_distance * 0.9375)::INTEGER -- 15/16
    ];
    
    RETURN v_pages;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Check thread density at a page
CREATE OR REPLACE FUNCTION check_thread_density(p_page INTEGER)
RETURNS TABLE(
    total_density NUMERIC,
    within_bounds BOOLEAN,
    recommendation TEXT
) AS $$
DECLARE
    v_layer1 INTEGER;
    v_layer2 INTEGER;
    v_layer3 INTEGER;
    v_layer4_approach INTEGER;
    v_layer4_resonance INTEGER;
    v_layer5_resonance INTEGER;
    v_temporal INTEGER;
    v_typological INTEGER;
    v_total NUMERIC;
BEGIN
    -- Count active elements at this page
    SELECT COUNT(*) INTO v_layer1 FROM motifs 
    WHERE foundation_layer = 'layer_one' 
    AND p_page BETWEEN planting_page AND convergence_page;
    
    SELECT COUNT(*) INTO v_layer2 FROM motifs 
    WHERE foundation_layer = 'layer_two' 
    AND p_page BETWEEN planting_page AND convergence_page;
    
    SELECT COUNT(*) INTO v_layer3 FROM motifs 
    WHERE foundation_layer = 'layer_three' 
    AND p_page BETWEEN planting_page AND convergence_page;
    
    SELECT COUNT(*) INTO v_layer4_approach FROM motifs 
    WHERE foundation_layer = 'layer_four' 
    AND current_status = 'approaching'
    AND p_page BETWEEN planting_page AND convergence_page;
    
    SELECT COUNT(*) INTO v_layer4_resonance FROM motifs 
    WHERE foundation_layer = 'layer_four' 
    AND current_status = 'converging'
    AND ABS(p_page - convergence_page) < 50;
    
    SELECT COUNT(*) INTO v_layer5_resonance FROM motifs 
    WHERE foundation_layer = 'layer_five' 
    AND current_status = 'converging'
    AND ABS(p_page - convergence_page) < 50;
    
    SELECT COUNT(*) INTO v_temporal FROM typological_correspondences
    WHERE p_page BETWEEN type_page AND antitype_page;
    
    v_typological := v_temporal; -- Simplified; could be separate count
    
    v_total := v_layer1 * 1.0 + v_layer2 * 1.0 + v_layer3 * 1.0 +
               v_layer4_approach * 1.0 + v_layer4_resonance * 2.0 +
               v_layer5_resonance * 3.0 + v_temporal * 0.5 + v_typological * 0.5;
    
    RETURN QUERY SELECT 
        v_total,
        v_total BETWEEN 18 AND 22,
        CASE 
            WHEN v_total < 18 THEN 'Density under minimum. Can add ' || (18 - v_total)::TEXT || ' thread-points.'
            WHEN v_total > 22 THEN 'Density over maximum. Must suspend ' || (v_total - 22)::TEXT || ' thread-points.'
            ELSE 'Density optimal.'
        END;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update timestamp on modification
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply timestamp triggers to all tables (idempotent)
DROP TRIGGER IF EXISTS trg_verses_timestamp ON verses;
CREATE TRIGGER trg_verses_timestamp BEFORE UPDATE ON verses FOR EACH ROW EXECUTE FUNCTION update_timestamp();

DROP TRIGGER IF EXISTS trg_events_timestamp ON events;
CREATE TRIGGER trg_events_timestamp BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_timestamp();

DROP TRIGGER IF EXISTS trg_motifs_timestamp ON motifs;
CREATE TRIGGER trg_motifs_timestamp BEFORE UPDATE ON motifs FOR EACH ROW EXECUTE FUNCTION update_timestamp();

DROP TRIGGER IF EXISTS trg_outline_timestamp ON outline_structure;
CREATE TRIGGER trg_outline_timestamp BEFORE UPDATE ON outline_structure FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Trigger: Auto-calculate canonical position on verse insert/update
CREATE OR REPLACE FUNCTION auto_calculate_canonical_position()
RETURNS TRIGGER AS $$
DECLARE
    v_book_order NUMERIC;
BEGIN
    SELECT canonical_order INTO v_book_order FROM canonical_books WHERE id = NEW.book_id;
    NEW.canonical_position := calculate_canonical_position(v_book_order, NEW.chapter, NEW.verse_number);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_verses_canonical_position ON verses;
CREATE TRIGGER trg_verses_canonical_position
BEFORE INSERT OR UPDATE ON verses
FOR EACH ROW EXECUTE FUNCTION auto_calculate_canonical_position();

-- ============================================================================
-- PRIMARY ORBITAL MOTIFS INITIALIZATION
-- Per MASTER_PLAN.md Layer Five (Bedrock Foundation)
-- ============================================================================

INSERT INTO motifs (name, description, foundation_layer, planting_page, convergence_page, 
                   planting_intensity, convergence_intensity, core_vocabulary, sensory_modalities,
                   current_status, harmonic_ratios) VALUES
-- The Lamb
('The Lamb', 'Sacrificial lamb imagery from Abel through Passover to Revelation',
 'layer_five', 50, 2400, 0.95, 1.0,
 ARRAY['lamb', 'sacrifice', 'blood', 'offering', 'altar', 'slain', 'spotless', 'firstborn'],
 ARRAY['visual', 'tactile', 'olfactory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Wood
('Wood', 'Wood/tree imagery from Eden through the Cross',
 'layer_five', 20, 2200, 0.95, 1.0,
 ARRAY['tree', 'wood', 'branch', 'vine', 'root', 'fruit', 'cross', 'beam'],
 ARRAY['visual', 'tactile'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Silence
('Silence', 'Divine silence and the still small voice',
 'layer_five', 100, 2200, 0.90, 1.0,
 ARRAY['silence', 'still', 'quiet', 'whisper', 'peace', 'rest', 'wait'],
 ARRAY['auditory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- The Binding
('The Binding', 'Binding/bondage imagery from Isaac to Christ',
 'layer_five', 700, 2200, 0.95, 1.0,
 ARRAY['bind', 'bound', 'cord', 'rope', 'chain', 'loose', 'free', 'release'],
 ARRAY['tactile', 'kinesthetic'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Water
('Water', 'Water imagery from creation through baptism',
 'layer_four', 10, 1800, 0.90, 0.95,
 ARRAY['water', 'sea', 'river', 'flood', 'well', 'spring', 'baptize', 'wash'],
 ARRAY['visual', 'tactile', 'auditory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Fire
('Fire', 'Divine fire from burning bush to Pentecost',
 'layer_four', 300, 2050, 0.95, 1.0,
 ARRAY['fire', 'flame', 'burn', 'consume', 'kindle', 'torch', 'light', 'blaze'],
 ARRAY['visual', 'tactile', 'olfactory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Blood
('Blood', 'Blood covenant from Abel to the Cross',
 'layer_five', 50, 2200, 0.95, 1.0,
 ARRAY['blood', 'life', 'covenant', 'sprinkle', 'pour', 'shed', 'redeem'],
 ARRAY['visual', 'tactile'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Bread
('Bread', 'Bread/manna imagery to Eucharist',
 'layer_four', 400, 2100, 0.90, 1.0,
 ARRAY['bread', 'manna', 'grain', 'wheat', 'flour', 'leaven', 'unleavened', 'eat'],
 ARRAY['tactile', 'gustatory', 'olfactory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Shepherd
('Shepherd', 'Shepherd imagery from Abel to Good Shepherd',
 'layer_four', 50, 1900, 0.85, 1.0,
 ARRAY['shepherd', 'sheep', 'flock', 'pasture', 'staff', 'rod', 'fold', 'lamb'],
 ARRAY['visual', 'auditory'], 'planted', ARRAY[0.5, 0.833, 0.9375]),

-- Stone
('Stone', 'Stone imagery from Bethel to cornerstone',
 'layer_four', 750, 2000, 0.85, 0.95,
 ARRAY['stone', 'rock', 'pillar', 'altar', 'cornerstone', 'foundation', 'tablet'],
 ARRAY['visual', 'tactile'], 'planted', ARRAY[0.5, 0.833, 0.9375])
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- IMPLEMENTATION NOTES
-- ============================================================================
-- 
-- This schema implements the complete database architecture for ΒΊΒΛΟΣ ΛΌΓΟΥ:
-- 
-- 1. 16 Core Tables covering verses, events, motifs, patristics, vocabularies
-- 2. Complete Enumerated Types for processing states and categories
-- 3. Fourfold Sense Integration (Literal 30%, Allegorical 25%, Tropological 25%, Anagogical 20%)
-- 4. Nine-Matrix Elements per Stratified Foundation System
-- 5. Orbital Resonance Tracking with harmonic ratio calculations
-- 6. Thread Density Management (target bounds: 18-22)
-- 7. Tonal Adjustment per Hermeneutical.txt principles
-- 8. Primary Orbital Motifs (Layer 4-5) pre-seeded
-- 9. Views for common queries and status tracking
-- 10. Functions for canonical positioning and density calculations
-- 11. Triggers for automatic timestamp and position updates
-- 
-- Target deployment: PostgreSQL 14+
-- Estimated verse count: 37,454+
-- Estimated page count: 2,500+
-- 
-- ============================================================================
