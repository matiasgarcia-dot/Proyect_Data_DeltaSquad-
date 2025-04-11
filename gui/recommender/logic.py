import pandas as pd
import numpy as np


def normalizar_matrix(df_final: pd.DataFrame):
    df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
    ratings_matrix = df_agg.pivot(index='userId', columns='movieId', values='rating')
    avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
    ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
    return ratings_matrix_normalized, ratings_matrix



def guardar_nueva_recomendacion(ratings_matrix_normalized):
    """
    Este es para crear nuevo si se quiere,
    para sacar los valores usar la funcion normalizar_matrix
    # si falla el guardado poner import pyprojroot
    No hace falta volver a hacer porque ya estas en el repo el primero
    pero para agregar más gente se puede tener en cuenta para implementarlo
    """
    from paths import processed_data
    from datetime import datetime
    from sklearn.neighbors import NearestNeighbors
    from joblib import dump
    
    
    nueva ejecucion = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    prototipo_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    prototipo_knn.fit(ratings_matrix_normalized.values)
    
    nombre_prototipo = f'{}_knn_model.joblib'
    
    prototipo_path = processed_data / nombre_prototipo
    
    dump(prototipo_knn, prototipo_path)
    
    print(f"probar en {prototipo_path}")



def recomendacion_knn(
        usuario_id_o_ratings, ratings_matrix_normalized,
        ratings_matrix, df_movies, knn_model, n_recommendations: int = 10
    ):
    if isinstance(usuario_id_o_ratings, pd.Series):
        usuario_id_o_ratings = pd.DataFrame(usuario_id_o_ratings).transpose()
        usuario_id_o_ratings_complete = usuario_id_o_ratings.reindex(columns=ratings_matrix.columns)
        avg_user = usuario_id_o_ratings_complete.mean(axis=1)
        usuario_id_o_ratings_normalized = usuario_id_o_ratings_complete.sub(avg_user, axis=0).fillna(0)
        distances, indices = knn_model.kneighbors(usuario_id_o_ratings_normalized.values, n_neighbors=n_recommendations + 1)
    else:
        user_idx = ratings_matrix.index.get_loc(usuario_id_o_ratings)
        distances, indices = knn_model.kneighbors(
            ratings_matrix_normalized.iloc[user_idx, :].values.reshape(1, -1), n_neighbors=n_recommendations + 1
        )

    distances = distances.flatten()[1:]
    indices = indices.flatten()[1:]
    similar_users = ratings_matrix_normalized.iloc[indices]
    mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
    mean_ratings_df = pd.DataFrame(mean_ratings, index=ratings_matrix.columns, columns=['mean_rating'])
    mean_ratings_df = mean_ratings_df.dropna()

    if isinstance(usuario_id_o_ratings, pd.DataFrame):
        seen_movies = usuario_id_o_ratings.dropna(axis=1).columns
    else:
        seen_movies = ratings_matrix.loc[usuario_id_o_ratings].dropna().index

    recommendations = mean_ratings_df[~mean_ratings_df.index.isin(seen_movies)]
    recommendations = recommendations.sort_values('mean_rating', ascending=False).head(n_recommendations)
    recommendations = recommendations.merge(df_movies[['movieId', 'title', 'genre']], left_index=True, right_on='movieId')
    recommendations = recommendations[['title']]

    return recommendations
    
