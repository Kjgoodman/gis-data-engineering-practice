Select 
    state_name,
    state-fips_code,
    ST_AREA(state_geom) / 10000000 AS area_sq_km

FROM
    `bigquery-public-data.geo.us_states`

Where state_name = 'Oregon'