{{ config(
    partition_by={
      "field": "transaction_created_date",
      "data_type": "datetime",
      "granularity": "day" 
    },
    materialized="incremental",
    unique_key="inventory_id",
    incremental_strategy="merge"
)}}

with source as (
    select
        id as inventory_id,
        transaction_type,
        -- HAPUS casting date(), biarkan asli atau cast ke datetime jika perlu
        transaction_created_date, 
        transaction_modified_date,
        product_id,
        quantity,
        purchase_order_id,
        customer_order_id,
        comments,
        current_timestamp() as insertion_timestamp,
    from {{ ref('stg_inventory_transactions') }}

    {% if is_incremental() %}
    where transaction_modified_date > (select max(transaction_modified_date) from {{ this }})
    {% endif %}
),

unique_source as (
    select *,
            row_number() over(
                partition by inventory_id 
                order by transaction_modified_date desc
            ) as row_number
    from source
)

select * except (row_number),
from unique_source
where row_number = 1