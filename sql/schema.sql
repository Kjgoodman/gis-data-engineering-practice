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
  cobcode VARCHAR(10),
  geom GEOMETRY(MULTIPOLYGON, 4326)
);

-- Oregon trails table
-- Source: USFS National Forest System Trails
-- Focused on motorized use attributes for onX Offroad use case
CREATE TABLE IF NOT EXISTS oregon_trails (
  id SERIAL PRIMARY KEY,
  trail_name VARCHAR(200),
  trail_no VARCHAR(50),
  trail_cn VARCHAR(50),
  trail_class VARCHAR(50),
  segment_length DOUBLE PRECISION,
  gis_miles DOUBLE PRECISION,
  trail_surface VARCHAR(100),
  surface_firmness VARCHAR(50),
  typical_trail_grade VARCHAR(50),
  typical_tread_width VARCHAR(50),
  mvum_symbol DOUBLE PRECISION,
  terra_motorized VARCHAR(50),
  snow_motorized VARCHAR(50),
  motorcycle_managed VARCHAR(50),
  motorcycle_accpt VARCHAR(50),
  atv_managed VARCHAR(50),
  atv_accpt VARCHAR(50),
  fourwd_managed VARCHAR(50),
  fourwd_accpt VARCHAR(50),
  snowmobile_managed VARCHAR(50),
  snowmobile_accpt VARCHAR(50),
  snowcoach_snowcat_managed VARCHAR(50),
  managing_org VARCHAR(100),
  admin_org VARCHAR(100),
  security_id VARCHAR(50),
  allowed_terra_use VARCHAR(200),
  national_trail_designation INTEGER,
  special_mgmt_area VARCHAR(200),
  geom GEOMETRY(MULTILINESTRING, 4326)
);

-- Oregon land ownership table
-- Source: Oregon GeoHub - Ownership Land Management
-- Includes public land by managing agency and private land classifications
CREATE TABLE IF NOT EXISTS oregon_land_ownership (
  id SERIAL PRIMARY KEY,
  lm_class INTEGER,
  fee_title_holder VARCHAR(200),
  fee_title_source VARCHAR(200),
  land_manager VARCHAR(100),
  lm1_jurisdiction VARCHAR(200),
  lm2_jurisdiction VARCHAR(200),
  lm_source VARCHAR(200),
  shape_area DOUBLE PRECISION,
  shape_length DOUBLE PRECISION,
  geom GEOMETRY(MULTIPOLYGON, 4326)
);