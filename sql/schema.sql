-- Schema: GIS Data Engineering Practice
-- Database: gis_practice (PostGIS via Docker)
-- Purpose: Define spatial tables for Oregon land, trail, and hydrology analysis

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Oregon counties table
-- Source: Will be populated from USGS/Census TIGER data
-- SRID 4326 = WGS84 geographic coordinate system (standard lat/lng)
CREATE TABLE IF NOT EXISTS oregon_counties (
  id SERIAL PRIMARY KEY,
  county_name VARCHAR(100),
  fips_code VARCHAR(10),
  geom GEOMETRY(MULTIPOLYGON, 4326)
);

-- Oregon trails table
-- Source: Will be populated from USFS National Forest System Trails
CREATE TABLE IF NOT EXISTS oregon_trails (
  id SERIAL PRIMARY KEY,
  trail_name VARCHAR(200),
  trail_no VARCHAR(50),
  surface_type VARCHAR(100),
  managing_org VARCHAR(100),
  geom GEOMETRY(MULTILINESTRING, 4326)
);

-- Oregon land ownership table
-- Source: Will be populated from BLM Surface Management Agency data
CREATE TABLE IF NOT EXISTS oregon_land_ownership (
  id SERIAL PRIMARY KEY,
  owner_name VARCHAR(200),
  ownership_type VARCHAR(100),
  state_fips VARCHAR(2),
  geom GEOMETRY(MULTIPOLYGON, 4326)
);

-- Oregon hydrology table
-- Source: Will be populated from USGS NHDPlus
CREATE TABLE IF NOT EXISTS oregon_hydrology (
  id SERIAL PRIMARY KEY,
  stream_name VARCHAR(200),
  stream_order INTEGER,
  stream_type VARCHAR(100),
  geom GEOMETRY(MULTILINESTRING, 4326)
);