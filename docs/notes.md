# Project Notes

## Session 1 - GitHub Setup
- Initialized Git and configured with username and email
- Created GitHub repo and connected local folder
- Built project folder structure
- Created .gitignore to protect credentials and large data files
- Wrote professional README documenting the stack

## Session 2 - BigQuery
- Created Google Cloud project and BigQuery dataset (oregon_gis, US multi-region)
- Learned BigQuery geospatial functions: ST_AREA, ST_INTERSECTS
- Queried Oregon state boundary and calculated area (254,297 sq km)
- Queried Oregon counties by area using state FIPS code '41'
- Ran first spatial join: zip codes per Oregon county
- Key learning: BigQuery cannot GROUP BY geometry columns

## Session 3 - Docker + PostGIS
- Installed Docker Desktop
- Pulled postgis/postgis image (required --platform linux/amd64 for M5)
- Created container: gis_postgis running PostgreSQL 17 + PostGIS 3.5
- Created gis_practice database with four spatial tables:
  - oregon_counties (MULTIPOLYGON)
  - oregon_trails (MULTILINESTRING)
  - oregon_land_ownership (MULTIPOLYGON)
  - oregon_hydrology (MULTILINESTRING)
- Key learning: GitHub stores code, Docker runs the live database - they are separate

## Session 4 - Python Setup
- Installed Homebrew (Mac package manager)
- Installed pyenv to manage Python versions
- Installed Python 3.11.9 via pyenv (fixed lzma warning by installing xz first)
- Set Python 3.11.9 as local version for project via .python-version file
- Created Python virtual environment (venv) inside project folder
- Installed geospatial libraries:
  - geopandas — spatial dataframes
  - sqlalchemy — database connection manager
  - psycopg2-binary — PostgreSQL driver
  - shapely — geometry operations
  - pandas — data manipulation
  - requests — downloading data from URLs
- Generated requirements.txt to document all dependencies
- Wrote test_connection.py to verify Python → PostGIS connection
- Key learning: psycopg2-binary vs psycopg2 — use binary version on Mac to avoid compilation errors
- Key learning: always activate venv with `source venv/bin/activate` before working on the project

## Session 5 - First Data Ingestion
- Installed geoalchemy2 (required by GeoPandas to_postgis())
- Updated requirements.txt
- Found Oregon county boundaries on Oregon GeoHub via ArcGIS REST API
- Chose REST API over manual download to mirror real pipeline practices
- Wrote ingest_counties.py to fetch GeoJSON directly from API URL
- Discovered dataset included Washington state counties (39) mixed with Oregon (36)
- Added COBCODE filter to isolate Oregon counties only
- Loaded 36 Oregon counties into PostGIS table: oregon_counties_raw
- Key learning: raw tables (_raw) preserve source data exactly as received
- Key learning: two stage pipeline — raw ingestion first, transform second
- Key learning: manual script run = one snapshot in time, production pipelines
  use schedulers like Airflow to refresh data automatically
- Next: ingest Oregon trails, BLM land ownership, and USGS hydrology raw data

## Session 6 - Data Ingestion Continued
- Wrote ingest_trails.py to fetch USFS National Forest System Trails
- Discovered USFS API has 2000 record limit per request
- Implemented pagination using resultOffset parameter
- Encountered HTTP 500 errors from USFS server at large batch sizes
- Fixed by reducing BATCH_SIZE from 2000 to 500
- Added retry logic with 3 attempts and 5 second delay between retries
- Added 1 second delay between requests to be respectful of API
- Successfully loaded 10,196 trails into PostGIS table: oregon_trails_raw
- Key learning: always check API max record count before ingesting
- Key learning: smaller batch sizes are more reliable than large requests
- Key learning: retry logic is essential for unreliable government APIs
- Next: ingest Oregon tax lots from Oregon Explorer

## Session 7 - Data Ingestion Complete
- Wrote ingest_land_ownership.py to fetch Oregon public/private land boundaries
- Used batch size of 500 for reliability, loaded 3,291 features
- Attempted USGS NHDPlus HR hydrology dataset but encountered 504 Gateway Timeout
- Decided to drop hydrology dataset — not critical for onX Offroad focus
- Explored trails dataset columns — discovered MVUM data already included:
  - mvum_symbol, terra_motorized, motorcycle_managed, atv_managed etc.
  - 1,938 motorized trails in dataset
- Explored land ownership columns — confirmed state parks already included:
  - OPRD (Oregon Parks and Recreation) = 294 features
  - Also includes BLM, USFS, ODFW, NPS, and private land classifications
- Key learning: always explore your data before sourcing additional datasets
- Key learning: government datasets often include more attributes than expected
- Raw ingestion phase complete — 3 datasets loaded:
  - oregon_counties_raw (36 counties)
  - oregon_trails_raw (10,196 trails)
  - oregon_land_ownership_raw (3,291 features)
- Next: transformation phase — clean, rename, and load into schema tables

## Session 8 - Schema Updates and Data Transformation
- Reviewed and updated schema for all three datasets
- Removed oregon_hydrology table entirely — not needed for Offroad focus
- Updated oregon_counties schema: renamed fips_code to cobcode (more accurate)
- Updated oregon_trails schema: added all motorized use fields for onX Offroad:
  - mvum_symbol, terra_motorized, snow_motorized
  - motorcycle, atv, fourwd, snowmobile, snowcoach managed/accpt fields
  - Fixed VARCHAR(10) to VARCHAR(50) after discovering atv_managed has 23 char values
- Updated oregon_land_ownership schema: kept all fields, renamed to snake_case
- Wrote transform.sql to move data from raw tables to clean schema tables
- Successfully transformed all three datasets:
  - oregon_counties: 36 counties
  - oregon_trails: 8,522 trails (1,674 dropped due to null geometries in source)
  - oregon_land_ownership: 3,266 features
- Key learning: always check max field lengths before setting VARCHAR size
- Key learning: null geometry filtering is essential QA in any spatial pipeline
- Key learning: document data quality issues like null geometries — 
  this is what OnX QA workflows catch
- Next: QGIS visualization

## Session 9 - QGIS Visualization
- Installed QGIS (Long Term Release)
- Connected QGIS directly to PostGIS Docker container via PostgreSQL connection
- Loaded three layers from PostGIS:
  - oregon_counties — state boundary and county lines
  - oregon_land_ownership — public/private land by managing agency
  - oregon_trails — trail network with motorized use attributes
- Styled land ownership by land_manager field (categorized symbology)
- Styled trails by terra_motorized field (Y/N/N/A)
  - Orange/red = motorized allowed
  - Gray = no motorized use
- Saved QGIS project as oregon_offroad.qgz in qgis/ folder
- Key learning: QGIS .qgz file stores connection settings not data
- Key learning: data lives in PostGIS, QGIS just visualizes it
- Next: load transformed data to BigQuery, then vector tiles with Tippecanoe