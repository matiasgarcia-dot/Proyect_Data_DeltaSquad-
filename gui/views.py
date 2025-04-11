
# Cada clase es una pantalla:
#   - MainView: la pantalla de inicio (título, subtítulo, botón).
#   - NameInputView: solicita el nombre al usuario.
#   - MovieRatingView: permite al usuario hacer las calificaciones.
#   - RecommendationsView: recomendaciones de peliculas
# Cada vista es una clase que hereda de tk.Frame.

import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window, create_styled_button
from PIL import Image, ImageTk
import os

class MainView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        # Frame principal
        self.frame = tk.Frame(parent, bg="#ADD8E6")
        
        # Configurar el fondo celeste para toda la ventana
        self.parent.configure(bg="#ADD8E6")  # Color celeste claro
        
        # Frase superior
        self.phrase_label = tk.Label(
            self.frame,
            text="¿No sabes qué ver esta noche?",
            font=("Arial", 18),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.phrase_label.pack(pady=(50, 0))
        
        # Contenedor central para título y subtítulo
        self.center_frame = tk.Frame(self.frame, bg="#ADD8E6")
        self.center_frame.pack(expand=True)
        
        # Título Imagen
        logo_path= os.path.join("assets", "logo_filmia.png")
        try:
            image = Image.open(logo_path)
            image = image.resize((600, 180), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = tk.Label(
                self.center_frame,
                image=self.logo_image,
                bg="#ADD8E6"
            )
            self.logo_label.pack(pady=(0,10))
        except Exception as e:
            print(f"Error cargando la imagen: {e}")
            # Fallback en caso de error
            self.logo_label = tk.Label(
                self.center_frame,
                text="FilmIA",
                font=("Arial", 36, "bold"),
                bg="#ADD8E6",
                fg="#1E3A8A"
            )
            self.logo_label.pack(pady=(0,10))
        
        # Subtítulo
        self.subtitle_label = tk.Label(
            self.center_frame,
            text="recomendaciones hechas a tu medida",
            font=("Arial", 16, "italic"),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # Botón "descúbrelo ahora"
        self.discover_button = create_styled_button(
            self.center_frame,
            "descúbrelo ahora",
            self.controller.on_discover_click
        )
        self.discover_button.pack(pady=(0, 50))
    
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        self.frame.pack_forget()


class NameInputView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        # Frame principal
        self.frame = tk.Frame(parent, bg="#ADD8E6")
        
        # Contenedor central
        self.center_frame = tk.Frame(self.frame, bg="#ADD8E6")
        self.center_frame.pack(expand=True)
        
        # Título
        self.title_label = tk.Label(
            self.center_frame,
            text="Ingrese su nombre",
            font=("Arial", 24, "bold"),
            bg="#ADD8E6",
            fg="#1E3A8A"
        )
        self.title_label.pack(pady=(0, 30))
        
        # Campo de entrada para el nombre
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            self.center_frame,
            textvariable=self.name_var,
            font=("Arial", 14),
            width=30
        )
        self.name_entry.pack(pady=(0, 20))
        
        # Botón "comenzar"
        self.start_button = create_styled_button(
            self.center_frame,
            "comenzar",
            self.on_start_click
        )
        self.start_button.pack(pady=(0, 50))
    
    def on_start_click(self):
        name = self.name_var.get().strip()
        if name:
            self.controller.on_start_click(name)
        else:
            # Si el nombre está vacío, mostrar un mensaje de error
            messagebox.showerror("Error", "Por favor ingrese su nombre")
    
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Limpiar el campo de entrada y darle el foco
        self.name_var.set("")
        self.name_entry.focus()
    
    def hide(self):
        self.frame.pack_forget()


class MovieRatingView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        # Frame principal
        self.frame = tk.Frame(parent, bg="#ADD8E6")
        
        # Título principal
        self.title_frame = tk.Frame(self.frame, bg="#ADD8E6")
        self.title_frame.pack(fill=tk.X, pady=(30, 5))
        
        # Título centrado
        self.title_label = tk.Label(
            self.title_frame,
            text="Califica una película",
            font=("Arial", 28, "bold"),
            bg="#ADD8E6",
            fg="#1E3A8A"
        )
        self.title_label.pack(anchor=tk.CENTER)
        
        # Subtítulo con el nombre de usuario (a la izquierda)
        self.username_frame = tk.Frame(self.frame, bg="#ADD8E6", padx=50)
        self.username_frame.pack(fill=tk.X, pady=(0, 20), anchor=tk.W)
        
        self.username_label = tk.Label(
            self.username_frame,
            text="Usuario: ",
            font=("Arial", 14, "bold"),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.username_label.pack(side=tk.LEFT)
        
        self.username_value = tk.Label(
            self.username_frame,
            text="",  # Se actualizará al mostrar la vista
            font=("Arial", 14, "bold"),  # Ahora en negrita
            bg="#ADD8E6",
            fg="#1E3A8A"
        )
        self.username_value.pack(side=tk.LEFT)
        
        # Contenedor principal
        self.content_frame = tk.Frame(self.frame, bg="#ADD8E6", padx=50)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de búsqueda de películas
        self.search_frame = tk.Frame(self.content_frame, bg="#ADD8E6")
        self.search_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.search_label = tk.Label(
            self.search_frame,
            text="Selecciona una película que te guste para calificar",
            font=("Arial", 14),
            bg="#ADD8E6",
            fg="#333333",
            anchor=tk.W
        )
        self.search_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para la búsqueda
        self.search_input_frame = tk.Frame(self.search_frame, bg="#ADD8E6")
        self.search_input_frame.pack(fill=tk.X)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_input_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, pady=(0, 10))
        
        self.search_button = create_styled_button(
            self.search_input_frame,
            "Buscar",
            self.on_search
        )
        self.search_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        
        # Lista de resultados (simulada por ahora)
        self.results_frame = tk.Frame(self.search_frame, bg="#ADD8E6")
        self.results_frame.pack(fill=tk.X)
        
        self.results_label = tk.Label(
            self.results_frame,
            text="Resultados de búsqueda:",
            font=("Arial", 12, "bold"),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.results_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Listbox para mostrar resultados
        self.results_listbox = tk.Listbox(
            self.results_frame,
            font=("Arial", 12),
            height=5,
            width=50,
            selectmode=tk.SINGLE
        )
        self.results_listbox.pack(fill=tk.X)
        
        # Inicializar lista vacía de películas (se llenará en el método show)
        self.example_movies = []
        
        # Sección de calificación
        self.rating_frame = tk.Frame(self.content_frame, bg="#ADD8E6")
        self.rating_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.rating_label = tk.Label(
            self.rating_frame,
            text="Calificar",
            font=("Arial", 14, "bold"),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.rating_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para mostrar la película seleccionada
        self.selected_movie_frame = tk.Frame(self.rating_frame, bg="#ADD8E6")
        self.selected_movie_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.selected_movie_label = tk.Label(
            self.selected_movie_frame,
            text="Película seleccionada: ",
            font=("Arial", 12),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.selected_movie_label.pack(side=tk.LEFT)
        
        self.selected_movie_var = tk.StringVar(value="Ninguna")
        self.selected_movie_value = tk.Label(
            self.selected_movie_frame,
            textvariable=self.selected_movie_var,
            font=("Arial", 12, "bold"),
            bg="#ADD8E6",
            fg="#1E3A8A"
        )
        self.selected_movie_value.pack(side=tk.LEFT)
        
        # Frame para la calificación y el botón siguiente
        self.rating_buttons_frame = tk.Frame(self.rating_frame, bg="#ADD8E6")
        self.rating_buttons_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Frame para los botones de calificación
        self.stars_frame = tk.Frame(self.rating_buttons_frame, bg="#ADD8E6")
        self.stars_frame.pack(side=tk.LEFT)
        
        self.rating_var = tk.IntVar(value=0)
        self.rating_buttons = []
        
        # Crear botones de calificación del 1 al 10
        for i in range(1, 11):
            btn = ttk.Button(
                self.stars_frame,
                text=str(i),
                width=3,
                command=lambda i=i: self.set_rating(i)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.rating_buttons.append(btn)
        
        # Botón "siguiente" para ir a recomendaciones (ahora a la derecha de los números)
        self.next_button = create_styled_button(
            self.rating_buttons_frame,
            "Siguiente",
            self.on_next_click
        )
        self.next_button.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Etiqueta para mostrar la calificación seleccionada
        self.rating_display_frame = tk.Frame(self.rating_frame, bg="#ADD8E6")
        self.rating_display_frame.pack(fill=tk.X)
        
        self.rating_display_label = tk.Label(
            self.rating_display_frame,
            text="Tu calificación: ",
            font=("Arial", 12),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.rating_display_label.pack(side=tk.LEFT)
        
        self.rating_display_var = tk.StringVar(value="No calificado")
        self.rating_display_value = tk.Label(
            self.rating_display_frame,
            textvariable=self.rating_display_var,
            font=("Arial", 12, "bold"),
            bg="#ADD8E6",
            fg="#1E3A8A"
        )
        self.rating_display_value.pack(side=tk.LEFT)
        
        # Configurar eventos
        self.results_listbox.bind("<<ListboxSelect>>", self.on_select_movie)
    
    def on_search(self):
        """Busca películas que coincidan con el término de búsqueda"""
        search_term = self.search_var.get().strip()
        self.results_listbox.delete(0, tk.END)
        
        if search_term:
            # Usar el controlador para buscar películas en el dataset
            results = self.controller.search_movies(search_term)
            
            if results:
                for movie in results:
                    self.results_listbox.insert(tk.END, movie)
            else:
                self.results_listbox.insert(tk.END, "No se encontraron resultados")
        else:
            # Si no hay término de búsqueda, mostrar las primeras 20 películas
            all_movies = self.controller.get_all_movies()[:20]
            for movie in all_movies:
                self.results_listbox.insert(tk.END, movie)
    
    def on_select_movie(self, event):
        selection = self.results_listbox.curselection()
        if selection:
            movie = self.results_listbox.get(selection[0])
            if movie != "No se encontraron resultados":
                self.selected_movie_var.set(movie)
                # Resetear la calificación
                self.rating_var.set(0)
                self.rating_display_var.set("No calificado")
    
    def set_rating(self, rating):
        self.rating_var.set(rating)
        self.rating_display_var.set(f"{rating}/10")
        
        # Guardar automáticamente la calificación cuando el usuario selecciona una puntuación
        movie = self.selected_movie_var.get()
        if movie != "Ninguna":
            self.controller.on_rate_movie(movie, rating)
            # Se eliminó el mensaje emergente
    
    def on_next_click(self):
        # Verificar si hay al menos una película calificada
        if not self.controller.rated_movies:
            messagebox.showwarning("Advertencia", "Por favor califica al menos una película antes de continuar")
            return
            
        # Ir a la pantalla de recomendaciones
        success = self.controller.on_next_to_recommendations()
        
        if not success:
            messagebox.showwarning("Advertencia", "Por favor califica al menos una película antes de continuar")
    
    def on_submit_rating(self):
        movie = self.selected_movie_var.get()
        rating = self.rating_var.get()
        
        if movie == "Ninguna":
            messagebox.showerror("Error", "Por favor seleccione una película")
            return
        
        if rating == 0:
            messagebox.showerror("Error", "Por favor califique la película del 1 al 10")
            return
        
        # Enviar la calificación al controlador
        success = self.controller.on_rate_movie(movie, rating)
        
        if success:
            messagebox.showinfo("Éxito", f"Has calificado '{movie}' con {rating}/10")
            # Resetear la selección y calificación
            self.selected_movie_var.set("Ninguna")
            self.rating_var.set(0)
            self.rating_display_var.set("No calificado")
            self.results_listbox.selection_clear(0, tk.END)
    
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Actualizar el nombre de usuario en el subtítulo
        if self.controller.user_name:
            self.username_value.config(text=self.controller.user_name)
        
        # Cargar la lista de películas desde el controlador
        self.example_movies = self.controller.get_all_movies()
        
        # Mostrar las primeras 20 películas al inicio para no sobrecargar la UI
        self.results_listbox.delete(0, tk.END)
        for movie in self.example_movies[:20]:
            self.results_listbox.insert(tk.END, movie)
    
    def hide(self):
        self.frame.pack_forget()


class RecommendationsView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        # Frame principal
        self.frame = tk.Frame(parent, bg="#ADD8E6")
        
        # Título y subtítulo
        self.header_frame = tk.Frame(self.frame, bg="#ADD8E6")
        self.header_frame.pack(fill=tk.X, pady=(20, 30), padx=50)
        
        # Subtítulo en la parte superior derecha
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Películas Recomendadas Basadas en Tus Calificaciones:",
            font=("Arial", 14, "bold"),
            bg="#ADD8E6",
            fg="#333333"
        )
        self.subtitle_label.pack(anchor=tk.E)
        
        # Contenedor principal para las recomendaciones
        self.content_frame = tk.Frame(self.frame, bg="#ADD8E6", padx=50)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para mostrar las películas recomendadas
        self.recommendations_frame = tk.Frame(self.content_frame, bg="#ADD8E6")
        self.recommendations_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox para mostrar las recomendaciones
        self.recommendations_listbox = tk.Listbox(
            self.recommendations_frame,
            font=("Arial", 14),
            height=10,
            width=50,
            selectmode=tk.SINGLE,
            bg="#E6F7FF",  # Un azul más claro para el fondo
            bd=2,
            relief=tk.GROOVE
        )
        self.recommendations_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Mensaje para cuando no hay recomendaciones
        self.no_recommendations_label = tk.Label(
            self.recommendations_frame,
            text="Aquí se mostrarán tus recomendaciones personalizadas\nbasadas en tus calificaciones.",
            font=("Arial", 12, "italic"),
            bg="#ADD8E6",
            fg="#555555"
        )
        
        # Botones de navegación
        self.buttons_frame = tk.Frame(self.content_frame, bg="#ADD8E6")
        self.buttons_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Botón para volver a la pantalla de calificación
        self.back_button = create_styled_button(
            self.buttons_frame,
            "Volver a Calificar",
            self.controller.show_movie_rating_view
        )
        self.back_button.pack(side=tk.LEFT)
        
        # Botón para volver a la pantalla principal
        self.home_button = create_styled_button(
            self.buttons_frame,
            "Volver al Inicio",
            self.controller.show_main_view
        )
        self.home_button.pack(side=tk.RIGHT)
    
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Obtener recomendaciones del controlador
        recommendations = self.controller.get_recommendations()
        
        # Limpiar la lista
        self.recommendations_listbox.delete(0, tk.END)
        
        if recommendations:
            # Mostrar las recomendaciones
            for i, movie in enumerate(recommendations, 1):
                self.recommendations_listbox.insert(tk.END, f"{i}. {movie}")
            
            # Ocultar el mensaje de no recomendaciones
            self.no_recommendations_label.pack_forget()
            # Mostrar la lista
            self.recommendations_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        else:
            # Ocultar la lista
            self.recommendations_listbox.pack_forget()
            # Mostrar mensaje de no recomendaciones
            self.no_recommendations_label.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    def hide(self):
        self.frame.pack_forget()


