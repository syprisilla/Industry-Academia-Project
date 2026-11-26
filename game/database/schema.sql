-- Syllables are stored in Korean (사 서 세 소 수 스 시); target_words uses "syllable" in place of vowel_environment.
CREATE TABLE IF NOT EXISTS children (
    child_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT UNIQUE NOT NULL,  -- the game only knows a child by the entered name
    core_word TEXT,
    vowel_environment TEXT REFERENCES reference_stats(syllable)  -- stable: clearest syllable from the assessment
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id    INTEGER REFERENCES children(child_id),
    mode        TEXT,                -- to be decided by the team
    boss_result TEXT                 -- clear / fail
);

CREATE TABLE IF NOT EXISTS target_words (
    word_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    word_text        TEXT NOT NULL,
    chapter          INTEGER,        -- NULL for core words
    difficulty_level TEXT,           -- m1 / m2 / m3, NULL for core words
    syllable         TEXT REFERENCES reference_stats(syllable),
    pool_type        TEXT            -- core / target
);

CREATE TABLE IF NOT EXISTS attempt_log (
    attempt_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id        INTEGER REFERENCES sessions(session_id),
    word_id           INTEGER REFERENCES target_words(word_id),  -- NULL for the boss sentence
    word_text         TEXT,
    set_number        INTEGER,       -- monster round: which hit (1~3) the child is aiming for
    attempt_number    INTEGER,       -- try number within that round
    result            TEXT,          -- success / fail / unrecognized
    cog               REAL,
    spectral_variance REAL
);

CREATE TABLE IF NOT EXISTS reference_stats (
    syllable      TEXT PRIMARY KEY,
    cog_mean      REAL,
    cog_sd        REAL,
    variance_mean REAL,
    variance_sd   REAL
);
