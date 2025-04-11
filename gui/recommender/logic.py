# logic.py
"""
Módulo que contiene la lógica de recomendación de películas
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from joblib import dump, load
from datetime import datetime
import os

def normalizar_matrix(df_final: pd.DataFrame):
    """
    Normaliza la matriz de calificaciones para mejorar las recomendaciones.
    
    Args:
        df_final: DataFrame con las columnas userId, movieId y rating
        
    Returns:
        Tuple con la matriz normalizada y la matriz original
    """
    # Agrupar por usuario y película, promediando calificaciones duplicadas
    df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
    
    # Crear matriz pivote de usuarios x películas
    ratings_matrix = df_agg.pivot(index='userId', columns='movieId', values='rating')
    
    # Calcular calificación promedio por usuario
    avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
    
    # Normalizar restando la calificación promedio
    ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
    
    return ratings_matrix_normalized, ratings_matrix


def guardar_nueva_recomendacion(ratings_matrix_normalized, processed_data_path):
    """
    Crea y guarda un nuevo modelo KNN para recomendaciones.
    
    Args:
        ratings_matrix_normalized: Matriz normalizada de calificaciones
        processed_data_path: Ruta donde guardar el modelo
        
    Returns:
        Ruta donde se guardó el modelo
    """
    # Crear timestamp para el nombre del archivo
    nueva_ejecucion = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    # Crear y entrenar modelo KNN
    prototipo_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    prototipo_knn.fit(ratings_matrix_normalized.values)
    
    # Definir nombre y ruta del archivo
    nombre_prototipo = f'{nueva_ejecucion}_knn_model.joblib'
    prototipo_path = processed_data_path / nombre_prototipo
    
    # Guardar modelo
    dump(prototipo_knn, prototipo_path)
    
    print(f"Modelo guardado en {prototipo_path}")
    return prototipo_path


def recomendacion_knn(
        usuario_id_o_ratings, ratings_matrix_normalized,
        ratings_matrix, df_movies, knn_model, n_recommendations: int = 10
    ):
    """
    Genera recomendaciones de películas usando KNN.
    
    Args:
        usuario_id_o_ratings: ID de usuario o Series con calificaciones {movieId: rating}
        ratings_matrix_normalized: Matriz normalizada de calificaciones
        ratings_matrix: Matriz original de calificaciones
        df_movies: DataFrame con información de películas
        knn_model: Modelo KNN entrenado
        n_recommendations: Número de recomendaciones a devolver
        
    Returns:
        DataFrame con las películas recomendadas
    """
    # Caso 1: El usuario es un Series de calificaciones (usuario nuevo)
    if isinstance(usuario_id_o_ratings, pd.Series):
        # Convertir a DataFrame
        usuario_id_o_ratings = pd.DataFrame(usuario_id_o_ratings).transpose()
        
        # Completar con todas las columnas de la matriz original
        usuario_id_o_ratings_complete = usuario_id_o_ratings.reindex(columns=ratings_matrix.columns)
        
        # Normalizar calificaciones del usuario
        avg_user = usuario_id_o_ratings_complete.mean(axis=1)
        usuario_id_o_ratings_normalized = usuario_id_o_ratings_complete.sub(avg_user, axis=0).fillna(0)
        
        # Encontrar vecinos más cercanos
        distances, indices = knn_model.kneighbors(
            usuario_id_o_ratings_normalized.values, 
            n_neighbors=n_recommendations + 1
        )
    
    # Caso 2: El usuario es un ID existente en la matriz
    else:
        # Obtener índice del usuario
        user_idx = ratings_matrix.index.get_loc(usuario_id_o_ratings)
        
        # Encontrar vecinos más cercanos
        distances, indices = knn_model.kneighbors(
            ratings_matrix_normalized.iloc[user_idx, :].values.reshape(1, -1), 
            n_neighbors=n_recommendations + 1
        )

    # Procesar resultados
    distances = distances.flatten()[1:]  # Ignorar el primer resultado (el propio usuario)
    indices = indices.flatten()[1:]
    
    # Obtener usuarios similares
    similar_users = ratings_matrix_normalized.iloc[indices]
    
    # Calcular calificaciones ponderadas por distancia
    mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
    mean_ratings_df = pd.DataFrame(mean_ratings, index=ratings_matrix.columns, columns=['mean_rating'])
    mean_ratings_df = mean_ratings_df.dropna()

    # Identificar películas ya vistas para excluirlas
    if isinstance(usuario_id_o_ratings, pd.DataFrame):
        seen_movies = usuario_id_o_ratings.dropna(axis=1).columns
    else:
        seen_movies = ratings_matrix.loc[usuario_id_o_ratings].dropna().index

    # Filtrar películas ya vistas y ordenar por calificación
    recommendations = mean_ratings_df[~mean_ratings_df.index.isin(seen_movies)]
    recommendations = recommendations.sort_values('mean_rating', ascending=False).head(n_recommendations)
    
    # Unir con información de películas
    try:
        recommendations = recommendations.merge(
            df_movies[['movieId', 'title', 'genres']], 
            left_index=True, 
            right_on='movieId'
        )
    except KeyError:
        # Si 'genres' no existe, intentar con 'genre'
        try:
            recommendations = recommendations.merge(
                df_movies[['movieId', 'title', 'genre']], 
                left_index=True, 
                right_on='movieId'
            )
        except KeyError:
            # Si ninguno existe, solo usar título
            recommendations = recommendations.merge(
                df_movies[['movieId', 'title']], 
                left_index=True, 
                right_on='movieId'
            )
    
    # Devolver solo los títulos
    recommendations = recommendations[['title']]

    return recommendations


def buscar_peliculas(query, df_movies, max_results=10):
    """
    Busca películas que coincidan con la consulta.
    
    Args:
        query: Texto a buscar
        df_movies: DataFrame con información de películas
        max_results: Número máximo de resultados
        
    Returns:
        Lista de títulos de películas que coinciden
    """
    if not query:
        return []
    
    # Convertir a minúsculas para búsqueda insensible a mayúsculas
    query = query.lower()
    
    # Buscar coincidencias en el título
    matches = df_movies[df_movies['title'].str.lower().str.contains(query)]
    
    # Devolver los primeros max_results resultados
    return matches.head(max_results)['title'].tolist() 
