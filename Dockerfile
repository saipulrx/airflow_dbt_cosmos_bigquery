FROM apache/airflow:2.11.0

RUN pip install --no-cache-dir astronomer-cosmos[dbt-bigquery]==1.12.0

ENV PIP_USER=false

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.11.0 && deactivate

ENV PIP_USER=true