import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

## ----- Functions ----- ##

def extract_artist(workers):
    """
    Extracts the artist name from the 'workers' column if it's within parentheses.
    
    """
    if pd.isna(workers):
        return None
    match = re.search(r'\((.*?)\)', workers)
    if match:
        return match.group(1)
    return None

def move_workers_to_artist(row):
    """
    Moves the value from 'workers' to 'artist' if 'artist' is NaN and 'workers' doesn't contain ';' or ','.
    
    """
    if pd.isna(row["artist"]) and pd.notna(row["workers"]):
        workers = row["workers"]
        if not re.search(r'[;,]', workers):
            return workers
    return row["artist"]

def extract_artists_before_semicolon(workers, roles):
    """
    Extracts the first segment of 'workers' before the semicolon if it doesn't contain roles of interest.
    
    """
    if pd.isna(workers):
        return None
    parts = workers.split(';')
    first_part = parts[0].strip()
    if ',' not in first_part and not any(role in first_part.lower() for role in roles):
        return first_part
    return None

def extract_roles_based_on_interest(workers, roles):
    """
    Extracts names associated with specific roles from 'workers' and assigns them to 'artist'.
    
    """
    if pd.isna(workers):
        return None
    roles_pattern = '|'.join(roles)
    pattern = r'([^;]+)\s*,\s*(?:' + roles_pattern + r')'
    matches = re.findall(pattern, workers, flags=re.IGNORECASE)
    return ", ".join(matches).strip() if matches else None

# Define the categories to filter out
categories = [
    "Best Classical Vocal Soloist Performance",
    "Best Classical Vocal Performance",
    "Best Small Ensemble Performance (With Or Without Conductor)",
    "Best Classical Performance - Instrumental Soloist Or Soloists (With Or Without Orchestra)",
    "Most Promising New Classical Recording Artist",
    "Best Classical Performance - Vocal Soloist (With Or Without Orchestra)",
    "Best New Classical Artist",
    "Best Classical Vocal Soloist",
    "Best Performance - Instrumental Soloist Or Soloists (With Or Without Orchestra)",
    "Best Classical Performance - Vocal Soloist"
]

# Define roles of interest
roles_of_interest = [
    "artist",
    "artists",
    "composer",
    "conductor",
    "conductor/soloist",
    "choir director",
    "chorus master",
    "graphic designer",
    "soloist",
    "soloists",
    "ensembles"
]

## ----- Grammys Transformations ----- ##

def transforming_grammys_data(df):
    """
    Cleans and transforms the Grammy Awards data and returns the DataFrame.
    
    """
    try:
        logging.info(f"Starting transformation. The DataFrame has {df.shape[0]} rows and {df.shape[1]} columns.")
        
        df = df.rename(columns={"winner": "is_nominated"})
        
        # Dropping unnecessary columns
        df = df.drop(columns=["published_at", "updated_at", "img"])
        
        # Dropping null values - Nominee case
        df = df.dropna(subset=["nominee"])
        
        # Dropping null values - Artist case
        both_null_values = df[df["artist"].isna() & df["workers"].isna()]
        
        both_filtered = both_null_values[both_null_values["category"].isin(categories)]
        
        both_null_values = both_null_values.drop(both_filtered.index)
        df = df.drop(both_filtered.index)
        
        df.loc[both_null_values.index, "artist"] = both_null_values["nominee"]
        
        df["artist"] = df.apply(
            lambda row: extract_artist(row["workers"]) if pd.isna(row["artist"]) else row["artist"],
            axis=1
        )
        
        df["artist"] = df.apply(move_workers_to_artist, axis=1)
        
        df["artist"] = df.apply(
            lambda row: extract_artists_before_semicolon(row["workers"], roles_of_interest)
            if pd.isna(row["artist"]) else row["artist"],
            axis=1
        )
        
        df["artist"] = df.apply(
            lambda row: extract_roles_based_on_interest(row["workers"], roles_of_interest)
            if pd.isna(row["artist"]) else row["artist"],
            axis=1
        )
        
        df = df.dropna(subset=["artist"])
        
        # Transforming values - Artist cases
        df["artist"] = df["artist"].replace({"(Various Artists)": "Various Artists"})
        
        # Dropping workers column as it's no longer needed
        df = df.drop(columns=["workers"])
        
        logging.info(f"Transformation complete. The DataFrame now has {df.shape[0]} rows and {df.shape[1]} columns.")
        
        return df
    
    except Exception as e:
        logging.error(f"An error has occurred: {e}")