
import tkinter as tk
from tkinter import ttk

def center_window(window):
    """Centra una ventana en la pantalla."""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def create_styled_button(parent, text, command):
    """Crea un botón estilizado con hover effect."""
    style = ttk.Style()
    style.configure(
        "Styled.TButton",
        font=("Arial", 12, "bold"),
        background="#3366CC",
        foreground="white",
        padding=10
    )
    
    # Configurar estilos para hover
    style.map(
        "Styled.TButton",
        background=[("active", "#254EDB")],
        relief=[("pressed", "sunken")]
    )
    
    button = ttk.Button(
        parent,
        text=text,
        command=command,
        style="Styled.TButton",
        cursor="hand2"
    )
    
    return button

def format_text(text, max_width=40):
    """Formatea texto para que no exceda un ancho máximo."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(' '.join(current_line + [word])) <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

