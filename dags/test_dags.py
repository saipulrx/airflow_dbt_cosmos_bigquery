import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.operators import DbtSeedOperator
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig
from include.dbt.northwind.cosmos_config import DBT_CONFIG, DBT_PROJECT_CONFIG
from airflow.models.baseoperator import chain

@dag(
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False,
    tags=['dbt','elt_northwind_data'],
)
def elt_northwind_data():

    # 1. Definisikan Task menggunakan dekorator secara eksplisit
    @task
    def start_task():
        # Mendapatkan waktu sekarang
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- ELT process STARTED at: {now} ---")
        return now

    @task
    def end_task():
        # Mendapatkan waktu sekarang
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- ELT process COMPLETED at: {now} ---")
        return now

    # Task khusus untuk dbt seed
    dbt_seed = DbtSeedOperator(
        task_id="dbt_seed",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        project_dir=DBT_PROJECT_CONFIG.dbt_project_path,
        # Jika dbt_project.yml Anda membutuhkan deps
        install_deps=True,
    )
    # 2. Langsung panggil DbtTaskGroup tanpa membungkusnya lagi dengan @task_group
    # Ini akan otomatis menjadi Task Group di dalam DAG
    dbt_model = DbtTaskGroup(
        group_id="dbt_model",
        profile_config=DBT_CONFIG,
        project_config=DBT_PROJECT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models']
        )
    )

    # 3. Hubungkan task. PASTIKAN fungsi @task dipanggil dengan kurung ()
    # Gunakan operator >> atau chain()
    chain(start_task(), dbt_seed, dbt_model, end_task())

elt_northwind_data()