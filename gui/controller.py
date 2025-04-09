from gui.views import MainView, NameInputView, MovieRatingView, RecommendationsView

class FilmIAController:
    def __init__(self, root):
        self.root = root
        self.root.title("FilmIA")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Variables para almacenar datos del usuario
        self.user_name = ""
        self.rated_movies = {}  # Diccionario para almacenar {movie_name: rating}
        
        # Inicializar las vistas
        self.main_view = MainView(root, self)
        self.name_input_view = NameInputView(root, self)
        self.movie_rating_view = MovieRatingView(root, self)
        self.recommendations_view = RecommendationsView(root, self)
        
        # Mostrar la vista principal inicialmente
        self.show_main_view()
        
    def on_discover_click(self):
        # Cambiar a la pantalla de ingreso de nombre
        self.show_name_input_view()
    
    def on_start_click(self, name):
        # Guardar el nombre del usuario
        self.user_name = name
        print(f"Nombre ingresado: {self.user_name}")
        # Navegar a la pantalla de calificación de películas
        self.show_movie_rating_view()
    
    def on_rate_movie(self, movie_name, rating):
        # Guardar la calificación de la película
        if movie_name and rating > 0:
            self.rated_movies[movie_name] = rating
            print(f"Película calificada: {movie_name} - {rating}/10")
            return True
        return False
    
    def on_next_to_recommendations(self):
        # Verificar si el usuario ha calificado al menos una película
        if not self.rated_movies:
            return False
        # Navegar a la pantalla de recomendaciones
        self.show_recommendations_view()
        return True
    
    def get_recommendations(self):
        # Esta función simula obtener recomendaciones basadas en las calificaciones
        # En el futuro, se conectará a una base de datos real
        
        # Por ahora, simplemente devuelve una lista de películas de ejemplo
        # que no hayan sido calificadas por el usuario
        rated_movies_set = set(self.rated_movies.keys())
        example_movies = [
            "Volver al Futuro", "El Silencio de los Inocentes", "Gladiador",
            "El Gran Lebowski", "Parásitos", "Joker", "La La Land",
            "Coco", "El Laberinto del Fauno", "Mad Max: Fury Road"
        ]
        
        # Filtrar películas que no han sido calificadas
        recommendations = [movie for movie in example_movies if movie not in rated_movies_set]
        
        # Devolver hasta 5 recomendaciones
        return recommendations[:5]
    
    def show_main_view(self):
        # Ocultar todas las vistas y mostrar la principal
        self.name_input_view.hide()
        self.movie_rating_view.hide()
        self.recommendations_view.hide()
        self.main_view.show()
    
    def show_name_input_view(self):
        # Ocultar todas las vistas y mostrar la de ingreso de nombre
        self.main_view.hide()
        self.movie_rating_view.hide()
        self.recommendations_view.hide()
        self.name_input_view.show()
    
    def show_movie_rating_view(self):
        # Ocultar todas las vistas y mostrar la de calificación de películas
        self.main_view.hide()
        self.name_input_view.hide()
        self.recommendations_view.hide()
        self.movie_rating_view.show()
    
    def show_recommendations_view(self):
        # Ocultar todas las vistas y mostrar la de recomendaciones
        self.main_view.hide()
        self.name_input_view.hide()
        self.movie_rating_view.hide()
        self.recommendations_view.show()