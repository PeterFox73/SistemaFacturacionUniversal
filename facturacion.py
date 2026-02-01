import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

class FacturacionTab:
    def __init__(self, notebook, db):
        self.frame = ttk.Frame(notebook)
        self.db = db
        notebook.add(self.frame, text="Facturación")
        self.setup_ui()
        self.cart = []

    def setup_ui(self):
        # Top Frame: Client Selection
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(top_frame, text="Cliente:").pack(side="left")
        self.client_combo = ttk.Combobox(top_frame, state="readonly", width=40)
        self.client_combo.pack(side="left", padx=5)
        self.refresh_clients()
        
        ttk.Button(top_frame, text="Refrescar", command=self.refresh_clients).pack(side="left")

        # Middle Frame: Product Selection
        middle_frame = ttk.Frame(self.frame)
        middle_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(middle_frame, text="Producto:").grid(row=0, column=0, padx=5)
        self.product_combo = ttk.Combobox(middle_frame, state="readonly", width=40)
        self.product_combo.grid(row=0, column=1, padx=5)
        self.refresh_products()
        
        ttk.Label(middle_frame, text="Cantidad:").grid(row=0, column=2, padx=5)
        self.qty_entry = ttk.Entry(middle_frame, width=10)
        self.qty_entry.insert(0, "1")
        self.qty_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(middle_frame, text="Agregar a Factura", command=self.add_to_cart).grid(row=0, column=4, padx=10)

        # Bottom Frame: Invoice Details (Cart)
        bottom_frame = ttk.Frame(self.frame)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Producto", "Precio", "Cantidad", "Subtotal")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)
        
        # Totals and Actions
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        self.total_label = ttk.Label(action_frame, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.total_label.pack(side="left")
        
        ttk.Button(action_frame, text="Generar Factura", command=self.generate_invoice).pack(side="right", padx=5)
        ttk.Button(action_frame, text="Limpiar", command=self.clear_cart).pack(side="right")

    def refresh_clients(self):
        clients = self.db.obtener_clientes()
        self.client_map = {f"{c[1]} ({c[2] or 'Particular'})": c[0] for c in clients}
        self.client_combo['values'] = list(self.client_map.keys())

    def refresh_products(self):
        products = self.db.obtener_productos()
        # db.obtener_productos returns (id, nombre, categoria, precio, min, stock)
        # We need to map display string to (id, price, stock)
        self.product_map = {}
        display_values = []
        for p in products:
            # p[3] is price, p[5] is stock
            display_str = f"{p[1]} - ${p[3]} (Stock: {p[5]})"
            self.product_map[display_str] = {'id': p[0], 'price': p[3], 'stock': p[5], 'name': p[1]}
            display_values.append(display_str)
        self.product_combo['values'] = display_values

    def add_to_cart(self):
        product_selection = self.product_combo.get()
        qty_str = self.qty_entry.get()
        
        if not product_selection or not qty_str:
            return

        try:
            qty = int(qty_str)
            product_data = self.product_map[product_selection]
            
            if qty > product_data['stock']:
                messagebox.showerror("Error", "Stock insuficiente")
                return
            
            subtotal = qty * product_data['price']
            
            # Add to cart list
            self.cart.append({
                'id': product_data['id'],
                'name': product_data['name'],
                'price': product_data['price'],
                'qty': qty,
                'subtotal': subtotal
            })
            
            # Update Treeview
            self.tree.insert("", "end", values=(product_data['name'], f"${product_data['price']}", qty, f"${subtotal}"))
            self.update_total()
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")

    def update_total(self):
        total = sum(item['subtotal'] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def clear_cart(self):
        self.cart = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_total()

    def generate_invoice(self):
        client_selection = self.client_combo.get()
        if not client_selection:
            messagebox.showerror("Error", "Seleccione un cliente")
            return
            
        if not self.cart:
            messagebox.showerror("Error", "El carrito está vacío")
            return

        client_id = self.client_map[client_selection]
        total = sum(item['subtotal'] for item in self.cart)
        
        # Prepare items for DB: (product_id, qty, price)
        db_items = [(item['id'], item['qty'], item['price']) for item in self.cart]
        
        try:
            factura_id = self.db.crear_factura(client_id, total, db_items)
            messagebox.showinfo("Éxito", f"Factura #{factura_id} generada correctamente")
            self.clear_cart()
            self.refresh_products() # Refresh stock
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {e}")
