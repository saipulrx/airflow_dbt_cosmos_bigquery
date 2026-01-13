
  
    

    create or replace table `learning-gcp-369416`.`dbt_cosmos_airflow`.`dim_customers`
      
    
    

    
    OPTIONS()
    as (
      with source as (
    select
        id as customer_id,
        company,
        last_name,
        first_name,
        email_address,
        job_title,
        business_phone,
        home_phone,
        mobile_phone,
        fax_number,
        address,
        city,
        state_province,
        zip_postal_code,
        country_region,
        web_page,
        notes,
        attachments,
        current_timestamp() as insertion_timestamp,
    from `learning-gcp-369416`.`dbt_cosmos_airflow`.`stg_customers`
)
select * 
from source
    );
  