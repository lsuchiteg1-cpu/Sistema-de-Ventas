# ==================================================================
# SISTEMA DE VENTAS
# ==================================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import datetime

# ======================================
# MODELO DE PRODUCTO 
# ======================================
# Fuente:
# Python Classes Documentation.
# https://docs.python.org/3/tutorial/classes.html
# ============================================================

class Producto:

    def __init__(self, id_producto, nombre, precio):

        self.id = id_producto
        self.nombre = nombre
        self.precio = precio


# =========================================
# NODO PARA LISTA ENLAZADA Y PILA
# =========================================

class Nodo:

    def __init__(self, producto):

        self.producto = producto
        self.siguiente = None

# ============================================================
# IMPLEMENTACIÓN DE LISTA ENLAZADA
# Basado en:
# Weiss, Mark Allen. Data Structures and Algorithm Analysis.
# Pearson Education, 2014.
# ============================================================
# =========================================
# LISTA ENLAZADA (CARRITO)
# =========================================

class ListaEnlazada:

    def __init__(self):

        self.cabeza = None

    def insertar(self, producto):

        nuevo_nodo = Nodo(producto)

        nuevo_nodo.siguiente = self.cabeza

        self.cabeza = nuevo_nodo
    
    def eliminar_cabeza(self):

        if self.cabeza is not None:

            self.cabeza = self.cabeza.siguiente

    def vaciar(self):

        self.cabeza = None

    def obtener_productos(self):

        productos = []

        actual = self.cabeza

        while actual:

            productos.append(actual.producto)

            actual = actual.siguiente

        return productos

# ============================================================
# IMPLEMENTACIÓN DE PILA (STACK)
# Basado en teoría de estructuras de datos.
# Fuente:
# Weiss, Mark Allen. Data Structures and Algorithm Analysis.
# ============================================================
# ==========================================================
# PILA PARA DESHACER
# ==========================================================

class PilaHistorial:

    def __init__(self):

        self.cima = None

    def push(self, producto):

        nuevo_nodo = Nodo(producto)

        nuevo_nodo.siguiente = self.cima

        self.cima = nuevo_nodo

    def pop(self):

        if self.cima is None:
            return None
        
        eliminado = self.cima.producto

        self.cima = self.cima.siguiente

        return eliminado
    
    def vaciar(self):

        self.cima = None
# ============================================================
# CONEXIÓN Y GESTIÓN DE BASE DE DATOS POSTGRESQL
# Fuente:
# PostgreSQL Global Development Group.
# PostgreSQL Documentation.
# https://www.postgresql.org/docs/
# ============================================================
# ================================================
# BASE DE DATOS POSTGRESQL
# ================================================

class DatabaseManager:

    def __init__(self):

        self.config = {

            "host": "localhost",
            "database": "ventas_db",
            "user": "postgres",
            "password": "seli1234"

        }

        self.inicializar_tablas()
# ============================================================
# TABLAS INTERACTIVAS UTILIZANDO TREEVIEW
# Fuente:
# Python Tutorial - Tkinter Treeview
# https://www.pythontutorial.net/tkinter/tkinter-treeview/
# ============================================================
    # ====================================
    # CREAR TABLAS
    # ===================================

    def inicializar_tablas(self):

        query_productos = """ 
        CREATE TABLE IF NOT EXISTS productos(
        
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        precio NUMERIC(10,2)

        );
        """

        query_ventas = """
        CREATE TABLE IF NOT EXISTS ventas(
        
        id SERIAL PRIMARY KEY,
        total NUMERIC(10,2)

        );
        """

        query_facturas = """
        CREATE TABLE IF NOT EXISTS facturas(
        
        id SERIAL PRIMARY KEY, 
        cliente VARCHAR(100),
        nit VARCHAR(50),
        total NUMERIC(10,2)

        );
        """

        self.ejecutar_dml(query_productos)
        self.ejecutar_dml(query_ventas)
        self.ejecutar_dml(query_facturas)

