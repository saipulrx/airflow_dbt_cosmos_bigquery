

  create or replace view `learning-gcp-369416`.`dbt_cosmos_airflow`.`stg_customers`
  OPTIONS()
  as with source as (

    select * from `learning-gcp-369416`.`dbt_cosmos_airflow`.`customers`

)
select 
    *,
    current_timestamp() as ingestion_timestamp
from source;

