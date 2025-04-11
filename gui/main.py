
# Inicializa el AppController y lanza la interfaz.



# Ejemplo de flujo completo:
# 1- Usuario abre la app → main.py lanza AppController.

# 2- controller.py inicia la vista de bienvenida (WelcomeView).

# 3- Usuario hace clic en “Descúbrelo ahora” → cambia a RecommendationView.

# 4- Se cargan películas desde model.py → se muestran en pantalla.

# 5- En el futuro: se procesan en logic.py y se muestran recomendaciones personalizadas.




import tkinter as tk
from controller import FilmIAController


def main():
    root = tk.Tk()
    app = FilmIAController(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Este es el archivo principal que inicia la aplicación")
