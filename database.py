import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                stock_minimo INTEGER NOT NULL DEFAULT 0,
                stock_actual INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha DATETIME NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        self.conn.commit()

    def agregar_producto(self, nombre, categoria, stock_minimo):
        self.cursor.execute("INSERT INTO productos (nombre, categoria, stock_minimo, stock_actual) VALUES (?, ?, ?, 0)", (nombre, categoria, stock_minimo))
        self.conn.commit()

    def registrar_movimiento(self, producto_id, tipo, cantidad):
        import datetime
        fecha = datetime.datetime.now()
        self.cursor.execute("INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)", (producto_id, tipo, cantidad, fecha))
        self.conn.commit()

        # Actualizar el stock actual
        if tipo == "entrada":
            self.cursor.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?", (cantidad, producto_id))
        elif tipo == "salida":
            self.cursor.execute("UPDATE productos SET stock_actual = stock_actual - ? WHERE id = ?", (cantidad, producto_id))
        self.conn.commit()

        self.conn.commit()

    def editar_producto(self, id, nombre, categoria):
        self.cursor.execute("UPDATE productos SET nombre = ?, categoria = ? WHERE id = ?", (nombre, categoria, id))
        self.conn.commit()

    def eliminar_producto(self, id):
        self.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        self.conn.commit()

    def obtener_productos(self):
        self.cursor.execute("SELECT id, nombre, categoria, stock_minimo, stock_actual FROM productos")
        productos = self.cursor.fetchall()
        return productos