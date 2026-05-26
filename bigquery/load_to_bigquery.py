# load_to_bigquery.py
# Purpose: Load transformed PostGIS data into BigQuery for cloud analytics
# Source: Local PostGIS gis_practice database
# Destination: BigQuery oregon_gis dataset
# Run: python3 bigquery/load_to_bigquery.py

import geopandas as gpd
from sqlalchemy import create_engine
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# PostGIS connection
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gis_practice"
DB_USER = "postgres"
DB_PASS = "Portland11!"

# BigQuery settings
PROJECT_ID = "gis-data-engineering-practice"
DATASET_ID = "Oregon_GIS"
CREDENTIALS_PATH = "bigquery/credentials.json"

def get_bq_client():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)

def load_table(engine, bq_client, table_name):
    print(f"Loading {table_name}...")

    # Read from PostGIS
    gdf = gpd.read_postgis(
        f"SELECT * FROM {table_name}",
        engine,
        geom_col="geom"
    )

    print(f"  Read {len(gdf)} records from PostGIS")

    # Convert geometry to WKT string for BigQuery
    gdf["geom_wkt"] = gdf["geom"].apply(
        lambda x: x.wkt if x is not None else None
    )
    df = pd.DataFrame(gdf.drop(columns=["geom"]))

    # Load to BigQuery
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = bq_client.load_table_from_dataframe(
        df, table_ref, job_config=job_config
    )
    job.result()

    print(f"  Loaded {len(df)} records to BigQuery: {table_ref}")

def main():
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    bq_client = get_bq_client()

    tables = [
        "oregon_counties",
        "oregon_trails",
        "oregon_land_ownership"
    ]

    for table in tables:
        load_table(engine, bq_client, table)

    print("\nAll tables loaded to BigQuery successfully!")

if __name__ == "__main__":
    main()