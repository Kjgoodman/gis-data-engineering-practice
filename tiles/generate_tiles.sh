#!/bin/bash
# generate_tiles.sh
# Purpose: Export PostGIS data to GeoJSON and generate vector tiles
# Requirements: GDAL, Tippecanoe
# Run: bash tiles/generate_tiles.sh

echo "Exporting PostGIS tables to GeoJSON..."

ogr2ogr -f GeoJSON data/processed/oregon_counties.geojson \
  'PG:host=localhost port=5432 dbname=gis_practice user=postgres password=Portland11!' \
  oregon_counties

ogr2ogr -f GeoJSON data/processed/oregon_trails.geojson \
  'PG:host=localhost port=5432 dbname=gis_practice user=postgres password=Portland11!' \
  oregon_trails

ogr2ogr -f GeoJSON data/processed/oregon_land_ownership.geojson \
  'PG:host=localhost port=5432 dbname=gis_practice user=postgres password=Portland11!' \
  oregon_land_ownership

echo "Generating vector tiles with Tippecanoe..."

tippecanoe -o tiles/oregon_offroad.pmtiles \
  --name="Oregon Offroad" \
  -L counties:data/processed/oregon_counties.geojson \
  -L trails:data/processed/oregon_trails.geojson \
  -L land_ownership:data/processed/oregon_land_ownership.geojson \
  --minimum-zoom=5 \
  --maximum-zoom=14 \
  --drop-densest-as-needed \
  -f

echo "Done! Tiles saved to tiles/oregon_offroad.pmtiles"