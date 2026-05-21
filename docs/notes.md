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