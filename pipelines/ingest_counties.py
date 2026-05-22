# ingest_counties.py
# Purpose: Fetch Oregon county boundaries from Oregon GeoHub REST API
# and load them into PostGIS oregon_counties table
# Source: https://oregonexplorer.info
# Run: python3 pipelines/ingest_counties.py

import geopandas as gpd
import sqlalchemy
from sqlalchemy import create_engine, text
import requests

# Oregon GeoHub - County Boundaries REST API
URL = "https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services/BLM_OR_County_Boundaries_Polygon_Hub/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson"

# PostGIS connection
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gis_practice"
DB_USER = "postgres"
DB_PASS = "Portland11!"

def ingest_counties():
    print("Fetching Oregon county boundaries from Oregon GeoHub...")
    
    # Read GeoJSON directly from REST API into a GeoDataFrame
    gdf = gpd.read_file(URL)
    
    print(f"Downloaded {len(gdf)} counties")
    print(f"Columns: {list(gdf.columns)}")
    print(f"CRS: {gdf.crs}")

    # Filter to Oregon counties only
    gdf = gdf[gdf['COBCODE'].str.startswith('OR')]
    print(f"Filtered to {len(gdf)} Oregon counties")
    
    # Reproject to WGS84 (EPSG:4326) if needed
    if gdf.crs.to_epsg() != 4326:
        print("Reprojecting to EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)
    
    # Connect to PostGIS
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    print("Loading into PostGIS...")
    
    # Write to PostGIS - replace existing data
    gdf.to_postgis(
        name="oregon_counties_raw",
        con=engine,
        if_exists="replace",
        index=False
    )
    
    print("Done! Oregon counties loaded into PostGIS table: oregon_counties_raw")

if __name__ == "__main__":
    ingest_counties()