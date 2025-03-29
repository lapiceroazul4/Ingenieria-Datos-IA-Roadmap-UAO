import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

## ----- Functions ----- ##

def categorize_duration(duration_ms):
    """
    Categorize the duration of a song based on its duration in milliseconds.
    
    """
    if duration_ms < 150000:
        return "Short"
    elif 150000 <= duration_ms <= 300000:
        return "Average"
    else:
        return "Long"
    
def categorize_popularity(popularity):
    """
    Categorize the popularity of a song based on its popularity score.
    
    """
    if popularity <= 30:
        return "Low Popularity"
    elif 31 <= popularity <= 70:
        return "Average Popularity"
    else:
        return "High Popularity"
    
def determine_mood(valence):
    """
    Determine the mood of a song based on its valence score.
    
    """
    if valence <= 0.3:
        return "Sad"
    elif 0.31 <= valence <= 0.6:
        return "Neutral"
    else:
        return "Happy"
    
## ----- Spotify Transformations ----- ##
        
def transforming_spotify_data(df):
    """
    Cleaning and transforming the Spotify DataFrame and return said DataFrame.
    
    """
    try:
        logging.info(f"Cleaning and transforming the DataFrame. You currently have {df.shape[0]} rows and {df.shape[1]} columns.")
        
        # Remove Unnamed: 0 column
        df = df.drop(columns=["Unnamed: 0"])
       
        # Remove null values  
        df = (df
                .dropna()
                .reset_index(drop=True))
        
        # Remove duplicates - First step: drop strict duplicates
        df = df.drop_duplicates()
        
        # Remove duplicates - Second step: track_id case
        df = (df
                .drop_duplicates(subset=["track_id"])
                .reset_index(drop=True))
        
        # Remove duplicates - Third step: Mapping track_genre to its respective category
        genre_mapping = {
            'Rock/Metal': [
                'alt-rock', 'alternative', 'black-metal', 'death-metal', 'emo', 'grindcore',
                'hard-rock', 'hardcore', 'heavy-metal', 'metal', 'metalcore', 'psych-rock',
                'punk-rock', 'punk', 'rock-n-roll', 'rock', 'grunge', 'j-rock', 'goth',
                'industrial', 'rockabilly', 'indie'
            ],
            
            'Pop': [
                'pop', 'indie-pop', 'power-pop', 'k-pop', 'j-pop', 'mandopop', 'cantopop',
                'pop-film', 'j-idol', 'synth-pop'
            ],
            
            'Electronic/Dance': [
                'edm', 'electro', 'electronic', 'house', 'deep-house', 'progressive-house',
                'techno', 'trance', 'dubstep', 'drum-and-bass', 'dub', 'garage', 'idm',
                'club', 'dance', 'minimal-techno', 'detroit-techno', 'chicago-house',
                'breakbeat', 'hardstyle', 'j-dance', 'trip-hop'
            ],
            
            'Urban': [
                'hip-hop', 'r-n-b', 'dancehall', 'reggaeton', 'reggae'
            ],
            
            'Latino': [
                'brazil', 'salsa', 'samba', 'spanish', 'pagode', 'sertanejo',
                'mpb', 'latin', 'latino'
            ],
            
            'Global Sounds': [
                'indian', 'iranian', 'malay', 'turkish', 'tango', 'afrobeat', 'french', 'german', 'british', 'swedish'
            ],
            
            'Jazz and Soul': [
                'blues', 'bluegrass', 'funk', 'gospel', 'jazz', 'soul', 'groove', 'disco', 'ska'
            ],
            
            'Varied Themes': [
                'children', 'disney', 'forro', 'kids', 'party', 'romance', 'show-tunes',
                'comedy', 'anime'
            ],
            
            'Instrumental': [
                'acoustic', 'classical',  'guitar', 'piano',
                'world-music', 'opera', 'new-age'
            ],
            
            'Mood': [
                'ambient', 'chill', 'happy', 'sad', 'sleep', 'study'
            ],
            
            'Single Genre': [
                'country', 'honky-tonk', 'folk', 'singer-songwriter'
            ]
        }
        
        genre_category_mapping = {genre: category for category, genres in genre_mapping.items() for genre in genres}
        df["track_genre"] = df["track_genre"].map(genre_category_mapping)
        
        # Remove duplicates - Fourth step: track_name and artist case
        subset_cols = [col for col in df.columns if col not in ["track_id", "album_name"]]
        df = df.drop_duplicates(subset=subset_cols, keep="first")
        
        # Remove duplicate - Fifth step: duplicated rows with some differences
        df = (df
                .sort_values(by="popularity", ascending=False)
                .groupby(["track_name", "artists"])
                .head(1)
                .sort_index()
                .reset_index(drop=True))
        
        # Create column - duration_min
        df["duration_min"] = (df["duration_ms"]
                                .apply(lambda x: f"{x // 60000}"))
        
        df["duration_min"] = df["duration_min"].astype(int)

        # Create column - duration_category
        df["duration_category"] = df["duration_ms"].apply(categorize_duration)
        
        # Create column - popularity_category
        df["popularity_category"] = df["popularity"].apply(categorize_popularity)
        
        # Create column - track_mood
        df["track_mood"] = df["valence"].apply(determine_mood)
        
        # Create column - live_performance
        df["live_performance"] = df["liveness"] > 0.8
        
        # Dropping columns
        df = df.drop(columns=["loudness", "mode", "duration_ms", "key", "tempo", "valence", "speechiness", "acousticness", "instrumentalness", "liveness", "time_signature"])

        logging.info(f"The dataframe has been cleaned and transformed. You are left with {df.shape[0]} rows and {df.shape[1]} columns.")
        
        return df
    except Exception as e:
        logging.error(f"An error has occurred: {e}.")
        
  
