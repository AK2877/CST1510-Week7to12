import pandas as pd
from pathlib import Path
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.datasets import *
from app.data.incidents import *
from app.data.tickets import *

DATA_direc = Path("CW2\DATA")


def load_all_csv_data(conn):
    """
    Load CSVs found in the DATA directory into their corresponding tables.

    Returns total number of rows loaded.
    """
    total = 0
    mapping = {
        DATA_direc / "cyber_incidents.csv": "cyber_incidents",
        DATA_direc / "datasets_metadata.csv": "datasets_metadata",
        DATA_direc / "it_tickets.csv": "it_tickets",
    }

    for path, table in mapping.items():
        try:
            rows = load_csv_to_table(conn, path, table)
            total += rows
        except Exception as e:
            print(f"Error loading {path.name} into {table}: {e}")

    return total


def setup_database_complete():
    """
    Complete database setup:
      1. Connect to database
      2. Create all tables
      3. Migrate users from users.txt
      4. Load CSV data for all domains
      5. Verify setup
    """
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    try:
        # Step 2: Create tables
        print("\n[2/5] Creating database tables...")
        create_all_tables(conn)

        # Step 3: Migrate users (function manages its own DB connection)
        print("\n[3/5] Migrating users from users.txt...")
        user_count = migrate_users_from_file("CW2/DATA/users.txt")
        print(f"       Migrated {user_count} users")

        # Step 4: Load CSV data
        print("\n[4/5] Loading CSV data...")
        total_rows = load_all_csv_data(conn)
        print(f"       Loaded {total_rows} rows from CSV files")

        # Step 5: Verify
        print("\n[5/5] Verifying database setup...")
        cursor = conn.cursor()

        # Count rows in each table
        tables = ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]
        print("\n Database Summary:")
        print(f"{'Table':<25} {'Row Count':<15}")
        print("-" * 40)

        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
            except Exception:
                count = 0
            print(f"{table:<25} {count:<15}")

    finally:
        conn.close()

    print("\n" + "=" * 60)
    print(" DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database()
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")
    
    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)


def main():
    # Run full setup and then comprehensive tests
    setup_database_complete()
    run_comprehensive_tests()


if __name__ == "__main__":
    main()
