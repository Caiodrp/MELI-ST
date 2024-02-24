from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from extract_api import fetch_product_data, main

# Define os argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 31),  # Data de início
    'email': ['caiodouglasrodrigues@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define a DAG
dag = DAG(
    'mercado_livre_extraction',
    default_args=default_args,
    schedule_interval='0 3 * * SUN'  #rodar todo domingo às 00:00 (03:00 UTC)
)

# Define uma tarefa na DAG para indicar o início do processo
start_operator = EmptyOperator(task_id='start_extraction', dag=dag)

# Define uma tarefa na DAG para extrair os dados
t1 = PythonOperator(
    task_id='extract_data',
    python_callable=main,
    dag=dag
)

# Define uma tarefa na DAG para indicar o fim do processo
end_operator = EmptyOperator(task_id='end_extraction', dag=dag)

# Define a ordem das tarefas
start_operator >> t1 >> end_operator