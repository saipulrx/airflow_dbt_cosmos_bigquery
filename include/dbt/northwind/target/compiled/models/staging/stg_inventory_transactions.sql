with source as (

    select * from `learning-gcp-369416`.`dbt_cosmos_airflow`.`inventory_transactions`
)
select 
    *,
    current_timestamp() as ingestion_timestamp
from source