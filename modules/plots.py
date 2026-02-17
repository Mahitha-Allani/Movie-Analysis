import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from modules.data_loader import get_data
from modules.utils import split_genres

def show_data_info():
    movies, ratings, tags, links = get_data()
    if movies is None:
        print("Error: Load datasets first!")
        return
    
    print(f"\nMovies: {movies.shape[0]} rows, {movies.shape[1]} columns")
    print(f"Ratings: {ratings.shape[0]} rows, {ratings.shape[1]} columns")
    print(f"Tags: {tags.shape[0]} rows, {tags.shape[1]} columns")
    print(f"Links: {links.shape[0]} rows, {links.shape[1]} columns")

def plot_ratings():
    movies, ratings, tags, links = get_data()
    if ratings is None:
        print("Error: Load datasets first!")
        return

    plt.figure(figsize=(8,4))
    sns.histplot(ratings['rating'], bins=10, kde=True, color='blue')
    plt.title("Distribution of Movie Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.show(block=True)

def plot_genres():
    movies, ratings, tags, links = get_data()
    if movies is None:
        print("Error: Load datasets first!")
        return

    genre_counts = {}
    for genres in movies['genres']:
        for genre in split_genres(genres):
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
    genre_df = genre_df.sort_values(by='Count', ascending=False)

    plt.figure(figsize=(10,5))
    sns.barplot(x='Count', y='Genre', data=genre_df, palette='viridis')
    plt.title("Movie Count per Genre")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.show(block=True)
def show_top_movies_grading(top_n=10):
    """
    Show top N movies in a grading table (average rating + grade)
    """
    movies, ratings, tags, links = get_data()
    if movies is None or ratings is None:
        print("Error: Load datasets first!")
        return

    # Calculate average rating per movie
    avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
    avg_ratings = avg_ratings.merge(movies[['movieId','title']], on='movieId')

    # Take top N movies by average rating
    top_movies = avg_ratings.sort_values(by='rating', ascending=False).head(top_n)
    
    # Optional: assign a grade based on average rating
    def assign_grade(r):
        if r >= 4.5:
            return "A+"
        elif r >= 4.0:
            return "A"
        elif r >= 3.5:
            return "B+"
        elif r >= 3.0:
            return "B"
        else:
            return "C"

    top_movies['Grade'] = top_movies['rating'].apply(assign_grade)
    
    # Print the table
    print("\nTop Movies Grading Table:")
    print(top_movies[['title', 'rating', 'Grade']].to_string(index=False))


def plot_single_movie_review_paginated(page_size=20):
    movies, ratings, tags, links = get_data()
    if movies is None or ratings is None:
        print("Error: Load datasets first!")
        return

    movies_sorted = movies.sort_values('title').reset_index(drop=True)
    total_movies = len(movies_sorted)
    total_pages = (total_movies + page_size - 1) // page_size
    current_page = 0

    while True:
        start = current_page * page_size
        end = min(start + page_size, total_movies)
        print(f"\nSelect a movie to view reviews (page {current_page+1}/{total_pages}):")
        for i in range(start, end):
            print(f"{i+1} - {movies_sorted.loc[i, 'title']}")
        print("n - next page, p - previous page, 0 - cancel")

        choice = input("Enter number: ").strip().lower()
        if choice == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif choice == 'p' and current_page > 0:
            current_page -= 1
        elif choice == '0':
            print("Cancelled.")
            return
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < total_movies:
                movie_id = movies_sorted.loc[idx, 'movieId']
                movie_title = movies_sorted.loc[idx, 'title']
                movie_ratings = ratings[ratings['movieId'] == movie_id]
                if movie_ratings.empty:
                    print("No ratings found for this movie.")
                    return
                import matplotlib.pyplot as plt
                plt.figure(figsize=(6,4))
                plt.hist(movie_ratings['rating'], bins=10, color='purple', edgecolor='black')
                plt.title(f"Ratings for {movie_title}")
                plt.xlabel("Rating")
                plt.ylabel("Number of Users")
                plt.show(block=True)
                return
            else:
                print("Invalid number. Try again.")
        else:
            print("Invalid input. Try again.")
