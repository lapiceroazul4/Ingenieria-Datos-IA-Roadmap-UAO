from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, BigInteger, Boolean, Integer, Float, String, Text, DateTime, MetaData, Table, Column
from sqlalchemy_utils import database_exists, create_database

import os
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

# Reading the environment variables
load_dotenv("../env/.env")

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")

host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")

database = os.getenv("PG_DATABASE")

# Creating the connection engine from the URL made up of the environment variables
def creating_engine():
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    
    if not database_exists(url):
        create_database(url)
        logging.info("Database created")
    
    logging.info("Engine created. You can now connect to the database.")
    
    return engine

def disposing_engine(engine):
    engine.dispose()
    logging.info("Engine disposed.")

# Defining a function to infer the SQLAlchemy types from Pandas Dtypes
def infering_types(dtype, column_name, df):
    if "int" in dtype.name:
        return Integer
    elif "float" in dtype.name:
        return Float
    elif "object" in dtype.name:
        max_len = df[column_name].astype(str).str.len().max()
        if max_len > 255:
            logging.info(f"Adjusting column {column_name} to Text due to length {max_len}.")
            return Text
        else:
            return String(255)
    elif "datetime" in dtype.name:
        return DateTime
    elif "bool" in dtype.name:
        return Boolean
    else:
        return Text


# Creating table and loading the raw data
def load_raw_data(engine, df, table_name):
    
    logging.info(f"Creating table {table_name} from Pandas DataFrame.")
    
    try:   
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    
        logging.info(f"Table {table_name} created successfully.")
    
    except Exception as e:
        logging.error(f"Error creating table {table_name}: {e}")

# Creating table and loading the clean data
def load_clean_data(engine, df, table_name):
    
    logging.info(f"Creating table {table_name} from Pandas DataFrame.")
    
    try:
        if not inspect(engine).has_table(table_name):
            metadata = MetaData()
            columns = [Column(name,
                            infering_types(dtype, name, df),
                            primary_key=(name == "id")) \
                                for name, dtype in df.dtypes.items()]
            
            table = Table(table_name, metadata, *columns)
            table.create(engine)
            
            logging.info(f"Table {table_name} created successfully.")

            df.to_sql(table_name, con=engine, if_exists="append", index=False)

            logging.info(f"Data loaded to table {table_name}.")
        else:
            logging.error(f"Table {table_name} already exists.")
    except Exception as e:
        logging.error(f"Error creating table {table_name}: {e}")