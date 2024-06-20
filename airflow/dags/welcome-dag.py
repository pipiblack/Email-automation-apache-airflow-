from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import requests


def print_welcome():
    print("Welcome to the Airflow DAG!")


def print_date():
    print('Today is {}'.format(datetime.today().date()))


def print_random_quote():
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()['content']
    print('Quote of the day:"{}"'.format(quote))


# create scheduler
dag = DAG(
    'welcome_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

# create tasks

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_quote_task = PythonOperator(
    task_id='print_quote',
    python_callable=print_random_quote,
    dag=dag

)

# set task dependencies

print_welcome_task >> print_date_task >> print_quote_task
