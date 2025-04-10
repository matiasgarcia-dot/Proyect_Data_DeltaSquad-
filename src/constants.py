import pyprojroot

"""
en realidad se puede hacer varias carpetas pero para poner más archivos
y no repetir rutas le puse así de dos en dos xD
"""

url_ml_last_small = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

root_path = pyprojroot.here()
data_path = root_path / 'data'

raw_data = data_path / 'raw_data'
ml_zip = raw_data / 'ml-latest-small.zip'
ml_path = raw_data / 'ml-latest-small'
movies_path = ml_path / 'movies.csv'
ratings_path = ml_path / 'ratings.csv'

processed_data =  data_path / 'processed_data'
knn_path =  processed_data / 'knn_model.joblib'
movies_output_path = processed_data / 'movies.feather'
ratings_output_path = processed_data / 'ratings.feather'
