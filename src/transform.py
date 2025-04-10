def preprocesamiento():
    import pandas as pd
    import re
    from constants import movies_path, ratings_path
    
    
    df_movies = pd.read_csv(movies_path)
    
    df_ratings = pd.read_csv(ratings_path)
    
    df_movies.dropna(inplace=True)
    df_ratings.dropna(inplace=True)

    df_movies.drop_duplicates(
        subset=['movieId'],
        keep='first',
        inplace=True
    )

    df_ratings.drop_duplicates(
        subset=['movieId', 'userId'],
        keep='first',
        inplace=True
    )

    df_movies['content'] = df_movies.genres.str.replace('|', ' ')
    df_movies['genre_set'] = df_movies['content'].apply(
        lambda x: set(x.split())
    )

    df_movies['genre'] = df_movies['genre_set'].apply(
        lambda genres: ', '.join(sorted(genres))
    )

    df_movies.drop(['genres', 'content', 'genre_set'], axis=1, inplace=True)

    df_ratings['timestamp'] = pd.to_datetime(
        df_ratings['timestamp'], unit='s'
    )

    def extract_year(title):
        year = re.search(r'\((\d{4})\)', title)
        return year.group(1) if year else None

    df_movies['year'] = df_movies['title'].apply(extract_year)

    df_movies['title'] = df_movies['title'].str.replace(
        r'^(.*),\s(The|An|A)\s(\(\d{4}\))$', r'\2 \1 \3', regex=True
    )

    cambios = {
        168358: 2851,
        26958: 838,
        64997: 34048,
        32600: 147002,
        6003: 144606,
    }

    df_ratings['movieId'] = df_ratings['movieId'].replace(cambios)
    
    return df_movies, df_ratings
