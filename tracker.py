from database import get_connection

STATUSES = ("pending", "in_process", "interview", "offer", "rejected", "closed")


# ---------- Adding data ----------

def add_company(name, field=None):
    """Add a new company and return its id."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO companies (name, field) VALUES (?, ?)",
        (name, field)
    )
    conn.commit()
    company_id = cursor.lastrowid
    conn.close()
    return company_id


def find_or_add_company(name, field=None):
    """Return the id of an existing company, or add it if it is new."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM companies WHERE name = ? COLLATE NOCASE",
        (name,)
    ).fetchone()
    conn.close()
    if row:
        return row[0]
    return add_company(name, field)


def add_position(title, company_id, description=None):
    """Add a new position and return its id."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO positions (title, company_id, description) VALUES (?, ?, ?)",
        (title, company_id, description)
    )
    conn.commit()
    position_id = cursor.lastrowid
    conn.close()
    return position_id


def add_application(position_id, applied_date, notes=None):
    """Add a new application and return its id."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO applications (position_id, applied_date, notes) VALUES (?, ?, ?)",
        (position_id, applied_date, notes)
    )
    conn.commit()
    application_id = cursor.lastrowid
    conn.close()
    return application_id


# ---------- Updating data ----------

def update_status(application_id, new_status, note=None):
    """Update an application's status. Returns True if the application exists."""
    conn = get_connection()
    cursor = conn.execute(
        """UPDATE applications
           SET status = ?,
               updated_date = datetime('now', 'localtime'),
               notes = CASE WHEN ? IS NULL THEN notes
                            WHEN notes IS NULL THEN ?
                            ELSE notes || ' | ' || ? END
           WHERE id = ?""",
        (new_status, note, note, note, application_id)
    )
    conn.commit()
    found = cursor.rowcount > 0
    conn.close()
    return found


# ---------- Reading data ----------

def list_applications():
    """Return all applications with company and position names."""
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
    """Return all applications with a given status."""
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


# ---------- Statistics ----------

def count_by_status():
    """Return (status, count) pairs, most common first."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT status, COUNT(*) AS total
           FROM applications
           GROUP BY status
           ORDER BY total DESC"""
    ).fetchall()
    conn.close()
    return rows


def stats_by_company():
    """Return (company, total, rejected, still_open, progressed) per company."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.name,
                  COUNT(a.id) AS total,
                  SUM(a.status = 'rejected') AS rejected,
                  SUM(a.status = 'pending') AS still_open,
                  SUM(a.status IN ('in_process', 'interview', 'offer')) AS progressed
           FROM companies c
           JOIN positions p ON p.company_id = c.id
           JOIN applications a ON a.position_id = p.id
           GROUP BY c.id
           ORDER BY total DESC, c.name"""
    ).fetchall()
    conn.close()
    return rows


def response_rate():
    """Return (total, answered, percent) - how many applications got any reply."""
    conn = get_connection()
    total, answered = conn.execute(
        """SELECT COUNT(*), SUM(status != 'pending') FROM applications"""
    ).fetchone()
    conn.close()
    answered = answered or 0
    percent = round(100 * answered / total) if total else 0
    return total, answered, percent