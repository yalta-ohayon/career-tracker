CREATE TABLE IF NOT EXISTS companies (
    id      INTEGER PRIMARY KEY AUTOINCREMENT, --מספר מזהה ייחודי לכל חברה 
    name    TEXT NOT NULL UNIQUE,--אומר שאי אפשר להכניס את אותה חברה פעמיים 
    field   TEXT -- תחום עיסוק של החברה 
);

CREATE TABLE IF NOT EXISTS positions(
    id          INTEGER PRIMARY KEY AUTOINCREMENT, --מספר מזהה ייחודי לכל משרה 
    title       TEXT NOT NULL, --שם המשרה 
    description TEXT, --תיאור המשרה 
    company_id  INTEGER NOT NULL, --מזהה החברה שמציעה את המשרה 
    FOREIGN KEY (company_id) REFERENCES companies(id)   
);

CREATE TABLE IF NOT EXISTS applications(
    id          INTEGER PRIMARY KEY AUTOINCREMENT, --מספר מזהה ייחודי לכל בקשה 
    position_id INTEGER NOT NULL, --מזהה המשרה אליה נשלחה הבקשה 
    applied_date TEXT NOT NULL, --תאריך שליחת הבקשה
    status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'in_process', 'interview', 'offer', 'rejected', 'closed')),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --תאריך עדכון אחרון של הבקשה
    notes       TEXT,-- הערות חופשיות
    FOREIGN KEY (position_id) REFERENCES positions(id)
);
