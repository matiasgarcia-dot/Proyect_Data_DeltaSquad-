import pandas as pd
from joblib import load
from logic import recomendacion_knn, normalizar_matrix
from paths import ratings_output_path, movies_output_path, knn_path


df_movies = pd.read_feather(movies_output_path)

df_ratings = pd.read_feather(ratings_output_path)

df_final = pd.merge(df_ratings, df_movies, on='movieId', how='inner')


"""
# TODO
Para la app llamar la lista
titles_movies = df_final.title.tolist()

movie_id = df_final[df_final['title'] == title]['movieId'].values[0]

para ayudar a hacer el usuario que está más abajo :P
"""

ratings_matrix_normalized, ratings_matrix = normalizar_matrix(df_final)

knn_model = load(knn_path)

"""
Para probar si lee puedes probar el 

print(df_final.info)
print(len(df_final))
"""
"""
# TODO
# Este no sé donde poner, para que me muestre los títulos en la app
# usuario que viene de la app para que devuelva asi

usuario = 603

o 
usuario = pd.Series({
    356: 4,
    58559: 5,
    1: 4
})

recomendaciones = recomendacion_knn(
    usuario, ratings_matrix_normalized, ratings_matrix, df_movies, knn_model
)
recomendaciones
"""