# ============================================================
# CONEXIÓN PYTHON - POSTGRESQL MEDIANTE PSYCOPG2
# Fuente:
# Psycopg Documentation.
# https://www.psycopg.org/docs/
# ============================================================
    # =====================================
    # EJECUTAR INSERT / UPDATE / DELETE
    # =====================================

    def ejecutar_dml(self, query, params=()):

        try:

            conexion = psycopg2.connect(**self.config)

            cursor = conexion.cursor()

            cursor.execute(query, params)

            conexion.commit()

            cursor.close()

            conexion.close()

            return True
        
        except Exception as e:

            messagebox.showerror(
                "Error Base de Datos",
                str(e)
            )

            return False
    
    # ======================================
    # OBTENER PRODUCTOS
    # ======================================

    def obtener_productos(self):

        try:

            conexion = psycopg2.connect(**self.config)

            cursor = conexion.cursor()

            cursor.execute("""
            SELECT id, nombre, precio
            FROM productos
            ORDER BY id
            """)

            productos = cursor.fetchall()

            cursor.close()
            conexion.close()

            return productos
        
        except Exception as e:

            print(e)

            return []
        
    # ==========================================
    # OBTENER HISTORIAL DE VENTAS
    # ==========================================

    def obtener_historial_ventas(self):

        try: 
            
            conexion = psycopg2.connect(**self.config)

            cursor = conexion.cursor()

            cursor.execute("""
            SELECT id, total
            FROM ventas
            ORDER BY id
            """)

            ventas = cursor.fetchall()

            cursor.close()
            conexion.close()

            return ventas
        
        except Exception as e:

            print(e)

            return []
        

# ============================================
# APLICACIÓN PRINCIPAL
# ============================================

class SistemaVentasApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Sistema de Ventas")
        self.geometry("800x600")
        self.configure(bg="#f0f2f5")

        # ====================================
        # SERVICIOS
        # ====================================

        self.db = DatabaseManager()

        self.carrito = ListaEnlazada()

        self.historial_pila = PilaHistorial()

        # ======================================
        # CONTENEDOR PRINCIPAL
        # ======================================

        self.contenedor = tk.Frame(
            self,
            bg="#f0f2f5"
        )

        self.contenedor.pack(
            fill="both",
            expand=True
        )

        self.pantallas = {}
# ============================================================
# INTERFAZ GRÁFICA DESARROLLADA CON TKINTER
# Fuente:
# Python Software Foundation. Tkinter Documentation.
# https://docs.python.org/3/library/tkinter.html
# ============================================================
        # ================================
        # PANTALLAS
        # ================================

        for PantallaClase in (

            MenuInicio,
            PantallaVentas,
            PantallaInventario,
            PantallaReportes

        ):
            nombre = PantallaClase.__name__

            pantalla = PantallaClase(
                self.contenedor,
                self
            )

            self.pantallas[nombre] = pantalla

            pantalla.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.contenedor.rowconfigure(0, weight=1)
        self.contenedor.columnconfigure(0, weight=1)

        self.mostrar_pantalla("MenuInicio")

    # =====================================
    # CAMBIAR PANTALLA
    # =====================================

    def mostrar_pantalla(self, nombre):

        pantalla = self.pantallas[nombre]

        if nombre == "PantallaInventario":
            pantalla.actualizar_tabla()

        elif nombre == "PantallaReportes":
            pantalla.actualizar_reportes()

        elif nombre == "PantallaVentas":
            pantalla.cargar_tabla_productos()

        pantalla.tkraise()


# ======================================================
# MENU PRINCIPAL
# ======================================================

class MenuInicio(tk.Frame):

    def __init__(self, parent, controlador):

        super().__init__(parent, bg="#f0f2f5")

        titulo = tk.Label(

            self,
            text="PUNTO DE VENTA",
            font=("Arial", 24, "bold"),
            bg="#f0f2f5",
            fg="#1a73e8"

        )

        titulo.pack(pady=40)

        frame_botones = tk.Frame(
            self,
            bg="#f0f2f5"
        )

        frame_botones.pack(pady=20)

        estilo_btn = {

            "font": ("Arial", 12, "bold"),
            "width": 20,
            "height": 2,
            "fg": "white",
            "bd": 0

        }

        # BOTON VENTAS

        tk.Button(

            frame_botones,
            text="🛒 VENTAS",
            bg="#31a853",
            command=lambda:
            controlador.mostrar_pantalla(
                "PantallaVentas"
            ),
            **estilo_btn
        ).grid(row=0, column=0, padx=10, pady=10)

        # BOTON INVENTARIO

        tk.Button(

            frame_botones,
            text="📦 INVENTARIO",
            bg="#fbbc05",
            command=lambda:
            controlador.mostrar_pantalla(
                "PantallaInventario"
            ),
            **estilo_btn
        ).grid(row=0, column=1, padx=10, pady=10)

        # BOTON DE REPORTES

        tk.Button(

            frame_botones,
            text="📊 REPORTES",
            bg="#1a73e8",
            command=lambda:
            controlador.mostrar_pantalla(
                "PantallaReportes"
            ),
            **estilo_btn
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=10,
            pady=10
        )


