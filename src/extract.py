import requests
import zipfile
import os


def download_movies_zip():
    from constants import url_ml_last_small, ml_zip, raw_data
    
    
    response = requests.get(url_ml_last_small)
    with open(ml_zip, "wb") as f:
        f.write(response.content)


    with zipfile.ZipFile(ml_zip, 'r') as zip_ref:
        zip_ref.extractall(raw_data)

    print(f'Listo ve a ver en \n {raw_data}')
