import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        # Crear un notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña de Productos
        self.productos_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.productos_tab, text="Productos")
        self.setup_productos_tab()

        # Pestaña de Importar Inventario
        self.importar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.importar_tab, text="Importar Inventario")
        self.setup_importar_tab()

        # Pestaña de Movimientos
        self.movimientos_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.movimientos_tab, text="Movimientos")
        self.setup_movimientos_tab()

        # Pestaña de Reportes
        self.reportes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reportes_tab, text="Reportes")
        self.setup_reportes_tab()

    def setup_movimientos_tab(self):
        # Etiquetas y campos de entrada para la gestión de movimientos
        ttk.Label(self.movimientos_tab, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.producto_combo = ttk.Combobox(self.movimientos_tab, values=self.obtener_nombres_productos())
        self.producto_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.movimientos_tab, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_combo = ttk.Combobox(self.movimientos_tab, values=["entrada", "salida"])
        self.tipo_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.movimientos_tab, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5)
        self.cantidad_entry = ttk.Entry(self.movimientos_tab)
        self.cantidad_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botón para registrar el movimiento
        ttk.Button(self.movimientos_tab, text="Registrar Movimiento", command=self.registrar_movimiento).grid(row=3, column=0, padx=5, pady=5)

    def registrar_movimiento(self):
        producto_nombre = self.producto_combo.get()
        tipo = self.tipo_combo.get()
        cantidad = self.cantidad_entry.get()

        if producto_nombre and tipo and cantidad:
            try:
                cantidad = int(cantidad)
                producto_id = self.obtener_id_producto(producto_nombre)
                self.db.registrar_movimiento(producto_id, tipo, cantidad)
                self.actualizar_tabla_productos()
                messagebox.showinfo("Éxito", "Movimiento registrado correctamente")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def obtener_nombres_productos(self):
        productos = self.db.obtener_productos()
        nombres = [producto[1] for producto in productos]
        return nombres

    def obtener_id_producto(self, nombre):
        productos = self.db.obtener_productos()
        for producto in productos:
            if producto[1] == nombre:
                return producto[0]
        return None
    def setup_productos_tab(self):
        # Etiquetas y campos de entrada para la gestión de productos
        ttk.Label(self.productos_tab, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)

    def setup_reportes_tab(self):
        # Botones para generar reportes en Excel/CSV
        ttk.Button(self.reportes_tab, text="Generar Reporte en Excel", command=self.generar_reporte_excel).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.reportes_tab, text="Generar Reporte en CSV", command=self.generar_reporte_csv).grid(row=0, column=1, padx=5, pady=5)

    def generar_reporte_excel(self):
        # Implementar la lógica para generar el reporte en Excel
        pass

    def generar_reporte_csv(self):
        # Implementar la lógica para generar el reporte en CSV
        pass

    def setup_reportes_tab(self):
        # Botones para generar reportes en Excel/CSV
        ttk.Button(self.reportes_tab, text="Generar Reporte en Excel", command=self.generar_reporte_excel).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.reportes_tab, text="Generar Reporte en CSV", command=self.generar_reporte_csv).grid(row=0, column=1, padx=5, pady=5)

    def generar_reporte_excel(self):
        # Implementar la lógica para generar el reporte en Excel
        pass

    def generar_reporte_csv(self):
        # Implementar la lógica para generar el reporte en CSV
        pass

    def generar_reporte_excel(self):
        import pandas as pd
        from tkinter import filedialog

        productos = self.db.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Nombre", "Categoría"])

        filename = filedialog.asksaveasfilename(initialdir=".", title="Guardar Reporte en Excel", filetypes=(("Archivos Excel", "*.xlsx"),))
        if filename:
            try:
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", "Reporte en Excel generado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el reporte en Excel: {e}")

    def generar_reporte_csv(self):
        import pandas as pd
        from tkinter import filedialog

        productos = self.db.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Nombre", "Categoría"])

        filename = filedialog.asksaveasfilename(initialdir=".", title="Guardar Reporte en CSV", filetypes=(("Archivos CSV", "*.csv"),))
        if filename:
            try:
                df.to_csv(filename, index=False)
                messagebox.showinfo("Éxito", "Reporte en CSV generado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el reporte en CSV: {e}")

    def setup_importar_tab(self):
        # Botón para seleccionar el archivo CSV/Excel
        ttk.Button(self.importar_tab, text="Seleccionar Archivo", command=self.seleccionar_archivo).grid(row=0, column=0, padx=5, pady=5)

    def seleccionar_archivo(self):
        from tkinter import filedialog
        import pandas as pd

        filename = filedialog.askopenfilename(initialdir=".", title="Seleccionar Archivo", filetypes=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")))
        if filename:
            try:
                if filename.endswith(".csv"):
                    df = pd.read_csv(filename)
                else:
                    df = pd.read_excel(filename)

                # Procesar los datos del DataFrame
                for index, row in df.iterrows():
                    nombre = row["Nombre"]
                    categoria = row["Categoría"]
                    stock_minimo = row["Stock Mínimo"]
                    self.db.agregar_producto(nombre, categoria, stock_minimo)

                self.actualizar_tabla_productos()
                messagebox.showinfo("Éxito", "Inventario importado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar el inventario: {e}")
        self.nombre_entry = ttk.Entry(self.productos_tab)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.productos_tab, text="Categoría:").grid(row=1, column=0, padx=5, pady=5)
        self.categoria_combo = ttk.Combobox(self.productos_tab, values=["Electrónicos", "Ropa", "Alimentos", "Otros"])
        self.categoria_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.productos_tab, text="Stock Mínimo:").grid(row=2, column=0, padx=5, pady=5)
        self.stock_minimo_entry = ttk.Entry(self.productos_tab)
        self.stock_minimo_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botones para agregar, editar y eliminar productos
        ttk.Button(self.productos_tab, text="Agregar Producto", command=self.agregar_producto).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.productos_tab, text="Editar Producto", command=self.editar_producto).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.productos_tab, text="Eliminar Producto", command=self.eliminar_producto).grid(row=2, column=2, padx=5, pady=5)

        # Tabla para mostrar los productos
        self.productos_table = ttk.Treeview(self.productos_tab, columns=("Nombre", "Categoría", "Stock Mínimo", "Stock Actual"))
        self.productos_table.heading("#0", text="ID")
        self.productos_table.heading("Nombre", text="Nombre")
        self.productos_table.heading("Categoría", text="Categoría")
        self.productos_table.heading("Stock Mínimo", text="Stock Mínimo")
        self.productos_table.heading("Stock Actual", text="Stock Actual")
        self.productos_table.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.actualizar_tabla_productos()

    def agregar_producto(self):
        nombre = self.nombre_entry.get()
        categoria = self.categoria_combo.get()
        stock_minimo = self.stock_minimo_entry.get()
        if nombre and categoria and stock_minimo:
            try:
                stock_minimo = int(stock_minimo)
                self.db.agregar_producto(nombre, categoria, stock_minimo)
                self.actualizar_tabla_productos()
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                self.verificar_stock_minimo()
            except ValueError:
                messagebox.showerror("Error", "El stock mínimo debe ser un número entero")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def editar_producto(self):
        selected_item = self.productos_table.selection()
        if selected_item:
            id = selected_item[0]
            nombre = self.nombre_entry.get()
            categoria = self.categoria_combo.get()
            if nombre and categoria:
                self.db.editar_producto(id, nombre, categoria)
                self.actualizar_tabla_productos()
                messagebox.showinfo("Éxito", "Producto editado correctamente")
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para editar")

    def eliminar_producto(self):
        selected_item = self.productos_table.selection()
        if selected_item:
            id = selected_item[0]
            self.db.eliminar_producto(id)
            self.actualizar_tabla_productos()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar")

    def actualizar_tabla_productos(self):
        # Limpiar la tabla
        for item in self.productos_table.get_children():
            self.productos_table.delete(item)

        # Obtener los productos de la base de datos
        productos = self.db.obtener_productos()

        # Insertar los productos en la tabla
        for producto in productos:
            self.productos_table.insert("", "end", iid=producto[0], text=producto[0], values=(producto[1], producto[2], producto[3], producto[4]))

    def verificar_stock_minimo(self):
        productos = self.db.obtener_productos()
        for producto in productos:
            id = producto[0]
            nombre = producto[1]
            categoria = producto[2]
            stock_minimo = producto[3]
            stock_actual = producto[4]
            if stock_actual < stock_minimo:
                messagebox.showwarning("Alerta de Stock Mínimo", f"El producto {nombre} ({categoria}) ha alcanzado el stock mínimo")