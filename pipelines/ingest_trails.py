# ingest_trails.py
# Purpose: Fetch USFS National Forest System Trails for Oregon region
# and load into PostGIS oregon_trails_raw table
# Source: USFS ArcGIS REST API
# Filter: SECURITY_ID 0601-0622 (Oregon/Washington region)
# Note: API limit is 2000 records per request - script paginates automatically
# Note: Will be further filtered to Oregon via spatial join with oregon_counties_raw
# Run: python3 pipelines/ingest_trails.py

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
import time

# USFS REST API base URL
BASE_URL = "https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query"
WHERE = "SECURITY_ID+IN+('0601','0602','0603','0605','0606','0607','0609','0610','0612','0614','0615','0616','0617','0618','0621','0622')"
BATCH_SIZE = 500
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# PostGIS connection
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gis_practice"
DB_USER = "postgres"
DB_PASS = "Portland11!"

def fetch_batch(url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            gdf = gpd.read_file(url)
            return gdf
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"  Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
    print("  Max retries reached, skipping batch.")
    return None

def ingest_trails():
    print("Fetching USFS trails for Oregon region (paginated)...")

    all_gdfs = []
    offset = 0

    while True:
        url = f"{BASE_URL}?where={WHERE}&outFields=*&resultOffset={offset}&resultRecordCount={BATCH_SIZE}&f=geojson"
        print(f"Fetching records {offset} to {offset + BATCH_SIZE}...")

        gdf = fetch_batch(url)

        if gdf is None or len(gdf) == 0:
            print("No more records — pagination complete.")
            break

        all_gdfs.append(gdf)
        offset += BATCH_SIZE

        if len(gdf) < BATCH_SIZE:
            print("Last batch received.")
            break

        # Small delay between requests to be respectful of the API
        time.sleep(1)

    # Combine all batches
    combined = pd.concat(all_gdfs, ignore_index=True)
    combined = gpd.GeoDataFrame(combined, geometry='geometry', crs='EPSG:4326')

    print(f"Total trails downloaded: {len(combined)}")

    # Reproject if needed
    if combined.crs.to_epsg() != 4326:
        print("Reprojecting to EPSG:4326...")
        combined = combined.to_crs(epsg=4326)

    # Connect to PostGIS
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("Loading into PostGIS...")

    combined.to_postgis(
        name="oregon_trails_raw",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Done! {len(combined)} USFS trails loaded into PostGIS table: oregon_trails_raw")

if __name__ == "__main__":
    ingest_trails()