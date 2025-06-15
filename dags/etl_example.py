from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
import logging

# Path lokasi file
dag_path = os.path.dirname(__file__)
input_file = os.path.join(dag_path, 'apple.csv')
output_extract = '/tmp/extracted_data.csv'
output_transform = '/tmp/transformed_data.csv'
output_load = os.path.join(dag_path, 'OLAP_data1.csv')

def extract():
    logging.info(f"[EXTRACT] Mencari file: {input_file}")
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"[EXTRACT] File tidak ditemukan: {input_file}")
    
    try:
        df = pd.read_csv(input_file, on_bad_lines='skip')
        logging.info(f"[EXTRACT] CSV berhasil dibaca. Jumlah baris: {len(df)}")
    except Exception as e:
        raise RuntimeError(f"[EXTRACT] Gagal membaca CSV: {e}")
    
    df.to_csv(output_extract, index=False)
    logging.info(f"[EXTRACT] Data disimpan di: {output_extract}")

def transform():
    logging.info("[TRANSFORM] Membaca data hasil extract...")
    
    if not os.path.exists(output_extract):
        raise FileNotFoundError(f"[TRANSFORM] File tidak ditemukan: {output_extract}")
    
    df = pd.read_csv(output_extract)
    
    required_columns = [
        'State', 'Region',
        'iPhone Sales (in million units)',
        'iPad Sales (in million units)',
        'Mac Sales (in million units)',
        'Wearables (in million units)',
        'Services Revenue (in billion $)'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"[TRANSFORM] Kolom berikut hilang dari data: {missing}")
    
    result = df.groupby(['State', 'Region']).agg({
        'iPhone Sales (in million units)': 'sum',
        'iPad Sales (in million units)': 'sum',
        'Mac Sales (in million units)': 'sum',
        'Wearables (in million units)': 'sum',
        'Services Revenue (in billion $)': 'sum'
    }).reset_index()
    
    result.to_csv(output_transform, index=False)
    logging.info(f"[TRANSFORM] Data hasil transform disimpan di: {output_transform}")

def load():
    logging.info("[LOAD] Membaca data hasil transform...")
    
    if not os.path.exists(output_transform):
        raise FileNotFoundError(f"[LOAD] File tidak ditemukan: {output_transform}")
    
    df = pd.read_csv(output_transform)
    df.to_csv(output_load, index=False)
    
    logging.info(f"[LOAD] Data akhir disimpan di: {output_load}")

# DAG Definition
with DAG(
    dag_id='etl_apple_sales',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['etl', 'apple']
) as dag:
    
    t1 = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    t2 = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    t3 = PythonOperator(
        task_id='load',
        python_callable=load
    )

    t1 >> t2 >> t3
