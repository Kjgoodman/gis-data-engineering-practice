# GIS Data Engineering Practice

A personal project to build and document an end-to-end data pipeline using real public land, trail, and other datasets for the state of Oregon.

## Purpose
To develop hands-on experience with a professional GIS and data engineering stack (outside of ESRI products) including PostGIS, BigQuery, Python, QGIS, and GitHub - mirroring the workflows used by outdoor technology companies working with large-scale spatial datasets.

## Stack
- **Database:** PostGIS (via Docker)
- **Cloud Warehouse:** Google Bigquery
- **Desktop GIS:** QGIS
- **Language:** Python (Geopandas, Shapely, SQLAlchemy)
- **Version Control:** GitHub
- **Tile Generation:** Tippecanoe

## Data Sources
- BLM (Federal Land Ownership)
- USGS NHDplus (hydrology)
- USFS National Forest System Trails
- USGS 3DEP (elevation)
- Oregon GEO (state pracels)

## Project Structure
- 'data/' - raw and processed spatial datasets (not tracked by Git)
- 'sql/ - schema, enrichment, and QA queries
- 'pipelines/' - Python ingestion and processing scripts
- 'bigquery/' - BigQuery load and query scripts
- 'qgis/' - QGIS project files
- 'tiles/' - vector tile generation scripts
- 'docs/' - notes and learning journal

##Status

...IN PROGRESS

## Stack Progress
- ✅ GitHub — repo, structure, version control
- ✅ BigQuery — dataset, geospatial queries, spatial joins
- ✅ Docker + PostGIS — container running PostgreSQL 17 + PostGIS 3.5
- ✅ Python — virtual environment, geospatial libraries, PostGIS connection
- 🔲 Data Ingestion
  - ✅ Oregon counties (36 counties from Oregon GeoHub)
  - ✅ USFS trails (10,196 trails from USFS REST API)
  - 🔲 Oregon tax lots
  - 🔲 USGS hydrology
- 🔲 Data transformation and spatial joins
- 🔲 QGIS — visualization
- 🔲 Tippecanoe — vector tiles