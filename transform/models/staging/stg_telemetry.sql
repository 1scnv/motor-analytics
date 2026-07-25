with source as (
    select * from {{ source('bronze', 'telemetry_raw') }}
),

renamed as (
    select
        -- session identifiers
        date as session_date,

        -- timing
        SessionTime             as session_time,
        Lap                     as lap,
        LapDistPct              as lap_dist_pct,
        LapCurrentLapTime       as lap_current_time,
        LapDeltaToBestLap       as lap_delta_to_best,

        -- inputs
        Throttle                as throttle,
        Brake                   as brake,
        Clutch                  as clutch,
        Gear                    as gear,
        SteeringWheelAngle      as steering_angle,

        -- motion
        Speed                   as speed_ms,
        round(Speed * 3.6, 4)   as speed_kmh,
        RPM                     as rpm,
        LongAccel               as accel_longitudinal,
        LatAccel                as accel_lateral,

        -- gps
        Lat                     as gps_lat,
        Lon                     as gps_lon

    from source
)

select * from renamed