# ============================================
# PANTALLA VENTAS
# ============================================

class PantallaVentas(tk.Frame):

    def __init__(self, parent, controlador):

        super().__init__(parent, bg="white")

        self.controlador = controlador

        self.total_venta = 0

        # =======================================
        # BARRA SUPERIOR
        # =======================================

        barra = tk.Frame(
            self,
            bg="#34a853",
            height=50
        )

        barra.pack(fill="x")

        tk.Button(

            barra,
            text="⬅ MENÚ",
            bg="#24733a",
            fg="white",
            command=lambda:
            controlador.mostrar_pantalla(
                "MenuInicio"
            )
        ).pack(side="left", padx=10, pady=10)

        # ======================================
        # TABLA INVENTARIO
        # ======================================

        self.tabla_inventario = ttk.Treeview(

            self,
            columns=("ID", "Nombre", "Precio"),
            show="headings",
            height=5

        )

        self.tabla_inventario.heading(
            "ID",
            text="ID"
        )

        self.tabla_inventario.heading(
            "Nombre",
            text="Nombre"
        )

        self.tabla_inventario.heading(
            "Precio",
            text="Precio" 
        )

        self.tabla_inventario.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ====================================
        # BOTONES
        # ====================================

        tk.Button(

            self,
            text="Agregar al Carrito",
            bg="#2196F3",
            fg="white",
            command=self.agregar_carrito

        ).pack(pady=5)

        tk.Button(

            self,
            text="Deshacer Último",
            bg="#FF9800",
            fg="white",
            command=self.deshacer

        ).pack(pady=5)

        # ====================================================
        # TABLA CARRITO
        # ====================================================

        self.tabla_carrito = ttk.Treeview(

            self,
            columns=("ID", "Nombre", "Precio"),
            show="headings",
            height=5

        )

        self.tabla_carrito.heading(
            "ID",
            text="ID"
        )

        self.tabla_carrito.heading(
            "Nombre",
            text="Nombre"
        )

        self.tabla_carrito.heading(
            "Precio",
            text="Precio"
        )

        self.tabla_carrito.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ====================================================
        # TOTAL
        # ====================================================

        self.lbl_total = tk.Label(

            self,
            text="TOTAL: Q.0.00",
            font=("Arial", 14, "bold"),
            bg="white"

        )

        self.lbl_total.pack(pady=10)

        # ====================================================
        # COBRAR
        # ====================================================

        tk.Button(

            self,
            text="COBRAR",
            bg="#1a73e8",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            command=self.cobrar

        ).pack(pady=10)

    # ========================================================
    # CARGAR PRODUCTOS
    # ========================================================

    def cargar_tabla_productos(self):

        for item in self.tabla_inventario.get_children():

            self.tabla_inventario.delete(item)

        productos = (
            self.controlador.db.obtener_productos()
        )

        for producto in productos:

            self.tabla_inventario.insert(
                "",
                tk.END,
                values=producto
            )

    # ========================================================
    # AGREGAR AL CARRITO
    # ========================================================

    def agregar_carrito(self):

        seleccion = (
            self.tabla_inventario.selection()
        )

        if not seleccion:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un producto"
            )

            return

        valores = self.tabla_inventario.item(
            seleccion[0],
            "values"
        )

        producto = Producto(

            int(valores[0]),
            valores[1],
            float(valores[2])

        )

        self.controlador.carrito.insertar(
            producto
        )

        self.controlador.historial_pila.push(
            producto
        )

        self.tabla_carrito.insert(

            "",
            tk.END,
            values=(
                producto.id,
                producto.nombre,
                producto.precio
            )

        )

        self.total_venta += producto.precio

        self.lbl_total.config(
            text=f"TOTAL: Q.{self.total_venta:.2f}"
        )

    # ========================================================
    # DESHACER
    # ========================================================

    def deshacer(self):

        removido = (
            self.controlador.historial_pila.pop()
        )

        if removido:

            self.controlador.carrito.eliminar_cabeza()

            hijos = (
                self.tabla_carrito.get_children()
            )

            if hijos:

                self.tabla_carrito.delete(
                    hijos[-1]
                )

            self.total_venta -= removido.precio

            self.lbl_total.config(
                text=f"TOTAL: Q.{self.total_venta:.2f}"
            )
    
    # ========================================================
    # COBRAR
    # ========================================================
    # Basado en manejo de archivos en Python.
    # Fuente:
    # Python File Handling Documentation.
    # https://docs.python.org/3/tutorial/inputoutput.html
    # ============================================================

    def cobrar(self):

        if self.total_venta == 0:

            messagebox.showwarning(
                "Aviso",
                "Carrito vacío"
            )

            return
        
        # =========================================
        # DATOS DEL CLIENTE
        # =========================================

        cliente = simpledialog.askstring(
            "Cliente",
            "Ingrese el nombre del cliente:"
        )

        if not cliente:
            return
        
        nit = simpledialog.askstring(
            "NIT",
            "Ingrese NIT del cliente:"
        )

        if not nit:
            return
        
        try:

            # ================================
            # CONEXION A POSTGRESQL
            # ================================

            conexion = psycopg2.connect(
                **self.controlador.db.config
            )

            cursor = conexion.cursor()

            # ================================
            # INSERTAR FACTURA
            # ================================

            query = """
            INSERT INTO facturas(
                cliente,
                nit,
                total
            )
            VALUES(%s, %s, %s)
            RETURNING id
            """

            cursor.execute(

                query,

                (
                    cliente,
                    nit,
                    self.total_venta
                )
            )

            factura_id = cursor.fetchone()[0]

            conexion.commit()

            # ===================================
            # CREAR FACTURA TXT
            # ===================================

            nombre_archivo = (
                f"factura_{factura_id}.txt"
            )

            archivo = open(
                nombre_archivo,
                "w",
                encoding="utf-8"
            )

            archivo.write(
                "=====================================\n"
            )

            archivo.write(
                "           FACTURA DE VENTA\n"
            )

            archivo.write(
                "===================================\n\n"
            )

            archivo.write(
                f"FACTURA No: {factura_id}\n"
            )

            archivo.write(
                f"CLIENTE: {cliente}\n"
            )

            archivo.write(
                f"NIT: {nit}\n\n"
            )

            archivo.write(
                "PRODUCTOS\n"
            )

            archivo.write(
                "-------------------------------------\n"
            )

            # =============================================
            # RECORRER CARRITO
            # =============================================

            actual = self.controlador.carrito.cabeza

            while actual is not None:

                producto = actual.producto

                archivo.write(

                    f"{producto.nombre}"
                    f" - "
                    f"Q.{producto.precio:.2f}\n"

                )

                actual = actual.siguiente

            archivo.write(
                "------------------------------------\n"
            )

            archivo.write(
                f"TOTAL: Q.{self.total_venta:.2f}\n"
            )

            archivo.write(
                "\nGracias por su compra\n"
            )

            archivo.close()

            # =======================================
            # MENSAJE DE ÉXITO
            # =======================================

            messagebox.showinfo(

                "Venta realizada",

                f"Factura generada correctamente\n\n"
                f"Archivo: {nombre_archivo}"
            )

            # =========================================
            # LIMPIAR CARRITO
            # =========================================

            self.controlador.carrito.vaciar()

            self.controlador.historial_pila.vaciar()

            self.total_venta = 0

            self.lbl_total.config(
                text= "TOTAL: Q.0.00"
            )

            for item in self.tabla_carrito.get_children():
                self.tabla_carrito.delete(item)

            cursor.close()
            conexion.close()

        except Exception as e:
            
            messagebox.showerror(
                "Error",
                str(e)
            )

