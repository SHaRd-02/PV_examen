"""
Nombre: Ricardo Hernandez
Grupo: 548
Materia: Programacion Visual
Profesor: Emmanuel Gomez
Fecha: 15/05/2023
Laboratorio
Practica
"""


# importando las librerias necesarias
from tkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from registro import Vehiculo
import mariadb

# logo = Image.open("C:\\Users\\hallo\\Pictures\\logo_car.png")


class Inicio:
    # contructor para la fucnion principal
    def __init__(self, root):
        # definiendo la ventana principal
        self.root = root
        self.root.title("Sistema de Administracion vehicular")
        self.root.geometry("350x550")
        self.root.resizable(False, False)
        # --------------------------------------------------
        # Ventana de inicio

        # Importando logo de la compañia
        self.logo = Image.open("C:\\Users\\hallo\\Pictures\\logo_car.png")
        # Reajustando la imagen
        self.resized_logo = self.logo.resize((300, 200))
        self.tk_logo = ImageTk.PhotoImage(self.resized_logo)
        # Creando frame
        frame_inicio = ttk.Frame(master=self.root)
        # Creando label del logo
        logo_label = tk.Label(
            master=frame_inicio, text="logo", image=self.tk_logo, bg="white"
        )
        # Creando labels con la informacion de la compañia
        titulo_label = ttk.Label(
            master=frame_inicio, text="Nova Sports", font="Calibri 24 bold"
        )
        telefono_label = ttk.Label(master=frame_inicio, text="Telefono:")
        numero_telefono_label = ttk.Label(master=frame_inicio, text="(555) 123-4567")
        direccion_label = ttk.Label(master=frame_inicio, text="Direccion:")
        datos_direccion = ttk.Label(
            master=frame_inicio,
            text="1234 Avenida de las \nInnovaciones, Los Angeles, \nCA 90001, Estados Unidos.",
        )
        # Creando botones
        boton_1 = ttk.Button(
            master=frame_inicio, text="Registrar un auto", command=self.registro_ventana
        )

        boton_2 = ttk.Button(
            master=frame_inicio, text="Cerrar Programa", command=self.root.destroy
        )

        # Desplegando todo en grid
        frame_inicio.grid(row=0, column=0, columnspan=5)
        logo_label.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky=W + E)
        titulo_label.grid(row=2, column=1, columnspan=3, padx=10, pady=10)
        telefono_label.grid(row=3, column=1, columnspan=1, pady=10)
        numero_telefono_label.grid(row=3, column=3, columnspan=1, pady=10)
        direccion_label.grid(row=4, column=1, columnspan=1, pady=10, padx=10)
        datos_direccion.grid(row=4, column=3, columnspan=3, pady=10)
        boton_1.grid(row=5, column=1, columnspan=3, pady=10)
        boton_1.focus()
        boton_2.grid(row=6, column=1, columnspan=3, pady=10)

    def registro_ventana(self):
        second_window = ttk.Toplevel()
        second_window.title("Registrar Auto")
        second_window.geometry("800x800")
        self.objeto = Vehiculo(second_window)
        self.objeto.mostrarDatos()
        self.root.withdraw()


# constructor para el loop principal
if __name__ == "__main__":
    root = ttk.Window(themename="solar")
    aplicacion = Inicio(root)
    root.mainloop()
