from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

@dag(
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False,
    tags=['dbt','load_northwind_data'],
)

def elt_dbt():

    dbt_seed = BashOperator(
        task_id = 'dbt_seed',
        bash_command = 'cd /opt/airflow/include/dbt/northwind/ && dbt seed --select customers'
    )

    dbt_run_staging = BashOperator(
        task_id = 'dbt_run_staging',
        bash_command = 'cd /opt/airflow/include/dbt/northwind/ && dbt run --select stg_customers'
    )

    dbt_run_warehouse = BashOperator(
        task_id = 'dbt_run_warehouse',
        bash_command = 'cd /opt/airflow/include/dbt/northwind/ && dbt run --select dim_customers'
    )

    dbt_seed >> dbt_run_staging >> dbt_run_warehouse

elt_dbt()