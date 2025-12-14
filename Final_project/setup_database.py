"""
This script sets up the database for the Multi-Domain Intelligence Platform.
It creates all the necessary tables.
Only need to execute once at the start to avoide any database creation errors but not necessory
"""

import sqlite3
import bcrypt
import os
from pathlib import Path

def setup_database():

    """Creates all required database tables."""
    
    DB_PATH = Path("Final_project\DATA") / "intelligence_platform.db"
    
    # Create DATA directory if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Setting up database at: {DB_PATH}")
    
    # Connect to the database
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create users table
    print("Creating users table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)
    
    # Create cyber incidents table
    print("Creating cyber_incidents table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT
    )
    """)
    
    # Create datasets metadata table
    print("Creating datasets_metadata table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT,
        category TEXT,
        source TEXT,
        last_updated DATE,
        record_count INTEGER,
        file_size_mb REAL
    )
    """)
    
    # Create it tickets table
    print("Creating it_tickets table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT,
        description TEXT,
        created_date DATE,
        resolved_date DATE,
        assigned_to TEXT
    )
    """)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database setup complete!")
    print("Using DB:", os.path.abspath(DB_PATH))

if __name__ == "__main__":
    setup_database()