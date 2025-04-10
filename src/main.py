from constants import movies_output_path, ratings_output_path, processed_data
from extract import download_movies_zip
from transform import preprocesamiento


if __name__ == "__main__":
    download_movies_zip()

    df_movies, df_ratings = preprocesamiento()

    df_movies.to_feather(movies_output_path)
    
    df_ratings.to_feather(ratings_output_path)

    print(f"Dataset limpio, transformado y guardado correctamente en \n{processed_data}")