# ============================================================
# PANTALLA INVENTARIO
# ============================================================

class PantallaInventario(tk.Frame):

    def __init__(self, parent, controlador):

        super().__init__(parent, bg="white")

        self.controlador = controlador

        barra = tk.Frame(
            self,
            bg="#fbbc05",
            height=50
        )

        barra.pack(fill="x")

        tk.Button(

            barra,
            text="⬅ MENÚ",
            bg="#c69502",
            fg="white",
            command=lambda:
            controlador.mostrar_pantalla(
                "MenuInicio"
            )

        ).pack(side="left", padx=10, pady=10)

        # ====================================================
        # FORMULARIO
        # ====================================================

        frame_form = tk.Frame(
            self,
            bg="white"
        )

        frame_form.pack(pady=10)

        tk.Label(
            frame_form,
            text="ID"
        ).grid(row=0, column=0)

        self.txt_id = tk.Entry(frame_form)

        self.txt_id.grid(row=0, column=1)

        tk.Label(
            frame_form,
            text="Nombre"
        ).grid(row=0, column=2)

        self.txt_nombre = tk.Entry(frame_form)

        self.txt_nombre.grid(row=0, column=3)

        tk.Label(
            frame_form,
            text="Precio"
        ).grid(row=0, column=4)

        self.txt_precio = tk.Entry(frame_form)

        self.txt_precio.grid(row=0, column=5)

        tk.Button(

            frame_form,
            text="Guardar",
            bg="#4CAF50",
            fg="white",
            command=self.guardar_producto

        ).grid(row=0, column=6, padx=10)

        # ====================================================
        # TABLA
        # ====================================================

        self.tabla = ttk.Treeview(

            self,
            columns=("ID", "Nombre", "Precio"),
            show="headings"

        )

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio")

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabla.bind(
            "<Double-1>",
            self.modificar_producto
        )

    # ========================================================
    # GUARDAR PRODUCTO
    # ========================================================

    def guardar_producto(self):

        try:

            query = """
            INSERT INTO productos(id, nombre, precio)
            VALUES(%s, %s, %s)
            """

            self.controlador.db.ejecutar_dml(

                query,

                (
                    int(self.txt_id.get()),
                    self.txt_nombre.get(),
                    float(self.txt_precio.get())
                )

            )

            self.actualizar_tabla()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # ACTUALIZAR TABLA
    # ========================================================

    def actualizar_tabla(self):

        for item in self.tabla.get_children():

            self.tabla.delete(item)

        productos = (
            self.controlador.db.obtener_productos()
        )

        for producto in productos:

            self.tabla.insert(
                "",
                tk.END,
                values=producto
            )

    # ========================================================
    # MODIFICAR PRODUCTO
    # ========================================================

    def modificar_producto(self, event):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        id_producto = int(valores[0])

        nuevo_nombre = simpledialog.askstring(

            "Modificar",
            "Nuevo nombre:",
            initialvalue=valores[1]

        )

        nuevo_precio = simpledialog.askfloat(

            "Modificar",
            "Nuevo precio:",
            initialvalue=float(valores[2])

        )

        if nuevo_nombre and nuevo_precio:

            query = """
            UPDATE productos
            SET nombre=%s,
                precio=%s
            WHERE id=%s
            """

            self.controlador.db.ejecutar_dml(

                query,

                (
                    nuevo_nombre,
                    nuevo_precio,
                    id_producto
                )

            )

            self.actualizar_tabla()


