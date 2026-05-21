Select 
    state_name,
    state-fips_code,
    ST_AREA(state_geom) / 10000000 AS area_sq_km

FROM
    `bigquery-public-data.geo.us_states`

Where state_name = 'Oregon'

-- Query: Oregon Counties by area
-- Source: bigquery-public-data.geo_us_boundaries.counties
-- Purpose: Explore Oregon county boundaries for land ownership analysis

SELECT
  county_name,
  county_fips_code,
  ST_AREA(county_geom) / 1000000 AS area_sq_km

FROM
  `bigquery-public-data.geo_us_boundaries.counties`

WHERE
  state_fips_code = '41'

ORDER BY 
  area_sq_km DESC