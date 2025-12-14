"""
From Week 8
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("Final_project\DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database and return a connection object.
    - Enables foreign key support (PRAGMA foreign_keys = ON).
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
