-- transform.sql
-- Purpose: Transform raw ingested data into clean schema tables
-- Run after all raw ingestion scripts have been executed

-- ============================================================
-- COUNTIES
-- ============================================================

TRUNCATE TABLE oregon_counties;

INSERT INTO oregon_counties (
    county_name,
    cobcode,
    geom
)
SELECT
    "COUNTY_NAME"                                       AS county_name,
    "COBCODE"                                           AS cobcode,
    ST_Multi(geometry)::geometry(MULTIPOLYGON, 4326)    AS geom
FROM
    oregon_counties_raw
WHERE
    "COBCODE" LIKE 'OR%';

-- ============================================================
-- TRAILS
-- ============================================================

TRUNCATE TABLE oregon_trails;

INSERT INTO oregon_trails (
    trail_name,
    trail_no,
    trail_cn,
    trail_class,
    segment_length,
    gis_miles,
    trail_surface,
    surface_firmness,
    typical_trail_grade,
    typical_tread_width,
    mvum_symbol,
    terra_motorized,
    snow_motorized,
    motorcycle_managed,
    motorcycle_accpt,
    atv_managed,
    atv_accpt,
    fourwd_managed,
    fourwd_accpt,
    snowmobile_managed,
    snowmobile_accpt,
    snowcoach_snowcat_managed,
    managing_org,
    admin_org,
    security_id,
    allowed_terra_use,
    national_trail_designation,
    special_mgmt_area,
    geom
)
SELECT
    trail_name,
    trail_no,
    trail_cn,
    trail_class,
    segment_length,
    gis_miles,
    trail_surface,
    surface_firmness,
    typical_trail_grade,
    typical_tread_width,
    mvum_symbol,
    terra_motorized,
    snow_motorized,
    motorcycle_managed,
    motorcycle_accpt,
    atv_managed,
    atv_accpt,
    fourwd_managed,
    fourwd_accpt,
    snowmobile_managed,
    snowmobile_accpt,
    snowcoach_snowcat_managed,
    managing_org,
    admin_org,
    security_id,
    allowed_terra_use,
    national_trail_designation,
    special_mgmt_area,
    ST_Multi(geometry)::geometry(MULTILINESTRING, 4326) AS geom
FROM
    oregon_trails_raw
WHERE
    geometry IS NOT NULL;

-- ============================================================
-- LAND OWNERSHIP
-- ============================================================

TRUNCATE TABLE oregon_land_ownership;

INSERT INTO oregon_land_ownership (
    lm_class,
    fee_title_holder,
    fee_title_source,
    land_manager,
    lm1_jurisdiction,
    lm2_jurisdiction,
    lm_source,
    shape_area,
    shape_length,
    geom
)
SELECT
    "LMClass"                                           AS lm_class,
    "FeeTitleHolder"                                    AS fee_title_holder,
    "FeeTitleSource"                                    AS fee_title_source,
    "LandManager"                                       AS land_manager,
    "LM1Jurisdiction"                                   AS lm1_jurisdiction,
    "LM2Jurisdiction"                                   AS lm2_jurisdiction,
    "LMSource"                                          AS lm_source,
    "SHAPE__Area"                                       AS shape_area,
    "SHAPE__Length"                                     AS shape_length,
    ST_Multi(geometry)::geometry(MULTIPOLYGON, 4326)    AS geom
FROM
    oregon_land_ownership_raw
WHERE
    geometry IS NOT NULL;