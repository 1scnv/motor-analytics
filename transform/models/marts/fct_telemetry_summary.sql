with telemetry as (
    select * from {{ ref('stg_telemetry') }}
),

summary as (
    select
        session_date,
        lap,
        lap_dist_pct,

        -- speed
        avg(speed_kmh)              as avg_speed_kmh,
        max(speed_kmh)              as max_speed_kmh,

        -- inputs
        avg(throttle)               as avg_throttle,
        avg(brake)                  as avg_brake,
        avg(clutch)                 as avg_clutch,

        -- forces
        avg(abs(accel_longitudinal)) as avg_long_accel,
        avg(abs(accel_lateral))      as avg_lat_accel,

        -- gps (centroid of the sector)
        avg(gps_lat)                as avg_lat,
        avg(gps_lon)                as avg_lon,

        count(*)                    as tick_count
    from telemetry
    where lap > 0 -- exclude out lap
    group by session_date, lap, lap_dist_pct
)

select
    {{ dbt_utils.generate_surrogate_key(['session_date', 'lap', 'lap_dist_pct']) }} as summary_id,
    *
from summary
