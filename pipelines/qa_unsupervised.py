# qa_unsupervised.py
# Purpose: Automated QA checks for Oregon Offroad spatial pipeline
# Checks geometry validity, null values, row counts, and data extent
# Run: python3 pipelines/qa_unsupervised.py

import psycopg2
from datetime import datetime

# PostGIS connection
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gis_practice"
DB_USER = "postgres"
DB_PASS = "Portland11!"

# Expected row counts
EXPECTED_COUNTS = {
    "oregon_counties": 36,
    "oregon_trails": 8522,
    "oregon_land_ownership": 3266
}

# Oregon bounding box (minx, miny, maxx, maxy)
OREGON_BBOX = (-124.703816, 41.885734, -116.463176, 46.292)

# Known valid land managers
VALID_LAND_MANAGERS = [
    'BLM', 'USFS', 'OPRD', 'NPS', 'ODFW', 'ODF', 'ODSL',
    'DOD', 'TRIBAL', 'ODOT', 'BIA', 'USBR', 'USACE',
    'PVI', 'PNI', 'PV', 'FEE', 'WATER', 'Water',
    'BPA', 'DOE', 'FAA', 'GSA', 'LG', 'OR', 'OSU',
    'OUS', 'USDA', 'ODFODSL', 'FWS'
]

def run_check(cursor, name, query, expected=None):
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if expected is not None:
        passed = result == expected
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {result} (expected {expected})")
    else:
        passed = result == 0
        status = "✅" if passed else "⚠️ WARNING"
        print(f"  {status} {name}: {result}")
    return passed

def qa_counties(cursor):
    print("\noregon_counties")
    print("-" * 40)

    run_check(cursor, "Row count",
        "SELECT COUNT(*) FROM oregon_counties",
        expected=EXPECTED_COUNTS["oregon_counties"])

    run_check(cursor, "Null geometries",
        "SELECT COUNT(*) FROM oregon_counties WHERE geom IS NULL")

    run_check(cursor, "Invalid geometries",
        "SELECT COUNT(*) FROM oregon_counties WHERE NOT ST_IsValid(geom)")

    run_check(cursor, "Null county names",
        "SELECT COUNT(*) FROM oregon_counties WHERE county_name IS NULL")

    run_check(cursor, "Null cobcodes",
        "SELECT COUNT(*) FROM oregon_counties WHERE cobcode IS NULL")

    run_check(cursor, "Features outside Oregon extent",
        f"""SELECT COUNT(*) FROM oregon_counties 
        WHERE NOT ST_Intersects(geom, 
        ST_MakeEnvelope({OREGON_BBOX[0]}, {OREGON_BBOX[1]}, 
        {OREGON_BBOX[2]}, {OREGON_BBOX[3]}, 4326))""")

def qa_trails(cursor):
    print("\noregon_trails")
    print("-" * 40)

    run_check(cursor, "Row count",
        "SELECT COUNT(*) FROM oregon_trails",
        expected=EXPECTED_COUNTS["oregon_trails"])

    run_check(cursor, "Null geometries",
        "SELECT COUNT(*) FROM oregon_trails WHERE geom IS NULL")

    run_check(cursor, "Invalid geometries",
        "SELECT COUNT(*) FROM oregon_trails WHERE NOT ST_IsValid(geom)")

    run_check(cursor, "Null trail names",
        "SELECT COUNT(*) FROM oregon_trails WHERE trail_name IS NULL")

    run_check(cursor, "Null terra_motorized",
        "SELECT COUNT(*) FROM oregon_trails WHERE terra_motorized IS NULL")

    run_check(cursor, "Features outside Oregon extent",
        f"""SELECT COUNT(*) FROM oregon_trails 
        WHERE NOT ST_Intersects(geom, 
        ST_MakeEnvelope({OREGON_BBOX[0]}, {OREGON_BBOX[1]}, 
        {OREGON_BBOX[2]}, {OREGON_BBOX[3]}, 4326))""")

def qa_land_ownership(cursor):
    print("\noregon_land_ownership")
    print("-" * 40)

    run_check(cursor, "Row count",
        "SELECT COUNT(*) FROM oregon_land_ownership",
        expected=EXPECTED_COUNTS["oregon_land_ownership"])

    run_check(cursor, "Null geometries",
        "SELECT COUNT(*) FROM oregon_land_ownership WHERE geom IS NULL")

    run_check(cursor, "Invalid geometries",
        "SELECT COUNT(*) FROM oregon_land_ownership WHERE NOT ST_IsValid(geom)")

    run_check(cursor, "Null land managers",
        "SELECT COUNT(*) FROM oregon_land_ownership WHERE land_manager IS NULL")

    run_check(cursor, "Features outside Oregon extent",
        f"""SELECT COUNT(*) FROM oregon_land_ownership 
        WHERE NOT ST_Intersects(geom, 
        ST_MakeEnvelope({OREGON_BBOX[0]}, {OREGON_BBOX[1]}, 
        {OREGON_BBOX[2]}, {OREGON_BBOX[3]}, 4326))""")

def main():
    print("=" * 40)
    print(f"QA REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    qa_counties(cursor)
    qa_trails(cursor)
    qa_land_ownership(cursor)

    cursor.close()
    conn.close()

    print("\n" + "=" * 40)
    print("QA complete.")
    print("=" * 40)

if __name__ == "__main__":
    main()