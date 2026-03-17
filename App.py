import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MovieLens Analysis",
    page_icon="🎬",
    layout="wide"
)

# ─── Data Loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    datasets_folder = os.path.join(os.path.dirname(__file__), "datasets")
    try:
        movies  = pd.read_csv(os.path.join(datasets_folder, "movies.csv"))
        ratings = pd.read_csv(os.path.join(datasets_folder, "ratings.csv"))
        tags    = pd.read_csv(os.path.join(datasets_folder, "tags.csv"))
        links   = pd.read_csv(os.path.join(datasets_folder, "links.csv"))
        return movies, ratings, tags, links
    except Exception as e:
        st.error(f"Could not load datasets: {e}")
        return None, None, None, None

def split_genres(genre_str):
    if isinstance(genre_str, str):
        return genre_str.split('|')
    return []

def assign_grade(r):
    if r >= 4.5: return "A+"
    elif r >= 4.0: return "A"
    elif r >= 3.5: return "B+"
    elif r >= 3.0: return "B"
    else: return "C"

# ─── Load Data ─────────────────────────────────────────────────────────────────
movies, ratings, tags, links = load_data()

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
st.sidebar.title("🎬 MovieLens Analysis")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📋 Dataset Info",
    "⭐ Ratings Distribution",
    "🎭 Genre Distribution",
    "🏆 Top Movies",
    "🔍 Movie Deep Dive"
])

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("🎬 MovieLens Data Analysis")
    st.markdown("Explore movie ratings, genres, and trends from the MovieLens dataset.")

    if movies is not None:
        st.markdown("### 📊 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎥 Movies",  f"{len(movies):,}")
        col2.metric("⭐ Ratings", f"{len(ratings):,}")
        col3.metric("🏷️ Tags",    f"{len(tags):,}")
        col4.metric("🔗 Links",   f"{len(links):,}")

        st.markdown("---")
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### 🎭 Top 10 Genres")
            genre_counts = {}
            for g in movies['genres']:
                for genre in split_genres(g):
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
            genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
            genre_df = genre_df.sort_values('Count', ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(x='Count', y='Genre', data=genre_df, palette='viridis', ax=ax)
            ax.set_title("Top 10 Genres")
            st.pyplot(fig)
            plt.close()

        with col_right:
            st.markdown("### ⭐ Ratings Overview")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.histplot(ratings['rating'], bins=10, kde=True, color='steelblue', ax=ax2)
            ax2.set_title("Ratings Distribution")
            ax2.set_xlabel("Rating")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)
            plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DATASET INFO  (was CLI Option 1)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Dataset Info":
    st.title("📋 Dataset Info")

    if movies is not None:
        tab1, tab2, tab3, tab4 = st.tabs(["🎥 Movies", "⭐ Ratings", "🏷️ Tags", "🔗 Links"])

        for tab, df, name in zip(
            [tab1, tab2, tab3, tab4],
            [movies, ratings, tags, links],
            ["Movies", "Ratings", "Tags", "Links"]
        ):
            with tab:
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows",    f"{df.shape[0]:,}")
                col2.metric("Columns", df.shape[1])
                col3.metric("Nulls",   int(df.isnull().sum().sum()))
                st.markdown("**Column Types**")
                st.dataframe(df.dtypes.rename("dtype").reset_index().rename(columns={"index": "Column"}), use_container_width=True)
                st.markdown("**Sample Rows**")
                st.dataframe(df.head(10), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RATINGS DISTRIBUTION  (was CLI Option 2)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⭐ Ratings Distribution":
    st.title("⭐ Ratings Distribution")

    if ratings is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ratings", f"{len(ratings):,}")
        col2.metric("Average Rating", f"{ratings['rating'].mean():.2f}")
        col3.metric("Unique Raters", f"{ratings['userId'].nunique():,}")

        st.markdown("---")
        chart_type = st.radio("Chart type", ["Histogram", "Bar Chart"], horizontal=True)
        color = st.color_picker("Bar color", "#4C72B0")

        fig, ax = plt.subplots(figsize=(9, 4))
        if chart_type == "Histogram":
            sns.histplot(ratings['rating'], bins=10, kde=True, color=color, ax=ax)
        else:
            rating_counts = ratings['rating'].value_counts().sort_index()
            ax.bar(rating_counts.index, rating_counts.values, width=0.4, color=color)
        ax.set_title("Distribution of Movie Ratings")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GENRE DISTRIBUTION  (was CLI Option 3)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎭 Genre Distribution":
    st.title("🎭 Genre Distribution")

    if movies is not None:
        genre_counts = {}
        for g in movies['genres']:
            for genre in split_genres(g):
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
        genre_df = genre_df.sort_values('Count', ascending=False)

        top_n = st.slider("Show top N genres", min_value=5, max_value=len(genre_df), value=15)
        chart_style = st.radio("Chart style", ["Horizontal Bar", "Pie Chart"], horizontal=True)

        genre_top = genre_df.head(top_n)
        fig, ax = plt.subplots(figsize=(9, 5))

        if chart_style == "Horizontal Bar":
            sns.barplot(x='Count', y='Genre', data=genre_top, palette='viridis', ax=ax)
            ax.set_title(f"Top {top_n} Genres by Movie Count")
        else:
            ax.pie(genre_top['Count'], labels=genre_top['Genre'], autopct='%1.1f%%', startangle=140)
            ax.set_title(f"Top {top_n} Genre Share")

        st.pyplot(fig)
        plt.close()

        st.markdown("**Full Genre Table**")
        st.dataframe(genre_df.reset_index(drop=True), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — TOP MOVIES  (was CLI Option 4)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Top Movies":
    st.title("🏆 Top Movies Grading Table")

    if movies is not None and ratings is not None:
        min_votes = st.slider("Minimum number of ratings", 1, 500, 50)
        top_n     = st.slider("Number of top movies to show", 5, 50, 10)

        vote_counts = ratings.groupby('movieId')['rating'].count().reset_index()
        vote_counts.columns = ['movieId', 'vote_count']

        avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
        avg_ratings = avg_ratings.merge(vote_counts, on='movieId')
        avg_ratings = avg_ratings[avg_ratings['vote_count'] >= min_votes]
        avg_ratings = avg_ratings.merge(movies[['movieId', 'title', 'genres']], on='movieId')

        top_movies = avg_ratings.sort_values('rating', ascending=False).head(top_n).reset_index(drop=True)
        top_movies['Grade'] = top_movies['rating'].apply(assign_grade)
        top_movies['rating'] = top_movies['rating'].round(2)
        top_movies.index += 1

        st.dataframe(
            top_movies[['title', 'genres', 'rating', 'vote_count', 'Grade']].rename(columns={
                'title': 'Title', 'genres': 'Genres',
                'rating': 'Avg Rating', 'vote_count': 'Votes'
            }),
            use_container_width=True
        )

        csv = top_movies.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "top_movies.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — MOVIE DEEP DIVE  (was CLI Option 5)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Movie Deep Dive":
    st.title("🔍 Movie Deep Dive")

    if movies is not None and ratings is not None:
        search = st.text_input("Search for a movie", placeholder="e.g. Toy Story")
        filtered = movies[movies['title'].str.contains(search, case=False, na=False)] if search else movies

        if filtered.empty:
            st.warning("No movies found. Try a different search.")
        else:
            movie_options = filtered['title'].sort_values().tolist()
            selected_title = st.selectbox("Select a movie", movie_options)

            movie_row  = movies[movies['title'] == selected_title].iloc[0]
            movie_id   = movie_row['movieId']
            movie_ratings = ratings[ratings['movieId'] == movie_id]

            col1, col2, col3 = st.columns(3)
            col1.metric("Genres", movie_row['genres'].replace('|', ', '))
            col2.metric("Total Ratings", len(movie_ratings))
            col3.metric("Avg Rating", f"{movie_ratings['rating'].mean():.2f}" if not movie_ratings.empty else "N/A")

            if not movie_ratings.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(movie_ratings['rating'], bins=10, color='purple', edgecolor='black')
                ax.set_title(f"Ratings for {selected_title}")
                ax.set_xlabel("Rating")
                ax.set_ylabel("Number of Users")
                st.pyplot(fig)
                plt.close()

                # Tags for this movie
                if tags is not None:
                    movie_tags = tags[tags['movieId'] == movie_id]['tag']
                    if not movie_tags.empty:
                        st.markdown("**🏷️ User Tags**")
                        st.write(", ".join(movie_tags.dropna().unique().tolist()))

                # IMDb / TMDb links
                if links is not None:
                    link_row = links[links['movieId'] == movie_id]
                    if not link_row.empty:
                        imdb_id = link_row.iloc[0].get('imdbId', None)
                        tmdb_id = link_row.iloc[0].get('tmdbId', None)
                        link_cols = st.columns(2)
                        if pd.notna(imdb_id):
                            link_cols[0].markdown(f"[🎬 IMDb Page](https://www.imdb.com/title/tt{int(imdb_id):07d}/)")
                        if pd.notna(tmdb_id):
                            link_cols[1].markdown(f"[🎥 TMDb Page](https://www.themoviedb.org/movie/{int(tmdb_id)})")
            else:
                st.info("No ratings found for this movie.")