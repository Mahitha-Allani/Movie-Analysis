import pandas as pd
import os

# Global datasets
movies = None
ratings = None
tags = None
links = None

def load_data(folder_path):
    """Load all datasets from a single folder"""
    global movies, ratings, tags, links
    
    try:
        movies = pd.read_csv(os.path.join(folder_path, "movies.csv"))
        ratings = pd.read_csv(os.path.join(folder_path, "ratings.csv"))
        tags = pd.read_csv(os.path.join(folder_path, "tags.csv"))
        links = pd.read_csv(os.path.join(folder_path, "links.csv"))
        print("Datasets loaded successfully!")
        return True
    except Exception as e:
        print(f"Failed to load datasets: {e}")
        return False

def get_data():
    return movies, ratings, tags, links
