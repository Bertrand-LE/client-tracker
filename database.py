import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tracker.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            duration_hours REAL NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


# ── Clients ──────────────────────────────────────────────────────────────────

def get_all_clients():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM clients ORDER BY name COLLATE NOCASE").fetchall()
    conn.close()
    return rows


def get_client(client_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
    conn.close()
    return row


def create_client(name, notes):
    conn = get_connection()
    conn.execute("INSERT INTO clients (name, notes) VALUES (?, ?)", (name, notes))
    conn.commit()
    conn.close()


def update_client(client_id, name, notes):
    conn = get_connection()
    conn.execute("UPDATE clients SET name = ?, notes = ? WHERE id = ?", (name, notes, client_id))
    conn.commit()
    conn.close()


def delete_client(client_id):
    conn = get_connection()
    conn.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()


# ── Interventions ─────────────────────────────────────────────────────────────

INTERVENTION_TYPES = [
    "Ticket",
    "Vergadering",
    "Ter plaatse",
    "Remote sessie",
    "Telefoongesprek",
    "Overig",
]


def get_interventions_this_month():
    conn = get_connection()
    rows = conn.execute("""
        SELECT i.*, c.name AS client_name
        FROM interventions i
        JOIN clients c ON c.id = i.client_id
        WHERE strftime('%Y-%m', i.date) = strftime('%Y-%m', 'now')
        ORDER BY i.date DESC, i.created_at DESC
    """).fetchall()
    conn.close()
    return rows


def get_interventions_for_month(year, month, client_id=None):
    period = f"{year:04d}-{month:02d}"
    conn = get_connection()
    if client_id:
        rows = conn.execute("""
            SELECT i.*, c.name AS client_name
            FROM interventions i
            JOIN clients c ON c.id = i.client_id
            WHERE strftime('%Y-%m', i.date) = ?
              AND i.client_id = ?
            ORDER BY c.name COLLATE NOCASE, i.date
        """, (period, client_id)).fetchall()
    else:
        rows = conn.execute("""
            SELECT i.*, c.name AS client_name
            FROM interventions i
            JOIN clients c ON c.id = i.client_id
            WHERE strftime('%Y-%m', i.date) = ?
            ORDER BY c.name COLLATE NOCASE, i.date
        """, (period,)).fetchall()
    conn.close()
    return rows


def get_interventions_for_week(start_date, end_date):
    conn = get_connection()
    rows = conn.execute("""
        SELECT i.*, c.name AS client_name
        FROM interventions i
        JOIN clients c ON c.id = i.client_id
        WHERE i.date BETWEEN ? AND ?
        ORDER BY i.date DESC, i.created_at DESC
    """, (start_date, end_date)).fetchall()
    conn.close()
    return rows


def get_intervention(intervention_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT i.*, c.name AS client_name
        FROM interventions i
        JOIN clients c ON c.id = i.client_id
        WHERE i.id = ?
    """, (intervention_id,)).fetchone()
    conn.close()
    return row


def create_intervention(client_id, date, type_, title, duration_hours, notes):
    conn = get_connection()
    conn.execute("""
        INSERT INTO interventions (client_id, date, type, title, duration_hours, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_id, date, type_, title, duration_hours, notes))
    conn.commit()
    conn.close()


def update_intervention(intervention_id, client_id, date, type_, title, duration_hours, notes):
    conn = get_connection()
    conn.execute("""
        UPDATE interventions
        SET client_id = ?, date = ?, type = ?, title = ?, duration_hours = ?, notes = ?
        WHERE id = ?
    """, (client_id, date, type_, title, duration_hours, notes, intervention_id))
    conn.commit()
    conn.close()


def delete_intervention(intervention_id):
    conn = get_connection()
    conn.execute("DELETE FROM interventions WHERE id = ?", (intervention_id,))
    conn.commit()
    conn.close()
