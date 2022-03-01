import datetime as dt
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import psycopg2
import pendulum



def load_youtube_data():
    
    hostname='localhost'
    database='youtube_db'
    username='postgres'
    pwd='admin'
    port_id=5432
    conn=psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
    cur = conn.cursor()
    file_name=str(datetime.now().date())+'yt_data.pkl'
    full_file_name=os.path.join(os.path.dirname(__file__), file_name)
    df=pd.read_pickle(full_file_name)
    df["Update_Date"]=datetime.now().date()
    df=df[['Channel', 'Video_Id', 'Upload_Date','Video_Title','Video_Description','View_Count', 'Like_Count', 'Comment_Count', 'Update_Date']]

    command= """INSERT INTO Youtube_Vid (Channel, Video_Id, Upload_Date, Video_Title, Video_Description, View_Count, Like_Count, Comment_Count,Update_Date)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s)"""


    for i, row in df.iterrows():
        param=(row["Channel"], row["Video_Id"], row["Upload_Date"],row["Video_Title"],row["Video_Description"],row["View_Count"],row["Like_Count"],
        row["Comment_Count"],row["Update_Date"])
        cur.execute(command, param)
        conn.commit()
    
    cur.close()
    conn.close()

        
    
default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'email': ['email'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
    }

dag=DAG(dag_id='youtube_etl', default_args=default_args, start_date=datetime(2022,2,27, tzinfo=pendulum.timezone('America/Los_Angeles')),schedule_interval="@daily")

task_1=BashOperator(
       task_id="get_yt_data",
       bash_command='python3 /airflow_home/dags/extract_transform_youtube_data.py', #This is where the dag folder is stored
       dag=dag)

task_2=PythonOperator(
       task_id="load_yt_data",
       python_callable=load_youtube_data,
       dag=dag)

task_1 >> task_2

