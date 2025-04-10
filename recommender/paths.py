"""
Para la siguiente lo podemos convertir en paquetes
e importar las rutas de uno comun
o mejor, mudarlo todo a la aplicacion la parte de recomendador :P
"""

import pyprojroot


root_path = pyprojroot.here()

processed_data =  root_path / data_path / 'processed_data'
knn_path =  processed_data / 'knn_model.joblib'
movies_output_path = processed_data / 'movies.feather'
ratings_output_path = processed_data / 'ratings.feather'
