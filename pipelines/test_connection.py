# test_connection.py
# Purpose: Verify Python can connect to local PostGIS database
# Run: python3 pipelines/test_connection.py

import psycopg2
from sqlalchemy import create_engine, text

# Connection settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gis_practice"
DB_USER = "postgres"
DB_PASS = "Portland11!"

def test_connection():
    print("Testing PostGIS connection...")
    
    # Connect using psycopg2
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    
    cursor = conn.cursor()
    
    # Check PostGIS version
    cursor.execute("SELECT PostGIS_Version();")
    version = cursor.fetchone()
    print(f"PostGIS Version: {version[0]}")
    
    # List our tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    print("\nTables in gis_practice:")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\nConnection successful!")

if __name__ == "__main__":
    test_connection()