with telemetry as (
    select * from {{ ref('stg_telemetry') }}
),

sessions as (
    select * from {{ ref('stg_sessions') }}
),

laps as (
    select
        session_date,
        lap,
        min(session_time)           as lap_start_time,
        max(lap_current_time)       as lap_time,
        avg(throttle)               as avg_throttle,
        avg(brake)                  as avg_brake,
        max(speed_kmh)              as max_speed_kmh,
        avg(speed_kmh)              as avg_speed_kmh,
        avg(rpm)                    as avg_rpm,
        avg(abs(steering_angle))    as avg_steering_abs,
        avg(abs(accel_lateral))     as avg_lat_accel,
        avg(abs(accel_longitudinal)) as avg_long_accel,
        count(*)                    as tick_count
    from telemetry
    where lap > 0 -- exclude out lap
    group by session_date, lap
),

joined as (
    select
        {{ dbt_utils.generate_surrogate_key(['laps.session_date', 'laps.lap']) }} as lap_id,
        laps.session_date,
        laps.lap,
        laps.lap_start_time,
        laps.lap_time,
        laps.avg_throttle,
        laps.avg_brake,
        laps.max_speed_kmh,
        laps.avg_speed_kmh,
        laps.avg_rpm,
        laps.avg_steering_abs,
        laps.avg_lat_accel,
        laps.avg_long_accel,
        laps.tick_count,
        dim_track.track_id,
        dim_car.car_id,
        sessions.session_type,
        sessions.best_lap_time
    from laps
    left join sessions
        on laps.session_date = sessions.session_date
    left join {{ ref('dim_track') }} as dim_track
        on sessions.track = dim_track.track
    left join {{ ref('dim_car') }} as dim_car
        on sessions.car = dim_car.car
)

select * from joined
