import os
import pandas as pd


def clean_data():
    data = pd.read_csv('/tmp/xrate.csv', header=None)

    # cleansing the data
    default_values = {
        int: 0,
        float: 0.0,
        str: " "
    }

    clean_data = data.fillna(value=default_values)

    # fetch the current date and time

    now = pd.Timestamp.now()
    year = now.year
    month = now.month
    day = now.day

    # create the directory to store the data if it does not exist
    data_dir = f'opt/airflow/data/xrate_cleansed/{year}/{month}/{day}'
    os.makedirs(data_dir, exist_ok=True)

    # save the data to the directory

    clean_data.to_csv(f'{data_dir}/xrate.csv', index=False)
