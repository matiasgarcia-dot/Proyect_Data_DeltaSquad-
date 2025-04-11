# paths.py
"""
Módulo para gestionar las rutas de archivos del proyecto
"""

import os
import pyprojroot

# Obtener la ruta raíz del proyecto
root_path = pyprojroot.here()

# Definir rutas para los archivos de datos
processed_data = root_path / 'data' / 'processed_data'
knn_path = processed_data / 'knn_model.joblib'
movies_output_path = processed_data / 'movies.feather'
ratings_output_path = processed_data / 'ratings.feather'

# Asegurar que el directorio de datos procesados existe
os.makedirs(processed_data, exist_ok=True)