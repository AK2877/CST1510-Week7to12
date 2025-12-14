"""
From Week 8 
"""

import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.incidents import load_csv_to_table


def load_datasets_csv(conn, csv_path):
    """Load datasets_metadata.csv into the datasets_metadata table."""
    return load_csv_to_table(conn, csv_path, "datasets_metadata")


def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert a new dataset metadata record."""
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
    )
    conn.commit()
    return cur.lastrowid


def get_all_datasets(conn):
    """Return a DataFrame of all datasets."""
    return pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)


def update_dataset_record_count(conn, dataset_id, new_count):
    """Update record_count for a dataset."""
    cur = conn.cursor()
    cur.execute(
        "UPDATE datasets_metadata SET record_count = ? WHERE id = ?",
        (new_count, dataset_id)
    )
    conn.commit()
    return cur.rowcount


def delete_dataset(conn, dataset_id):
    """Delete a dataset by ID."""
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    conn.commit()
    return cur.rowcount
