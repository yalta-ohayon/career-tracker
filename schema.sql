-- Career Tracker database schema

CREATE TABLE IF NOT EXISTS companies (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- unique company id
    name    TEXT NOT NULL UNIQUE,               -- company name, no duplicates
    field   TEXT                                -- industry, e.g. Cyber
);

CREATE TABLE IF NOT EXISTS positions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- unique position id
    title       TEXT NOT NULL,                      -- job title
    description TEXT,                               -- optional job description
    company_id  INTEGER NOT NULL,                   -- company offering the position
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS applications (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,  -- unique application id
    position_id  INTEGER NOT NULL,                   -- position applied to
    applied_date TEXT NOT NULL,                      -- YYYY-MM-DD
    status       TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_process', 'interview', 'offer', 'rejected', 'closed')),
    updated_date TIMESTAMP DEFAULT (datetime('now', 'localtime')),  -- last update
    notes        TEXT,                               -- free text notes
    FOREIGN KEY (position_id) REFERENCES positions(id)
);