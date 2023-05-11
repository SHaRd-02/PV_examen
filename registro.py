# Importando librerias necesarias
import tkinter as tk
import ttkbootstrap as ttk
import mariadb
from tkinter import messagebox

# Clase para registar los vehiculos


class Vehiculo:
    def __init__(self, registro):
        # Creando y configurando ventana con un contructor
        self.registro = registro
        self.registro.title("Registar Vehiculo")
        self.registro.geometry("1480x600")
        self.registro.resizable(False, False)

        # Combo box para elegir los años
        years = []
        for year in range(1990, 2024):
            years.append(year)
        year_var = tk.StringVar()
        # Opciones para el combo box para el color
        colores = ["Blanco", "Negro", "Gris",
                   "Rojo", "Azul", "Verde", "Amarillo"]
        color_var = tk.StringVar()
        # Opciones para el radiobutton para seleccionar el tipo de vehiculo
        tipo_var = tk.StringVar()
        tipos = ["SUV", "Hatchback", "Crossover",
                 "Convertible", "Sedan", "Sport", "Minivan", "Pickup"]

        # Labels de los datos a registrar
        frame_registro = ttk.LabelFrame(
            master=self.registro, text="Registrando Vehiculo")
        frame_registro.grid(row=0, column=0, rowspan=11)
        ttk.Label(master=frame_registro, text="Marca: ").grid(
            row=0, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="Modelo: ").grid(
            row=1, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="Año: ").grid(
            row=2, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="No. Serie: ").grid(
            row=3, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="Color: ").grid(
            row=4, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="Tipo: ").grid(
            row=5, column=0, columnspan=1)
        ttk.Label(master=frame_registro, text="Foto: ").grid(
            row=6, column=0, columnspan=1)
        self.mensaje = ttk.Label(
            master=frame_registro, text="", foreground="green")
        self.mensaje.grid(row=10, columnspan=2)

        # Entrys de los datos a registrar
        self.marca = ttk.Entry(master=frame_registro)
        self.marca.grid(row=0, column=1, pady=5, padx=5)
        self.marca.focus()

        self.modelo = ttk.Entry(master=frame_registro)
        self.modelo.grid(row=1, column=1, pady=5, padx=5)

        self.ano = ttk.Combobox(master=frame_registro,
                                textvariable=year_var, values=years)
        self.ano.grid(row=2, column=1, pady=5, padx=5)

        self.no_serie = ttk.Entry(master=frame_registro)
        self.no_serie.grid(row=3, column=1, pady=5, padx=5)

        self.color = ttk.Combobox(
            master=frame_registro, values=colores, textvariable=color_var)
        self.color.grid(row=4, column=1, pady=5, padx=5)

        self.tipo = ttk.Combobox(
            master=frame_registro, values=tipos, textvariable=tipo_var)
        self.tipo.grid(row=5, column=1, pady=5, padx=5)

        ttk.Button(master=frame_registro, text="Seleccionar foto",
                   command="").grid(row=6, column=1, pady=5, padx=5)

        # Botones para editar, guardar, buscar y eliminar
        self.buton_reg = ttk.Button(master=frame_registro, text="Registrar Vehiculo",
                                    command=self.agregarRegistro)
        self.buton_reg.grid(row=7, columnspan=2, pady=5, padx=5)

        self.buton_edit = ttk.Button(master=frame_registro, text="Editar Vehiculo",
                                     command=self.editarRegistro)
        self.buton_edit.grid(row=8, columnspan=2, pady=5, padx=5)
        self.buton_edit["state"] = "disabled"

        self.buton_delete = ttk.Button(master=frame_registro, text="Borrar Vehiculo",
                                       command=self.borrarRegistro)
        self.buton_delete.grid(row=9, columnspan=2, pady=5, padx=5)
        self.buton_delete["state"] = "disabled"

        # Boton buscar, labels y entrys para buscar por marca y no de serie
        self.buton_buscar = ttk.Button(
            master=self.registro, text=f"Buscar", command=self.ventanaBuscar)
        self.buton_buscar.grid(row=0, column=1, columnspan=1, padx=10, pady=5)
        # ttk.Label(master=self.registro, )

        # Treeview para desplegar los vehiculos registrados
        columns = ('marca', 'modelo', 'año', 'serie', 'color', 'tipo', 'foto')

        self.tabla_vehiculos = ttk.Treeview(self.registro, columns=columns)
        self.tabla_vehiculos.grid(
            row=1, column=2, columnspan=7, padx=5, pady=5)

        self.tabla_vehiculos.bind("<Double-Button-1>", self.doubleClick)

        self.tabla_vehiculos.heading("#0", text="Marca:", anchor="w")
        self.tabla_vehiculos.heading("#1", text="Modelo:", anchor="w")
        self.tabla_vehiculos.heading("#2", text="Año:", anchor="w")
        self.tabla_vehiculos.heading("#3", text="No. Serie:", anchor="w")
        self.tabla_vehiculos.heading("#4", text="Color:", anchor="w")
        self.tabla_vehiculos.heading("#5", text="Tipo:", anchor="w")
        self.tabla_vehiculos.heading("#6", text="Foto:", anchor="w")

        # Funciones

     # Funcion para consultar los vehiculos de la BDD
    def consultaVehiculo(self, query):
        try:
            conn = mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="agencia",
                autocommit=True
            )

            cur = conn.cursor()
            cur.execute(query)
            return cur
        except mariadb.Error as e:
            print('Error al conectarse a la base de datos', e)

    # Funcion para mostrar los datos de los vehiculos registrados
    def mostrarDatos(self, where=""):
        registros = self.tabla_vehiculos.get_children()
        for registro in registros:
            self.tabla_vehiculos.delete(registro)

        # cur = self.consultaVehiculo("SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos`")

        if len(where) > 0:
            cur = self.consultaVehiculo(
                "SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos`" + where)
        else:
            cur = self.consultaVehiculo(
                "SELECT `marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo` FROM `vehiculos`")

        for (marca, modelo, ano, serie, color, tipo) in cur:
            print(marca, modelo, ano, serie, color, tipo)
            self.tabla_vehiculos.insert(
                "", 0, text=marca, values=(modelo, ano, serie, color, tipo))

    # Funcion para agregar el registro a la BDD
    def agregarRegistro(self):

        if len(self.marca.get()) != 0 and len(self.modelo.get()) != 0 and len(self.ano.get()) != 0 and len(self.no_serie.get()) != 0 and len(self.color.get()) != 0 and len(self.tipo.get()) != 0:
            query = f"INSERT INTO `vehiculos`(`marca`, `modelo`, `año`, `numero de serie`, `color`, `Tipo`) VALUES ('{self.marca.get()}','{self.modelo.get()}','{self.ano.get()}','{self.no_serie.get()}','{self.color.get()}','{self.tipo.get()}');"
            self.consultaVehiculo(query)
            self.mensaje['text'] = f"El vehiculo marca {self.marca.get()}, \nmodelo {self.modelo.get()} se ha agregado \nexitosamente"
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            self.tipo.delete(0, tk.END)

            self.marca.focus()
            self.mostrarDatos()
        else:
            self.mensaje['text'] = "**Ningun dato debe de estar vacio, \nasegurate que todos los \ndatos esten completos"
            self.mensaje['foreground'] = "red"

    # Funcion para editar el registro a la BDD
    def editarRegistro(self):

        if len(self.marca.get()) != 0 and len(self.modelo.get()) != 0 and len(self.ano.get()) != 0 and len(self.no_serie.get()) != 0 and len(self.color.get()) != 0 and len(self.tipo.get()) != 0:
            query = f"UPDATE `vehiculos` SET `marca`='{self.marca.get()}',`modelo`='{self.modelo.get()}',`año`='{self.ano.get()}',`numero de serie`='{self.no_serie.get()}',`color`='{self.color.get()}',`Tipo`='{self.tipo.get()}' WHERE `numero de serie`={self.no_serieViejo}"
            self.consultaVehiculo(query)
            self.mensaje['text'] = f"El vehiculo marca {self.marca.get()}, \nmodelo {self.modelo.get()} se ha actulizado \nexitosamente"
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            self.tipo.delete(0, tk.END)

            self.marca.focus()
            self.mostrarDatos()
            self.buton_reg["state"] = "normal"
            self.buton_edit["state"] = "disable"
            self.buton_delete["state"] = "disable"
        else:
            self.mensaje['text'] = "**Ningun dato debe de estar vacio, \nasegurate que todos los \ndatos esten completos"
            self.mensaje['foreground'] = "red"

    # Funcion para borrar registro de la BDD
    def borrarRegistro(self):
        if messagebox.askyesno(message="Seguro de borrar el registro?",
                               title=f"Eliminar Vehiculo: {self.marca.get()}, {self.modelo.get()}") == True:
            query = f"DELETE FROM `vehiculos` WHERE `numero de serie`= '{self.no_serieViejo}'"
            self.consultaVehiculo(query)
            self.mensaje['text'] = f"El vehiculo {self.marca.get()}, {self.modelo.get()} \nse ha elimindao\nexitosamente"
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            self.tipo.delete(0, tk.END)
            self.marca.focus()
            self.mostrarDatos()
            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)
            self.ano.delete(0, tk.END)
            self.no_serie.delete(0, tk.END)
            self.color.delete(0, tk.END)
            self.tipo.delete(0, tk.END)

            self.buton_reg["state"] = "normal"
            self.buton_edit["state"] = "disable"
            self.buton_delete["state"] = "disable"
    # Funcion para hacer doble click en la tabla

    def doubleClick(self, event):
        self.no_serieViejo = str(
            self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][2])
        self.marca.delete(0, tk.END)
        self.modelo.delete(0, tk.END)
        self.ano.delete(0, tk.END)
        self.no_serie.delete(0, tk.END)
        self.color.delete(0, tk.END)
        self.tipo.delete(0, tk.END)
        self.buton_reg["state"] = "disable"
        self.buton_edit["state"] = "normal"
        self.buton_delete["state"] = "normal"
        self.marca.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["text"]))
        self.modelo.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][0]))
        self.ano.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][1]))
        self.no_serie.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][2]))
        self.color.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][3]))
        self.tipo.insert(
            0, str(self.tabla_vehiculos.item(self.tabla_vehiculos.selection())["values"][4]))

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
            row=0, column=0, padx=5, pady=5)
        ttk.Label(master=frame_buscar, text="Buscar por numero de serie").grid(
            row=1, column=0, padx=5, pady=5)

        # Creando los entrys para los campos de busqueda
        self.buscarMarca = ttk.Entry(master=frame_buscar)
        self.buscarMarca.grid(row=0, column=1, padx=5, pady=5)
        self.buscarNo_serie = ttk.Entry(master=frame_buscar)
        self.buscarNo_serie.grid(row=1, column=1, padx=5, pady=5)

        # Creando boton buscar
        self.buscar_boton = ttk.Button(
            master=frame_buscar, text="Buscar Vehiculo", command=self.buscarRegistro)
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
    registro = ttk.Window(themename='darkly')
    aplicacion = Vehiculo(registro)
    aplicacion.mostrarDatos()
    registro.mainloop()
