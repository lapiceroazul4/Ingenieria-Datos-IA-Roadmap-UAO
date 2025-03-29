# Importing the necessary modules
# --------------------------------

from extract.spotify_extract import extracting_spotify_data
from extract.grammys_extract import extracting_grammys_data

from transform.spotify_transform import transforming_spotify_data
from transform.grammys_transform import transforming_grammys_data
from transform.merge import merging_datasets

from load_and_store.load import loading_merged_data
from load_and_store.store import storing_merged_data

import os
import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Creating tasks functions
# ------------------------

def extract_spotify():
    try:
        df = extracting_spotify_data("./data/spotify_dataset.csv") 
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")

def extract_grammys():
    try:
        df = extracting_grammys_data()
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        
def transform_spotify(df):
    try:
        json_df = json.loads(df)
        
        raw_df = pd.DataFrame(json_df)
        df = transforming_spotify_data(raw_df)
        
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        
def transform_grammys(df):
    try:
        json_df = json.loads(df)
        
        raw_df = pd.DataFrame(json_df)
        df = transforming_grammys_data(raw_df)
        
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        
def merge_data(spotify_df, grammys_df):
    try:
        spotify_json = json.loads(spotify_df)
        grammys_json = json.loads(grammys_df)
        
        spotify_df = pd.DataFrame(spotify_json)
        grammys_df = pd.DataFrame(grammys_json)
        
        df = merging_datasets(spotify_df, grammys_df)
        
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error merging data: {e}")
        
def load_data(df):
    try:
        json_df = json.loads(df)
        
        df = pd.DataFrame(json_df)
        loading_merged_data(df, "merged_data")
        
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        
def store_data(df):
    try:
        json_df = json.loads(df)
        
        df = pd.DataFrame(json_df)
        storing_merged_data("merged_data", df)
    except Exception as e:
        logging.error(f"Error storing data: {e}")