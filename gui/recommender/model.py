# model.py
"""
Módulo para cargar y gestionar el modelo de recomendación
"""

import pandas as pd
import numpy as np
from joblib import load
import os
from recommender.logic import normalizar_matrix, recomendacion_knn, guardar_nueva_recomendacion
from recommender.paths import ratings_output_path, movies_output_path, knn_path, processed_data


class MovieRecommendationModel:
    """Clase para gestionar el modelo de recomendación de películas"""
    
    def __init__(self):
        """Inicializa el modelo cargando los datos y el modelo KNN"""
        self.df_movies = None
        self.df_ratings = None
        self.df_final = None
        self.ratings_matrix_normalized = None
        self.ratings_matrix = None
        self.knn_model = None
        self.model_loaded = False
        
        # Intentar cargar los datos
        self.load_data()
    
    def load_data(self):
        """Carga los datos de películas y calificaciones"""
        try:
            # Verificar si existen los archivos
            if os.path.exists(movies_output_path) and os.path.exists(ratings_output_path):
                # Cargar datos
                self.df_movies = pd.read_feather(movies_output_path)
                self.df_ratings = pd.read_feather(ratings_output_path)
                
                # Unir datasets
                self.df_final = pd.merge(self.df_ratings, self.df_movies, on='movieId', how='inner')
                
                # Normalizar matriz de calificaciones
                self.ratings_matrix_normalized, self.ratings_matrix = normalizar_matrix(self.df_final)
                
                # Cargar modelo KNN
                if os.path.exists(knn_path):
                    self.knn_model = load(knn_path)
                    self.model_loaded = True
                    print("Modelo de recomendación cargado correctamente")
                else:
                    print("Archivo de modelo KNN no encontrado, creando uno nuevo...")
                    self._create_new_model()
                
                return True
            else:
                print("Archivos de datos no encontrados")
                self._create_sample_data()
                return False
        
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self._create_sample_data()
            return False
    
    def _create_new_model(self):
        """Crea un nuevo modelo KNN si no existe"""
        try:
            # Crear y guardar modelo
            guardar_nueva_recomendacion(self.ratings_matrix_normalized, processed_data)
            
            # Cargar el modelo recién creado
            if os.path.exists(knn_path):
                self.knn_model = load(knn_path)
                self.model_loaded = True
                print("Nuevo modelo KNN creado y cargado")
            else:
                print("Error al crear nuevo modelo KNN")
        except Exception as e:
            print(f"Error al crear nuevo modelo: {e}")
    
    def _create_sample_data(self):
        """Crea datos de ejemplo para demostración"""
        print("Creando datos de ejemplo para demostración...")
        
        # Crear DataFrame de películas de ejemplo
        movies_data = {
            'movieId': list(range(1, 13)),
            'title': [
                "El Padrino", "Titanic", "Star Wars: Episodio IV", 
                "Jurassic Park", "El Señor de los Anillos", "Matrix",
                "Forrest Gump", "Pulp Fiction", "El Rey León",
                "Interestelar", "Inception", "Avatar"
            ],
            'genres': [
                "Crime|Drama", "Drama|Romance", "Action|Adventure|Sci-Fi", 
                "Adventure|Sci-Fi", "Adventure|Fantasy", "Action|Sci-Fi",
                "Drama|Romance", "Crime|Drama", "Animation|Adventure|Drama",
                "Adventure|Drama|Sci-Fi", "Action|Adventure|Sci-Fi", "Action|Adventure|Fantasy"
            ]
        }
        self.df_movies = pd.DataFrame(movies_data)
        
        # Crear ratings de ejemplo (usuarios ficticios)
        ratings_data = []
        for user_id in range(1, 11):  # 10 usuarios ficticios
            for movie_id in range(1, 13):  # 12 películas
                # Generar algunas calificaciones aleatorias
                if np.random.random() > 0.3:  # 70% de probabilidad de calificar
                    rating = np.random.randint(1, 11)  # Calificación de 1 a 10
                    ratings_data.append({'userId': user_id, 'movieId': movie_id, 'rating': rating})
        
        self.df_ratings = pd.DataFrame(ratings_data)
        self.df_final = pd.merge(self.df_ratings, self.df_movies, on='movieId', how='inner')
        
        # Normalizar matriz y crear modelo KNN
        self.ratings_matrix_normalized, self.ratings_matrix = normalizar_matrix(self.df_final)
        
        # Crear modelo KNN con datos de ejemplo
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(self.ratings_matrix_normalized.values)
        self.knn_model = knn_model
        self.model_loaded = True
        
        print("Datos y modelo de ejemplo creados correctamente")
    
    def get_all_movies(self):
        """Devuelve la lista de todas las películas disponibles"""
        if self.df_movies is not None:
            return self.df_movies['title'].tolist()
        return []
    
    def search_movies(self, query, max_results=10):
        """Busca películas que coincidan con la consulta"""
        if self.df_movies is None or not query:
            return []
        
        # Convertir a minúsculas para búsqueda insensible a mayúsculas
        query = query.lower()
        
        # Buscar coincidencias en el título
        matches = self.df_movies[self.df_movies['title'].str.lower().str.contains(query)]
        
        # Devolver los primeros max_results resultados
        return matches.head(max_results)['title'].tolist()
    
    def get_movie_id(self, title):
        """Obtiene el ID de una película por su título"""
        if self.df_movies is None:
            return None
        
        movie = self.df_movies[self.df_movies['title'] == title]
        if not movie.empty:
            return movie.iloc[0]['movieId']
        return None
    
    def get_recommendations(self, rated_movies, n_recommendations=5):
        """
        Genera recomendaciones basadas en las películas calificadas.
        
        Args:
            rated_movies: Diccionario {movie_name: rating}
            n_recommendations: Número de recomendaciones a devolver
            
        Returns:
            Lista de títulos de películas recomendadas
        """
        if not self.model_loaded or not rated_movies:
            return []
        
        try:
            # Convertir calificaciones a formato esperado por el algoritmo
            movie_ids = {}
            for movie_name, rating in rated_movies.items():
                movie_id = self.get_movie_id(movie_name)
                if movie_id is not None:
                    movie_ids[movie_id] = rating
            
            # Si no hay IDs válidos, no podemos recomendar
            if not movie_ids:
                return []
            
            # Convertir a Series de pandas
            user_ratings = pd.Series(movie_ids)
            
            # Obtener recomendaciones
            recommendations_df = recomendacion_knn(
                user_ratings,
                self.ratings_matrix_normalized,
                self.ratings_matrix,
                self.df_movies,
                self.knn_model,
                n_recommendations=n_recommendations
            )
            
            # Devolver lista de títulos
            return recommendations_df['title'].tolist()
        
        except Exception as e:
            print(f"Error al generar recomendaciones: {e}")
            return []