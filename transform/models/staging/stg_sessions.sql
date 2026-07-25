with source as (
    select * from {{ source('bronze', 'session_raw') }}
),

renamed as (
    select
        ibt_filename,
        track,
        car,
        session_type,
        total_laps,
        best_lap_time,
        date as session_date
    from source
)

select * from renamed
