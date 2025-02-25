import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageGrab
import random
import os

class Nota:
    def __init__(self, root, text="", color="#FFFF88", x=100, y=100, width=250, height=200):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.configure(bg=color)
        self.window.title("Nota Flotante (SuperNotas)")  # Título de la ventana
        
        # Asignar ícono
        icon_path = "SuperNotas.ico"
        if os.path.exists(icon_path):
            self.window.iconbitmap(icon_path)

        # Crear un marco para los botones
        self.frame_botones = tk.Frame(self.window, bg=color)
        self.frame_botones.pack(fill="x")

        # Botón para nueva nota
        self.btn_nueva = tk.Button(self.frame_botones, text="Nueva nota", command=self.crear_nueva)
        self.btn_nueva.pack(side="left", padx=2)

        # Botón para cambiar color
        self.btn_color = tk.Button(self.frame_botones, text="Cambiar color", command=self.cambiar_color)
        self.btn_color.pack(side="left", padx=2)

        # Botón para cerrar
        self.btn_cerrar = tk.Button(self.frame_botones, text="Cerrar nota", command=self.cerrar)
        self.btn_cerrar.pack(side="right", padx=2)

        # Área de texto
        self.text_area = tk.Text(self.window, wrap="word", bg=color, font=("Arial", 12))
        self.text_area.insert("1.0", text)
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # Diccionario para almacenar referencias de imágenes
        self.imagenes = {}

        # Atajos de teclado
        self.window.bind("<Control-n>", lambda event: self.crear_nueva())  # Nueva nota
        self.window.bind("<Control-q>", lambda event: self.cerrar())  # Cerrar nota
        self.window.bind("<Control-c>", lambda event: self.cambiar_color())  # Cambiar color
        self.window.bind("<Control-v>", lambda event: self.pegar_imagen())  # Pegar imagen

    def crear_nueva(self):
        Nota(self.root)

    def cambiar_color(self):
        colores = ["#FF5733", "#33FF57", "#5733FF", "#FFD700", "#FF69B4", "#40E0D0", "#FF4500", "#ADFF2F"]
        nuevo_color = random.choice(colores)
        self.window.configure(bg=nuevo_color)
        self.text_area.configure(bg=nuevo_color)
        self.frame_botones.configure(bg=nuevo_color)

    def pegar_imagen(self):
        try:
            # Capturar imagen desde el portapapeles
            image = ImageGrab.grabclipboard()
            if image is None:
                print("⚠ No hay imagen en el portapapeles")
                return
            
            image.thumbnail((200, 200))  # Ajustar tamaño
            photo = ImageTk.PhotoImage(image)
            
            # Crear un ID único para la imagen
            image_id = f"img_{len(self.imagenes)}"
            self.imagenes[image_id] = photo  # Guardar referencia para evitar que se borre

            # Insertar imagen en el área de texto
            self.text_area.image_create("insert", image=self.imagenes[image_id])
            self.text_area.insert("insert", "\n")  # Agregar un salto de línea después de la imagen
            print("✅ Imagen pegada con éxito")
        except Exception as e:
            print("⚠ Error al pegar la imagen:", e)

    def cerrar(self):
        self.window.destroy()

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Ocultar la ventana principal
        self.root.bind("<Control-n>", lambda event: Nota(root))  # Atajo para nueva nota

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    Nota(root)  # Crear la primera nota al iniciar
    root.mainloop()
