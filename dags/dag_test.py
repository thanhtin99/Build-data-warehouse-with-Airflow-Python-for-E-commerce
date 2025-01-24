# complex_dag.py

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.subdag_operator import SubDagOperator
from datetime import datetime, timedelta

# Hàm Python để thực hiện các tác vụ
def extract():
    print("Extracting data...")
    # Giả lập việc trích xuất dữ liệu
    return "data_extracted"

def transform(data):
    print(f"Transforming data: {data}")
    # Giả lập việc biến đổi dữ liệu
    return "data_transformed"

def load(data):
    print(f"Loading data: {data}")
    # Giả lập việc tải dữ liệu
    return "data_loaded"

def choose_branch(**kwargs):
    # Quyết định nhánh nào sẽ được thực hiện
    if kwargs['ti'].xcom_pull(task_ids='extract_data') == "data_extracted":
        return 'transform_data'
    else:
        return 'skip_transform'

# Định nghĩa DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'complex_etl_dag',
    default_args=default_args,
    description='A complex ETL DAG example',
    schedule_interval='@hourly',
    catchup=False,
)

# Các tác vụ trong DAG
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
    dag=dag,
)

branch_task = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    python_callable=choose_branch,
    dag=dag,
)

transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    op_kwargs={'data': "{{ task_instance.xcom_pull(task_ids='extract_data') }}"},
    dag=dag,
)

skip_transform = DummyOperator(
    task_id='skip_transform',
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load,
    op_kwargs={'data': "{{ task_instance.xcom_pull(task_ids='transform_data') }}"},
    dag=dag,
)

end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# Thiết lập thứ tự thực hiện các tác vụ
start_task >> extract_data >> branch_task
branch_task >> transform_data >> load_data >> end_task
branch_task >> skip_transform >> end_task