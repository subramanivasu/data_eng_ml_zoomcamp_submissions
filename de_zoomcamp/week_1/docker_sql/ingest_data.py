#!/usr/bin/env python
# coding: utf-8
import os 
import argparse

import pandas as pd

from time import time

#Creating a connection to postgres to generate the ddl that postgres can understand. 
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db=params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'
   
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name,iterator=True,chunksize=100000)
 
    df=next(df_iter)

    #We have to tell pandas that pickup/dropoff_datatime is of type datatime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    #n=0 will only return the header.We use this to insert all these data to our data base. Just the table
    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')

    #Insert data. Append - appends the values to the exi sting data for each chunk of data. %time - Tells time taken
    df.to_sql(name=table_name,con=engine,if_exists='append')


    while True:
        
        try:
            start_time = time()
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name,con=engine,if_exists='append')

            end_time = time()

            print("Inserted another chunk | Time Taken %.3f second' " %(end_time - start_time))
        
        except:
            print("Insertion Completed")
            break


if(__name__ == '__main__'):

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user',help='User name for Postgres')
    parser.add_argument('--password',help='Password for Postgres')
    parser.add_argument('--host',help='Host for Postgres')
    parser.add_argument('--port',help='Port for Postgres')
    parser.add_argument('--db',help='Database name for Postgres')
    parser.add_argument('--table_name',help='Table name where the results will be written to')
    parser.add_argument('--url',help='URL of the csv file')

    args = parser.parse_args()

    main(args)


