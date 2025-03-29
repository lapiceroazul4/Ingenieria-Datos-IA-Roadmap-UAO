from database.db_operations import creating_engine, load_clean_data, disposing_engine

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

# Loading the merged data to the database
def loading_merged_data(df: pd.DataFrame, table_name: str) -> None:
    """
    This function takes a merged DataFrame and a table name as input, 
    and loads the DataFrame into the specified table in the database. 
    It logs the process and handles any exceptions that occur during 
    the loading process.
    
    Parameters:
        df (pd.DataFrame): The merged DataFrame to be loaded into the database.
        table_name (str): The name of the table where the data will be loaded.
    
    Returns:
        None

    """
    
    logging.info("Loading clean data to the database.")
    
    engine = creating_engine()
    
    try:
        df = load_clean_data(engine, df, table_name)    
    except Exception as e:
        logging.error(f"Error loading clean data to the database: {e}.")
    finally:
        disposing_engine(engine)