# ============================================================
# PANTALLA REPORTES
# ============================================================

class PantallaReportes(tk.Frame):

    def __init__(self, parent, controlador):

        super().__init__(parent, bg="white")

        self.controlador = controlador

        barra = tk.Frame(
            self,
            bg="#1a73e8",
            height=50
        )

        barra.pack(fill="x")

        tk.Button(

            barra,
            text="⬅ MENÚ",
            bg="#1152a5",
            fg="white",
            command=lambda:
            controlador.mostrar_pantalla(
                "MenuInicio"
            )

        ).pack(side="left", padx=10, pady=10)

        # ====================================================
        # TABLA REPORTES
        # ====================================================

        self.tabla = ttk.Treeview(

            self,
            columns=("ID", "TOTAL"),
            show="headings"

        )

        self.tabla.heading(
            "ID",
            text="Venta"
        )

        self.tabla.heading(
            "TOTAL",
            text="Total"
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.lbl_total = tk.Label(

            self,
            text="TOTAL ACUMULADO: Q.0.00",
            font=("Arial", 14, "bold"),
            bg="white"

        )

        self.lbl_total.pack(pady=10)

    # ========================================================
    # ACTUALIZAR REPORTES
    # ========================================================

    def actualizar_reportes(self):

        for item in self.tabla.get_children():

            self.tabla.delete(item)

        ventas = (
            self.controlador.db
            .obtener_historial_ventas()
        )

        total = 0

        for venta in ventas:

            self.tabla.insert(
                "",
                tk.END,
                values=venta
            )

            total += float(venta[1])

        self.lbl_total.config(
            text=f"TOTAL ACUMULADO: Q.{total:.2f}"
        )


# ============================================================
# EJECUTAR APP
# ============================================================

if __name__ == "__main__":

    app = SistemaVentasApp()

    app.mainloop()

# Bibliografía
# Python Software Foundation. (2026). Python Documentation. Recuperado de https://docs.python.org/3/
# PostgreSQL Global Development Group. (2026). PostgreSQL Documentation. Recuperado de https://www.postgresql.org/docs/
# Di Gregorio, F. (2026). Psycopg2 Documentation. Recuperado de https://www.psycopg.org/docs/
# Weiss, M. A. (2014). Data Structures and Algorithm Analysis in C++. Pearson Education.
# Python Tutorial. (2026). Tkinter Treeview. Recuperado de https://www.pythontutorial.net/tkinter/tkinter-treeview/