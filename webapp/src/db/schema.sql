CREATE TABLE IF NOT EXISTS party_event(
            event_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            is_approved INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)