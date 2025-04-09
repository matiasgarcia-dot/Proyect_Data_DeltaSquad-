from src.extract import df
import pandas as pd

# Ver estructura inicial
print("Valores nulos por columna:")
print(df.isnull().sum())
print("\nTipos de datos iniciales:")
print(df.dtypes)


# Eliminar columnas innecesarias
df = df.drop(columns=["id", "status", "tagline","budget","revenue","production_companies","credits","keywords","poster_path","backdrop_path","recommendations"])


# Convertir columnas numéricas correctamente
df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce")
df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")


# Convertir fecha a datetime
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")


# Eliminar filas que tengan valores críticos faltantes
df = df.dropna(subset=["title", "release_date", "runtime"])


# Rellenar otros valores nulos que no sean críticos
df["overview"] = df["overview"].fillna("No overview")
df["genres"] = df["genres"].fillna("Unknown")


# Eliminar duplicados
df = df.drop_duplicates()


# ✅ Seleccionar columnas relevantes para análisis o recomendación
columnas_utiles = [
     "title", "genres", "original_language", "overview", "popularity",
    "release_date", "runtime",
    "vote_average", "vote_count"
]

df=df[columnas_utiles]


# Ordenar por rating promedio (de mayor a menor)
df = df.sort_values(by="vote_average", ascending=False).reset_index(drop=True)
df.head()



# Guardar DataFrame limpio
df.to_csv("data/processed_data/movies_clean.csv", index=False)

print(" Dataset limpio, transformado y guardado correctamente.")

