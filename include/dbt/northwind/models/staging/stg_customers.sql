with source as (

    select * from {{ ref('customers') }}

)
select 
    *,
    current_timestamp() as ingestion_timestamp
from source