# ingest_land_ownership.py
# Purpose: Fetch Oregon public land ownership and management boundaries
# and load into PostGIS oregon_land_ownership_raw table
# Source: Oregon GeoHub - Ownership Land Management
# Note: Polygons show public land by managing agency, everything else is private
# Note: API limit is 2000 records - batching at 500 for reliability
# Run: python3 pipelines/ingest_land_ownership.py

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
import time

# Oregon Land Ownership REST API
BASE_URL = "https://services.arcgis.com/uUvqNMGPm7axC2dD/ArcGIS/rest/services/Ownership_Land_Management/FeatureServer/0/query"
WHERE = "1%3D1"
BATCH_SIZE = 500
MAX_RETRIES = 3
RETRY_DELAY = 5

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

def ingest_land_ownership():
    print("Fetching Oregon land ownership data...")

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

        time.sleep(1)

    # Combine all batches
    combined = pd.concat(all_gdfs, ignore_index=True)
    combined = gpd.GeoDataFrame(combined, geometry='geometry', crs='EPSG:4326')

    print(f"Total features downloaded: {len(combined)}")

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
        name="oregon_land_ownership_raw",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Done! {len(combined)} features loaded into PostGIS table: oregon_land_ownership_raw")

if __name__ == "__main__":
    ingest_land_ownership()