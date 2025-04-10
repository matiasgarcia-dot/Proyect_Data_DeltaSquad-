# Proyect_Data_DeltaSquad-

Proyecto de data del grupo DeltaSquad para nocountry

# 🎬 Proyecto de Limpieza y Transformación de Datos de Películas

Este proyecto tiene como objetivo preparar un dataset de películas para su análisis y para ser utilizado en sistemas de recomendación. El flujo actual incluye la extracción de datos crudos, su limpieza y transformación, y el guardado del resultado final en un archivo procesado.
La data usada es un csv de peliculas de esta pagina: 
---

## 📂 Estructura del Proyecto

- `SRC/data/raw_data/`: contiene el dataset original.
- `SRC/data/processed_data/`: contiene el dataset limpio en formato feather y el modelo.
- `SRC/scripts/`: incluye los scripts de extracción y transformación de datos.
- `SRC/notebooks/`: carpeta destinada a análisis exploratorio (EDA).
- `README.md`: documentación general del proyecto.
- `requirements.txt`: dependencias del proyecto.

---
## 🧪 Instalación

Recuerda CREAR un entorno virtual para trabajar bien!!
Windows:
Para crearlo:
python -m venv <nombred entorno>

Para activarlo:
nombred entorno/scripts/activate


---
### RECORDATORIO!!:
Una ves que termines tu parte y hayas intalados otras librerias debes agregarlas al archivo requirements.txt para que el siguiente no tenga errores:

Para hacerlo:
pip freeze > requirements.txt 

---
## 🔁 Flujo de Trabajo Actual

1. **Extracción:**
   - Descargar y lectura del archivo original desde la carpeta `raw_data`.

2. **Transformación:**
   - Revisión de valores nulos y tipos de datos.
   - Eliminación de columnas irrelevantes.
   - Conversión de columnas numéricas y de fechas.
   - Eliminación de registros incompletos o duplicados.
   - Relleno de campos no críticos vacíos.
   - Selección de columnas útiles para análisis o sistemas de recomendación.
  
  > [!note]
  > usamos dos csvs movies y ratings que son los votos de los usuarios :P


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

## Integrantes
- [X] Lucel Da Silva
- [X] Agustín Garcia
- [X] Macarena Muñoz
- [X] Matías Garcia
