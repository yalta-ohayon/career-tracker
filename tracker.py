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


if __name__ == "__main__":
    pos_id = add_position("Software Engineer - Student", 1)
    print("Added position with id:", pos_id)

    app_id = add_application(pos_id, "2026-10-04", "Applied via company website")
    print("Added application with id:", app_id)

    ok = update_status(app_id, "interview")
    print("Status updated:", ok)

    ok = update_status(999, "offer")
    print("Update non-existing application:", ok)