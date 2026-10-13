import sqlite3 

DB_FILE = "career.db"        # השם של קובץ בסיס הנתונים
SCHEMA_FILE = "schema.sql"   # הקובץ עם הטבלאות שכתבת


def get_connection():
    """פותחת חיבור לבסיס הנתונים"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")  # מפעיל בדיקה של מפתחות זרים
    return conn


def init_db():
    """יוצרת את הטבלאות מתוך schema.sql"""
    # 1. קוראים את כל התוכן של schema.sql
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        sql = f.read()

    # 2. פותחים חיבור לבסיס הנתונים
    conn = get_connection()

    # 3. מריצים את כל פקודות ה-SQL וסוגרים
    conn.executescript(sql)
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database created!")
