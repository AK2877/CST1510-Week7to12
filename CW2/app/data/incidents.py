import pandas as pd
from pathlib import Path
from app.data.db import connect_database


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"⚠️  CSV not found: {csv_path}, {table_name} can't be loaded.")
        return 0

    df = pd.read_csv(csv_path)

    # If we're loading incidents, validate 'reported_by' values against users table
    if table_name == "cyber_incidents" and "reported_by" in df.columns:
        try:
            cur = conn.cursor()
            cur.execute("SELECT username FROM users")
            users = {row[0] for row in cur.fetchall() if row[0] is not None}
        except Exception:
            users = set()

        if users:
            # Replace any reported_by not in users with None (so it becomes NULL)
            df["reported_by"] = df["reported_by"].apply(
                lambda v: v if pd.notna(v) and str(v).strip() in users else None
            )
        else:
            # If no users exist, nullify all reported_by entries
            df["reported_by"] = None

    # avoid UNIQUE constraint errors
    if table_name == "it_tickets" and "ticket_id" in df.columns:
        # drop duplicates inside CSV by ticket_id
        before_len = len(df)
        df = df.drop_duplicates(subset=["ticket_id"], keep="first")
        dropped_in_csv = before_len - len(df)

        # query existing ticket_ids in DB and remove those rows from df
        try:
            cur = conn.cursor()
            cur.execute("SELECT ticket_id FROM it_tickets")
            existing = {row[0] for row in cur.fetchall() if row[0] is not None}
        except Exception:
            existing = set()

        if existing:
            df_before_existing_filter = len(df)
            df = df[df["ticket_id"].isin(existing)]
            skipped_due_to_existing = df_before_existing_filter - len(df)
        else:
            skipped_due_to_existing = 0

        if dropped_in_csv or skipped_due_to_existing:
            print(f"  - it_tickets: dropped {dropped_in_csv} duplicate rows from CSV; "
                  f"skipped {skipped_due_to_existing} rows that already exist in DB.")

    # Append to SQL table
    if len(df) == 0:
        print(f"No new rows to insert into {table_name} from {csv_path.name}.")
        return 0

    df.to_sql(
        name=table_name,
        con=conn,
        if_exists="append",
        index=False
    )

    row_cnt = len(df)
    print(f"✅ Loaded {row_cnt} rows from {csv_path.name} into {table_name}.")
    return row_cnt


def load_incidents_csv(conn, csv_path):
    """Load cyber_incidents.csv into the cyber_incidents table."""
    return load_csv_to_table(conn, csv_path, "cyber_incidents")
    

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.

    Returns:
        int: ID of the inserted incident
    """

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    conn.commit()
    return cursor.lastrowid


def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.

    Returns:
        pandas.DataFrame: All incidents
    """
    return pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )


def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    """

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )

    conn.commit()
    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    """

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )

    conn.commit()
    return cursor.rowcount


def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))


if __name__ == "__main__":
    conn = connect_database()

    print("\nIncidents by Type:")
    print(get_incidents_by_type_count(conn))

    print("\nHigh Severity Incidents by Status:")
    print(get_high_severity_by_status(conn))

    print("\nIncident Types with Many Cases (>5):")
    print(get_incident_types_with_many_cases(conn, min_count=5))

    conn.close()
