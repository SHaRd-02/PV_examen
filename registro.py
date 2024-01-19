"""
Nombre: Ricardo Hernandez
Grupo: 548
Materia: Programacion Visual
Profesor: Emmanuel Gomez
Fecha: 15/05/2023
Laboratorio
Practica
"""


# Importando librerias necesarias
import tkinter as tk
import ttkbootstrap as ttk
import mariadb
from tkinter import messagebox

# from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from io import BytesIO
from PIL import Image, ImageTk
import base64

# Clase para registar los vehiculos


class Vehiculo:
    def __init__(self, registro):
        # Creando y configurando ventana con un contructor
        self.registro = registro
        self.registro.title("Registar Vehiculo")
        self.registro.geometry("1480x950")
        self.registro.resizable(False, False)
        self.registro.config()

        # Combo box para elegir los años
        years = []
        for year in range(1990, 2024):
            years.append(year)
        year_var = tk.StringVar()
        # Opciones para el combo box para el color
        colores = ["Blanco", "Negro", "Gris", "Rojo", "Azul", "Verde", "Amarillo"]
        color_var = tk.StringVar()

        # Variable para foto
        self.foto = None

        # Labels de los datos a registrar

        # Frames para ingresar datos
        frame_registro = ttk.LabelFrame(
            master=self.registro, text="Registrando Vehiculo"
        )
        frame_registro.grid(column=0, rowspan=15)
        ttk.Label(master=frame_registro, text="Marca: ").grid(
            row=0,
            column=0,
            columnspan=1,
        )
        frame_2 = ttk.Frame(master=self.registro)
        frame_2.grid(column=0, rowspan=5)
        ttk.Label(master=frame_registro, text="Modelo: ").grid(
            row=1, column=0, columnspan=1
        )

        # Creando el menu
        self.menu_bar = ttk.Menu(master=self.registro)

        # Creando el menu archivo
        self.archivo_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.archivo_menu.add_command(label="Salir", command=self.registro.quit)

        # Creando el menu Opciones
        self.opciones_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.opciones_menu.add_command(
            label="Buscar Registro", command=self.ventanaBuscar
        )

        # Agregando los menus a la barra menu
        self.menu_bar.add_cascade(label="Archivo", menu=self.archivo_menu)
        self.menu_bar.add_cascade(label="Opciones", menu=self.opciones_menu)

        # Configurando el menu en la ventana principal
        self.registro.config(menu=self.menu_bar)

        ttk.Label(master=frame_registro, text="Año: ").grid(
            row=2, column=0, columnspan=1
        )
        ttk.Label(master=frame_registro, text="No. Serie: ").grid(
            row=3, column=0, columnspan=1
        )
        ttk.Label(master=frame_registro, text="Color: ").grid(
            row=4, column=0, columnspan=1
        )
        ttk.Label(master=frame_registro, text="Tipo: ").grid(
            row=5, column=0, columnspan=1
        )
        ttk.Label(master=frame_2, text="Foto: ").grid(
            row=0, column=0, columnspan=1, rowspan=1
        )
        self.mensaje = ttk.Label(master=frame_2, text="", foreground="green")
        self.mensaje.grid(row=17, columnspan=2)

        # Entrys de los datos a registrar
        self.marca = ttk.Entry(master=frame_registro)
        self.marca.grid(row=0, column=1, pady=5, padx=5)
        self.marca.focus()

        self.modelo = ttk.Entry(master=frame_registro)
        self.modelo.grid(row=1, column=1, pady=5, padx=5)

        self.ano = ttk.Combobox(
            master=frame_registro, textvariable=year_var, values=years
        )
        self.ano.grid(row=2, column=1, pady=5, padx=5)

        self.no_serie = ttk.Entry(master=frame_registro)
        self.no_serie.grid(row=3, column=1, pady=5, padx=5)

        self.color = ttk.Combobox(
            master=frame_registro, values=colores, textvariable=color_var
        )
        self.color.grid(row=4, column=1, pady=5, padx=5)

        # RadioButton 
        # self.tipo = ttk.Combobox(master=frame_registro, values=tipos, textvariable=tipo_var)
        self.tipos_var = tk.StringVar()
        # (SUV, Hatchback, Crossover, Convertible, Sedan, Sport, Minivan, Pickup)
        opciones = [
            "SUV",
            "Hatchback",
            "Crossover",
            "Convertible",
            "Sedan",
            "Sport",
            "Minivan",
            "Pickup",
        ]

        for opcion in opciones:
            self.tipo = ttk.Radiobutton(
                master=frame_registro,
                text=opcion,
                value=opcion,
                variable=self.tipos_var,
            )
            self.tipo.grid(column=1, pady=5, padx=5, rowspan=8)

        ttk.Button(
            master=frame_2, text="Seleccionar foto", command=self.select_photo
        ).grid(row=0, column=1, pady=5, padx=5, rowspan=1)

        # Botones para editar, guardar, buscar y eliminar
        self.buton_reg = ttk.Button(
            master=frame_2,
            text="Registrar Vehiculo",
            command=self.agregarRegistro,
        )
        self.buton_reg.grid(row=1, columnspan=2, pady=5, padx=5, rowspan=1)

        self.buton_edit = ttk.Button(
            master=frame_2, text="Editar Vehiculo", command=self.editarRegistro
        )
        self.buton_edit.grid(row=2, columnspan=2, pady=5, padx=5, rowspan=1)
        self.buton_edit["state"] = "disabled"

        self.buton_delete = ttk.Button(
            master=frame_2, text="Borrar Vehiculo", command=self.borrarRegistro
        )
        self.buton_delete.grid(row=3, columnspan=2, pady=5, padx=5, rowspan=1)
        self.buton_delete["state"] = "disabled"

        self.buton_foto = ttk.Button(
            master=frame_2, text="Ver Imagen", command=self.mostrarImagen
        )
        # self.buton_foto.grid(row=4, columnspan=2, rowspan=1, padx=5, pady=5)

        # Treeview para desplegar los vehiculos registrados
        columns = ("marca", "modelo", "año", "serie", "color", "tipo", "foto")

        self.tabla_vehiculos = ttk.Treeview(self.registro, columns=columns)
        self.tabla_vehiculos.grid(row=1, column=2, columnspan=7, padx=5, pady=5)

        self.tabla_vehiculos.bind("<Double-Button-1>", self.doubleClick)
        self.tabla_vehiculos.bind("<Escape>", self.escTabla)
        # self.registro.bind  ("<Double-Button-1>", self.escTabla)

        self.tabla_vehiculos.heading("#0", text="Marca:", anchor="w")
        self.tabla_vehiculos.heading("#1", text="Modelo:", anchor="w")
        self.tabla_vehiculos.heading("#2", text="Año:", anchor="w")
        self.tabla_vehiculos.heading("#3", text="No. Serie:", anchor="w")
        self.tabla_vehiculos.heading("#4", text="Color:", anchor="w")
        self.tabla_vehiculos.heading("#5", text="Tipo:", anchor="w")
        self.tabla_vehiculos.heading("#6", text="Foto:", anchor="w")

        # Label para desplegar imagen
        self.imagen_frame = ttk.LabelFrame(master=self.registro, text="Foto:")
        self.imagen_frame.grid(
            row=2, column=2, padx=10, pady=10, columnspan=2, sticky="w" + "e"
        )
        self.imagen_label = ttk.Label(master=self.imagen_frame, text="fotos", image="")

        self.imagen_label.grid(
            row=0, column=0, padx=10, pady=10, columnspan=2, sticky=("w", "e")
        )

        # Funciones

    # Funcion para que al presionar esc despues de hacer doble se borren los datos de las entradas y se rehabilite el boton de registrar

    def escTabla(self, event):
        self.marca.delete(0, tk.END)
        self.modelo.delete(0, tk.END)
        self.ano.delete(0, tk.END)
        self.no_serie.delete(0, tk.END)
        self.color.delete(0, tk.END)
        self.buton_reg["state"] = "normal"
        self.buton_edit["state"] = "disabled"
        self.buton_delete["state"] = "disabled"

    # Funcion para abrir la imagen y guardalar

    def select_photo(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/",
            title="Seleccionar foto",
            filetypes=(
                ("Archivos de imagen", "*.jpg;*.png"),
                ("Todos los archivos", "*.*"),
            ),
        )
        self.imagen_label["image"] = self.filename

    # Función para subir la foto a la base de datos
    def upload_photo(self, clave):
        try:
            # Establecer la conexión a la base de datos
            conn = mariadb.connect(
                user="root",
                password="",
                host="localhost",
                database="agencia",
            )

            # Leer la foto seleccionada en modo binario
            with open(self.filename, "rb") as file:
                photo_data = file.read()

            # Actualizar la foto en la base de datos
            cursor = conn.cursor()
            sql = "UPDATE `vehiculos` SET `foto`=%s WHERE `numero de serie`=%s"
            values = (photo_data, clave)
            cursor.execute(sql, values)
            conn.commit()

            # Cerrar la conexión y mostrar un mensaje de éxito
            cursor.close()
            conn.close()
            print("Foto actualizada correctamente en la base de datos.")

        except mariadb.Error as e:
            print("Error al actualizar la foto en la base de datos:", e)

    # Funcion para conectarse a la base de datos nuevamente e importar una imagen
    def connectDatabase(self):
        try:
            connection = mariadb.connect(
                user="root",
                password="",
                host="localhost",
                database="agencia",
            )
            print("Connected to the database")
            return connection
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    # Funcion para mostrar la imagen del vechiculo seleccionado
    def mostrarImagen(self):
        conection = self.connectDatabase()
        if conection is None:
            return
        try:
            cursor = conection.cursor()
            cursor.execute(
                f"SELECT `numero de serie`, `foto` FROM `vehiculos` WHERE `numero de serie` = {self.no_serieViejo}"
            )
            record = cursor.fetchone()

            if record is not None:
                id_, image_data = record
                image = Image.open(BytesIO(image_data))
                image = image.resize((700, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                # Insert the item into the Treeview with the image
                # item = self.tabla_vehiculos.insert("", tk.END, image=photo)
                self.tabla_vehiculos.Img = photo

                # Set the image attribute for the inserted item
                # self.tabla_vehiculos.set(item, "foto", photo)

                # Store reference to the photo in the Treeview widget
                self.tabla_vehiculos.photo = photo

                # Update the image displayed in the photo_label
                self.imagen_label["image"] = photo

        except mariadb.Error as e:
            print(f"Error retrieving image: {e}")

    # Funcion para consultar los vehiculos de la BDD
    def consultaVehiculo(self, query):
        try:
            conn = mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="agencia",
                autocommit=True,
            )

            cur = conn.cursor()
            cur.execute(query)
            return cur
        except mariadb.Error as e:
            print("Error al conectarse a la base de datos", e)

    # Funcion para mostrar los datos de los vehiculos registrados
    def mostrarDatos(self, where=""):
        registros = self.tabla_vehiculos.get_children()
        for registro in registros:
            self.tabla_vehiculos.delete(registro)

        # cur = self.consultaVehiculo("SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos`")

        if len(where) > 0:
            cur = self.consultaVehiculo(
                "SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos` "
                + where
            )
        else:
            cur = self.consultaVehiculo(
                "SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos` "
            )

        for marca, modelo, ano, serie, color, tipo in cur:
            self.tabla_vehiculos.insert(
                "", 0, text=marca, values=(modelo, ano, serie, color, tipo)
            )

    # Funcion para agregar el registro a la BDD
    def agregarRegistro(self):
        if (
            len(self.marca.get()) != 0
            and len(self.modelo.get()) != 0
            and len(self.ano.get()) != 0
            and len(self.no_serie.get()) != 0
            and len(self.color.get()) != 0
            and len(self.tipos_var.get()) != 0
        ):
            query = f"INSERT INTO `vehiculos`(`marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo`) VALUES ('{self.marca.get()}','{self.modelo.get()}','{self.ano.get()}','{self.no_serie.get()}','{self.color.get()}','{self.tipos_var.get()}');"
            self.consultaVehiculo(query)
            self.mensaje[
                "text"
            ] = f"El vehiculo marca {self.marca.get()}, \nmodelo {self.modelo.get()} se ha agregado \nexitosamente"

            self.upload_photo(self.no_serie.get())

            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            # self.tipo.delete(0, tk.END)

            self.marca.focus()
            self.mostrarDatos()
            # print(self.foto)
        else:
            self.mensaje[
                "text"
            ] = "**Ningun dato debe de estar vacio, \nasegurate que todos los \ndatos esten completos"
            self.mensaje["foreground"] = "red"

    # Funcion para editar el registro a la BDD
    def editarRegistro(self):
        if (
            len(self.marca.get()) != 0
            and len(self.modelo.get()) != 0
            and len(self.ano.get()) != 0
            and len(self.no_serie.get()) != 0
            and len(self.color.get()) != 0
            # and len(self.tipos_var.get()) != 0
        ):
            query = f"UPDATE `vehiculos` SET `marca`='{self.marca.get()}',`modelo`='{self.modelo.get()}',`año`='{self.ano.get()}',`numero de serie`='{self.no_serie.get()}',`color`='{self.color.get()}',`Tipo`='{self.tipos_var.get()}' WHERE `numero de serie`={self.no_serieViejo}"
            self.consultaVehiculo(query)
            self.mensaje[
                "text"
            ] = f"El vehiculo marca {self.marca.get()}, \nmodelo {self.modelo.get()} se ha actulizado \nexitosamente"
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            # self.tipo.delete(0, tk.END)

            self.marca.focus()
            self.mostrarDatos()
            self.upload_photo(self.no_serieViejo)
            self.buton_reg["state"] = "normal"
            self.buton_edit["state"] = "disable"
            self.buton_delete["state"] = "disable"
        else:
            self.mensaje[
                "text"
            ] = "**Ningun dato debe de estar vacio, \nasegurate que todos los \ndatos esten completos"
            self.mensaje["foreground"] = "red"

    # Funcion para borrar registro de la BDD
    def borrarRegistro(self):
        if (
            messagebox.askyesno(
                message="Seguro de borrar el registro?",
                title=f"Eliminar Vehiculo: {self.marca.get()}, {self.modelo.get()}",
            )
            == True
        ):
            query = f"DELETE FROM `vehiculos` WHERE `numero de serie`= '{self.no_serieViejo}'"
            self.consultaVehiculo(query)
            self.mensaje[
                "text"
            ] = f"El vehiculo {self.marca.get()}, {self.modelo.get()} \nse ha elimindao\nexitosamente"
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            # self.tipo.delete(0, tk.END)
            self.marca.focus()
            self.mostrarDatos()
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            # self.tipo.delete(0, tk.END)

            self.buton_reg["state"] = "normal"
            self.buton_edit["state"] = "disable"
            self.buton_delete["state"] = "disable"

    # Funcion para hacer doble click en la tabla

    def doubleClick(self, event):
        self.no_serieViejo = str(
            self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][2]
        )
        self.marca.delete(0, tk.END)
        self.modelo.delete(0, tk.END)
        self.ano.delete(0, tk.END)
        self.no_serie.delete(0, tk.END)
        self.color.delete(0, tk.END)
        # self.tipo.delete(0, tk.END)
        self.buton_reg["state"] = "disable"
        self.buton_edit["state"] = "normal"
        self.buton_delete["state"] = "normal"
        self.marca.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["text"])
        )
        self.modelo.insert(
            0,
            str(
                self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][0]
            ),
        )
        self.ano.insert(
            0,
            str(
                self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][1]
            ),
        )
        self.no_serie.insert(
            0,
            str(
                self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][2]
            ),
        )
        self.color.insert(
            0,
            str(
                self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][3]
            ),
        )

        self.mostrarImagen()
        # self.tipos_var.insert(0,str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][4]),)

    # Funcion para abrir una nueva ventana

    def ventanaBuscar(self):
        # Creando nueva ventana con un toplevel
        buscar_ventana = ttk.Toplevel()
        buscar_ventana.title("Buscar Registro")
        buscar_ventana.geometry("400x180")
        buscar_ventana.resizable(False, False)

        # Creando label frame para ingresar los datos de busqueda
        frame_buscar = ttk.LabelFrame(master=buscar_ventana, text="Buscar")
        frame_buscar.grid(row=0, column=0, rowspan=4, padx=5, pady=5)

        # Creando labels para los campos de busqueda
        ttk.Label(master=frame_buscar, text="Buscar por marca").grid(
            row=0, column=0, padx=5, pady=5
        )
        ttk.Label(master=frame_buscar, text="Buscar por numero de serie").grid(
            row=1, column=0, padx=5, pady=5
        )

        # Creando los entrys para los campos de busqueda
        self.buscarMarca = ttk.Entry(master=frame_buscar)
        self.buscarMarca.grid(row=0, column=1, padx=5, pady=5)
        self.buscarNo_serie = ttk.Entry(master=frame_buscar)
        self.buscarNo_serie.grid(row=1, column=1, padx=5, pady=5)

        # Creando boton buscar
        self.buscar_boton = ttk.Button(
            master=frame_buscar, text="Buscar Vehiculo", command=self.buscarRegistro
        )
        self.buscar_boton.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Funcion para buscar un registro

    def buscarRegistro(self):
        where = "where 1=1"
        if len(self.buscarMarca.get()) > 0:
            where = f" {where} and marca = '{self.buscarMarca.get()}'"
        if len(self.buscarNo_serie.get()) > 0:
            where = f" {where} and `numero de serie` = '{self.buscarNo_serie.get()}'"
        self.mostrarDatos(where)


if __name__ == "__main__":
    # Creando y configurando ventana con un contructor
    registro = ttk.Window(themename="darkly")
    aplicacion = Vehiculo(registro)
    aplicacion.mostrarDatos()
    registro.mainloop()
