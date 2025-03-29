import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

## ----- Spotify Extract ----- ##

def extracting_spotify_data(path):
    """
    Extracting data from the Spotify CSV file and return it as a DataFrame.   

    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}. Make sure you entered the correct absolute path.")
    try:
        df = pd.read_csv(path)
        logging.info(f"Data extracted from {path}.")
        return df
    except Exception as e:
        logging.error(f"Error extracting data: {e}.")