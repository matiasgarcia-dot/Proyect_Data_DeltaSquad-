import tkinter as tk
from gui.controller import FilmIAController


def main():
    root = tk.Tk()
    app = FilmIAController(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Este es el archivo principal que inicia la aplicación")
