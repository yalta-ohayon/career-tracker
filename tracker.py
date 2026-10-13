from database import get_connection

def add_company(name, field=None):
    """מוסיפה חברה חדשה ומחזירה את המספר המזהה שלה"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO companies (name, field) VALUES (?, ?)",
        (name, field)
    )
    conn.commit()
    company_id = cursor.lastrowid
    conn.close()
    return company_id


def add_position(title, company_id, description=None):
    """מוסיפה משרה חדשה ומחזירה את המספר המזהה שלה"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO positions (title, company_id, description) VALUES (?, ?, ?)",
        (title, company_id, description)
    )
    conn.commit()
    position_id = cursor.lastrowid
    conn.close()
    return position_id


def update_status(application_id, new_status):
    """מעדכנת סטטוס של הגשה. מחזירה True אם ההגשה נמצאה"""
    conn = get_connection()
    cursor = conn.execute(
        """UPDATE applications
           SET status = ?, updated_date = datetime('now', 'localtime')
           WHERE id = ?""",
        (new_status, application_id)
    )
    conn.commit()
    found = cursor.rowcount > 0
    conn.close()
    return found


def add_application(position_id, applied_date, notes=None):
    """מוסיפה הגשה חדשה ומחזירה את המספר המזהה שלה"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO applications (position_id, applied_date, notes) VALUES (?, ?, ?)",
        (position_id, applied_date, notes)
    )
    conn.commit()
    application_id = cursor.lastrowid
    conn.close()
    return application_id


def list_applications():
    """מחזירה את כל ההגשות עם שם החברה ושם המשרה"""
    conn = get_connection()
    rows = conn.execute(
        """SELECT a.id, c.name, p.title, a.applied_date, a.status
           FROM applications a
           JOIN positions p ON a.position_id = p.id
           JOIN companies c ON p.company_id = c.id
           ORDER BY a.applied_date DESC"""
    ).fetchall()
    conn.close()
    return rows

def list_by_status(status):
    """מחזירה את כל ההגשות עם סטטוס מסוים"""
    conn = get_connection()
    rows = conn.execute(
        """SELECT a.id, c.name, p.title, a.applied_date, a.status
           FROM applications a
           JOIN positions p ON a.position_id = p.id
           JOIN companies c ON p.company_id = c.id
           WHERE a.status = ?
           ORDER BY a.applied_date DESC""",
        (status,)
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print("Interviews:")
    for app in list_by_status("interview"):
        print(app)

    print("Rejected:")
    for app in list_by_status("rejected"):
        print(app)