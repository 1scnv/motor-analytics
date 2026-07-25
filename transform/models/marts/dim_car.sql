with sessions as (
    select distinct
        car
    from {{ ref('stg_sessions') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['car']) }} as car_id,
    car
from sessions
