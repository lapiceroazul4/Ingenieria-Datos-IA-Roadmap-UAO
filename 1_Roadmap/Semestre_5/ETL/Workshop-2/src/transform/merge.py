import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")
log = logging.getLogger(__name__)

## ---- Functions ---- ##

def fill_null_values(df, columns, value):
    """
    Fills null values in specified columns with a given value.
    
    """
    for column in columns:
        df[column] = df[column].fillna(value)

def drop_columns(df, columns):
    """
    Drops specified columns from the DataFrame.
    
    """
    df.drop(columns=columns, inplace=True, errors="ignore")
    
## ---- Merge datasets ---- ##

def merging_datasets(spotify_df: pd.DataFrame, grammys_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge the two datasets based on "track_name" and "nominee".
    
    """

    logging.info("Starting dataset merge.")
    
    logging.info(f"Initial Spotify dataset has {spotify_df.shape[0]} rows and {spotify_df.shape[1]} columns.")
    logging.info(f"Initial Grammys dataset has {grammys_df.shape[0]} rows and {grammys_df.shape[1]} columns.")
    
    try:
        # Clean "track_name" and "nominee" columns for better matching
        spotify_df["track_name_clean"] = spotify_df["track_name"].str.lower().str.strip()
        grammys_df["nominee_clean"] = grammys_df["nominee"].str.lower().str.strip()

        # Merge the datasets on the cleaned "track_name" and "nominee" columns
        df_merged = spotify_df.merge(
            grammys_df,
            how="left",
            left_on="track_name_clean",
            right_on="nominee_clean",
            suffixes=("", "_grammys")
        )

        # Fill null values in specified columns
        fill_columns = ["title", "category"]
        fill_null_values(df_merged, fill_columns, "Not applicable")

        fill_column = ["is_nominated"]
        fill_null_values(df_merged, fill_column, False)

        # Drop unnecessary columns
        columns_drop = [
            "year", "artist",
            "nominee", "nominee_clean", "track_name_clean"
        ]
        
        drop_columns(df_merged, columns_drop)
        
        df_merged = (df_merged
                     .reset_index()
                     .rename(columns={'index': 'id'}))
        
        df_merged['id'] = df_merged['id'].astype(int)

        logging.info(f"Merge process completed. The final dataframe has {df_merged.shape[0]} rows and {df_merged.shape[1]} columns.")
        
        return df_merged
    
    except Exception as e:
        logging.error(f"An error occurred during the merge process. {e}")