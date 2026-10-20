import sqlite3

DB_FILE = "career.db"        # database file name
SCHEMA_FILE = "schema.sql"   # table definitions


def get_connection():
    """Open a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
    return conn


def init_db():
    """Create the tables from schema.sql (safe to run more than once)."""
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        sql = f.read()
    conn = get_connection()
    conn.executescript(sql)
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database created!")