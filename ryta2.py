import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime

class Product:
    def __init__(self, id, name, category, quantity, price, location, created_at=None):
        self.id = id or str(int(datetime.now().timestamp()*1000))
        self.name = name
        self.category = category
        self.quantity = int(quantity)
        self.price = float(str(price).replace(',', '.'))
        self.location = location
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def to_list(self):
        return [self.id, self.name, self.category, str(self.quantity), f"{self.price:.2f}", self.location, self.created_at]

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Manager")
        self.products = []
        self.filtered_products = []
        self.create_widgets()
        
    def create_widgets(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Відкрити...", command=self.load_csv)
        filemenu.add_command(label="Зберегти", command=self.save_csv)
        filemenu.add_command(label="Зберегти як...", command=lambda: self.save_csv(save_as=True))
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.root.config(menu=menubar)
        
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ["id", "name", "category", "quantity", "price", "location", "created_at"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda _col=col: self.sort_column(_col, False))
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Пошук:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_tree())
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        form_frame = tk.Frame(self.root, relief=tk.RIDGE, bd=2)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        self.entries = {}
        fields = ["id", "name", "category", "quantity", "price", "location"]
        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field.capitalize()).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.entries[field] = entry
        
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=0, column=2, rowspan=len(fields), padx=10)
        tk.Button(btn_frame, text="Додати", width=12, command=self.add_product).pack(pady=2)
        tk.Button(btn_frame, text="Оновити", width=12, command=self.update_product).pack(pady=2)
        tk.Button(btn_frame, text="Видалити", width=12, command=self.delete_product).pack(pady=2)
        tk.Button(btn_frame, text="Очистити форму", width=12, command=self.clear_form).pack(pady=2)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Готово")
        status = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set_status(self, msg):
        self.status_var.set(msg)
        
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.set_status("Форма очищена")
        
    def validate_form(self):
        try:
            name = self.entries["name"].get().strip()
            category = self.entries["category"].get().strip()
            quantity = int(self.entries["quantity"].get())
            price = float(self.entries["price"].get().replace(',', '.'))
            location = self.entries["location"].get().strip()
            if not name or not category:
                raise ValueError("Name і Category не можуть бути порожніми")
            if quantity < 0 or price < 0:
                raise ValueError("Quantity і Price ≥ 0")
            return {
                "id": self.entries["id"].get().strip() or None,
                "name": name,
                "category": category,
                "quantity": quantity,
                "price": price,
                "location": location
            }
        except Exception as e:
            self.set_status(f"Помилка: {e}")
            return None
        
    def add_product(self):
        data = self.validate_form()
        if not data:
            return
        if data["id"] and any(p.id == data["id"] for p in self.products):
            self.set_status("Помилка: id вже існує")
            return
        product = Product(**data)
        self.products.append(product)
        self.update_tree()
        self.clear_form()
        self.set_status(f"Додано продукт {product.name}")
        
    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status("Немає обраного продукту")
            return
        data = self.validate_form()
        if not data:
            return
        item_id = selected[0]
        prod = next((p for p in self.products if p.id == item_id), None)
        if prod:
            new_id = data["id"] or prod.id
            if new_id != prod.id and any(p.id == new_id for p in self.products):
                self.set_status("Помилка: id вже існує")
                return
            prod.id = new_id
            prod.name = data["name"]
            prod.category = data["category"]
            prod.quantity = data["quantity"]
            prod.price = data["price"]
            prod.location = data["location"]
            self.update_tree()
            self.clear_form()
            self.set_status(f"Оновлено продукт {prod.name}")
        
    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status("Немає обраного продукту")
            return
        if not messagebox.askyesno("Підтвердження", "Видалити обраний продукт?"):
            return
        item_id = selected[0]
        self.products = [p for p in self.products if p.id != item_id]
        self.update_tree()
        self.clear_form()
        self.set_status("Продукт видалено")
        
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        prod = next((p for p in self.products if p.id == item_id), None)
        if prod:
            for field in ["id", "name", "category", "quantity", "price", "location"]:
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, str(getattr(prod, field)))
        
    def update_tree(self):
        query = self.search_var.get().lower()
        self.filtered_products = [p for p in self.products if query in p.name.lower() or query in p.category.lower()]
        self.tree.delete(*self.tree.get_children())
        for p in self.filtered_products:
            self.tree.insert("", tk.END, iid=p.id, values=p.to_list())
            
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.products = []
                for row in reader:
                    p = Product(
                        id=row["id"],
                        name=row["name"],
                        category=row["category"],
                        quantity=int(row["quantity"]),
                        price=float(row["price"].replace(',', '.')),
                        location=row["location"],
                        created_at=row.get("created_at")
                    )
                    self.products.append(p)
                self.update_tree()
                self.clear_form()
                self.set_status(f"Завантажено {len(self.products)} продуктів")
        except Exception as e:
            self.set_status(f"Помилка завантаження: {e}")
        
    def save_csv(self, save_as=False):
        if save_as or not hasattr(self, "current_file") or not self.current_file:
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if not path:
                return
            self.current_file = path
        try:
            with open(self.current_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id","name","category","quantity","price","location","created_at"])
                for p in self.products:
                    writer.writerow(p.to_list())
            self.set_status(f"Збережено {len(self.products)} продуктів")
        except Exception as e:
            self.set_status(f"Помилка збереження: {e}")
            
    def sort_column(self, col, reverse):
        try:
            self.products.sort(key=lambda p: getattr(p, col), reverse=reverse)
            self.update_tree()
            self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        except Exception as e:
            self.set_status(f"Помилка сортування: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.geometry("900x600")
    root.mainloop()
