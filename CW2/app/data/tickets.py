import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.incidents import load_csv_to_table


def load_tickets_csv(conn, csv_path):
    """Load it_tickets.csv into the it_tickets table."""
    return load_csv_to_table(conn, csv_path, "it_tickets")


def insert_ticket(conn, ticket_id, priority, status, category, subject, description,
                  created_date, resolved_date, assigned_to):
    """Insert a new IT ticket record."""
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description,
         created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (ticket_id, priority, status, category, subject, description,
         created_date, resolved_date, assigned_to)
    )
    conn.commit()
    return cur.lastrowid


def get_all_tickets(conn):
    """Return a DataFrame of all tickets."""
    return pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)


def update_ticket_status(conn, ticket_id, new_status):
    """Update the status of an IT ticket."""
    cur = conn.cursor()
    cur.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    return cur.rowcount


def delete_ticket(conn, ticket_id):
    """Delete a ticket by ticket_id."""
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    return cur.rowcount
