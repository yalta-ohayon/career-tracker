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

if __name__ == "__main__":
    claroty_id = add_company("Claroty", "Cyber")
    print("Added company with id:", claroty_id)


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
