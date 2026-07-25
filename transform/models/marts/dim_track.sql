with sessions as (
    select distinct
        track
    from {{ ref('stg_sessions') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['track']) }} as track_id,
    track
from sessions
