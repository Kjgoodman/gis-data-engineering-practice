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

-- Query 3: Spatial join - zip codes per Oregon county
-- Source: geo_us_boundaries.counties + geo_us_boundaries.zip_codes
-- Purpose: Practice spatial joins using ST_INTERSECTS across two public tables

SELECT
  c.county_name,
  COUNT(z.zip_code) AS zip_code_count
FROM
  `bigquery-public-data.geo_us_boundaries.counties` c
JOIN
  `bigquery-public-data.geo_us_boundaries.zip_codes` z
ON
  ST_INTERSECTS(c.county_geom, z.zip_code_geom)
WHERE
  c.state_fips_code = '41'
GROUP BY
  c.county_name
ORDER BY
  zip_code_count DESC
