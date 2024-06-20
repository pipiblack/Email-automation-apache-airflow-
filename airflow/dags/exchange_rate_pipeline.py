# import all necessary libraries

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import requests

from airflow.clean_data import clean_data

# define args for the dag

dag = DAG(
    'exchange_rate_et1',
    start_date=datetime(2023, 10, 1),
    end_date=datetime(2023, 12, 1),
    schedule_interval=('0 22 * * *'),
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=5)}

)

# define and create instances of the tasks

download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata',
    cwd='/tmp',
    dag=dag
)

clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag

)

send_email_task = EmailOperator(
    task_id='send_email',
    to='pipiblack161@gmail.com',
    subject='Exchange rate data download - success',
    html_content='Exchange rate data has been successfully downloaded',
)

# set the task dependancies

download_task >> clean_data_task >> send_email_task
