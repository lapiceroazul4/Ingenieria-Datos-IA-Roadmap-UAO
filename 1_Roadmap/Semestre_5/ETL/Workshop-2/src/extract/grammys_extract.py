from database.db_operations import creating_engine, disposing_engine

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

## ----- Grammys Extract ----- ##

def extracting_grammys_data():
    """
    Extracting data from the Spotify CSV file and return it as a DataFrame.   

    """
    engine = creating_engine()
    
    try:
        logging.info("Extracting data from the Grammy Awards table.")
        df = pd.read_sql_table("grammy_awards_raw", engine)
        logging.info("Data extracted from the Grammy Awards table.")
        
        return df
    except Exception as e:
        logging.error(f"Error extracting data from the Grammy Awards table: {e}.")
    finally:
        disposing_engine(engine)