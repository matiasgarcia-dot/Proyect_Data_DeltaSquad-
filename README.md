# Proyect_Data_DeltaSquad-
Proyecto de data del grupo DeltaSquad para nocountry

# 🎬 Proyecto de Limpieza y Transformación de Datos de Películas

Este proyecto tiene como objetivo preparar un dataset de películas para su análisis y para ser utilizado en sistemas de recomendación. El flujo actual incluye la extracción de datos crudos, su limpieza y transformación, y el guardado del resultado final en un archivo procesado.
La data usada es un csv de peliculas de esta pagina: https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies
---

## 📂 Estructura del Proyecto

- `SRC/data/raw_data/`: contiene el dataset original (`data.csv`).
- `SRC/data/processed_data/`: contiene el dataset limpio (`movies_clean.csv`).
- `SRC/scripts/`: incluye los scripts de extracción y transformación de datos.
- `SRC/notebooks/`: carpeta destinada a análisis exploratorio (EDA).
- `README.md`: documentación general del proyecto.
- `requirements.txt`: dependencias del proyecto.

---
## 🧪 Instalación

Recuerda activar el entorno virtual para trabajar bien!!
Windows:

Para activarlo:
venv/scripts/activate


---
### RECORDATORIO!!:
Una ves que termines tu parte y hayas intalados otras librerias debes agregarlas al archivo requirements.txt para que el siguiente no tenga errores:

Para hacerlo:
pip freeze > requirements.txt 

---
## 🔁 Flujo de Trabajo Actual

1. **Extracción:**
   - Lectura del archivo original `data.csv` desde la carpeta `raw_data`.

2. **Transformación:**
   - Revisión de valores nulos y tipos de datos.
   - Eliminación de columnas irrelevantes.
   - Conversión de columnas numéricas y de fechas.
   - Eliminación de registros incompletos o duplicados.
   - Relleno de campos no críticos vacíos.
   - Selección de columnas útiles para análisis o sistemas de recomendación.
   
   - title                        object
   - genres                       object
   - original_language            object
   - overview                     object
   - popularity                  float64
   - release_date         datetime64[ns]
   - runtime                     float64
   - vote_average                float64
   - vote_count                  float64

   - Ordenamiento del dataset por calificación promedio (`vote_average`).


3. **Exportación:**
   - Guardado del dataset limpio en la carpeta `processed_data`.

---

## ✅ Estado del Proyecto

✔ Extracción implementada  
✔ Limpieza y transformación completadas  
⬜ Análisis exploratorio (EDA) pendiente  
⬜ Desarrollo del sistema de recomendación  
⬜ Visualizaciones o dashboards

---



