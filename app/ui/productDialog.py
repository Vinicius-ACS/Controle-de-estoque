import tkinter as tk
from tkinter import ttk, messagebox

from app.models import Product
from app.service import ProductService


class ProductDialog(tk.Toplevel):
    def __init__(self, parent, service: ProductService, product: Product | None = None):
        super().__init__(parent)
        self.service = service
        self.product = product

        self.title("Produto")
        self.geometry("420x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if self.product:
            self.fill_form()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=35).grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Categoria").grid(row=1, column=0, sticky="w", pady=4)
        self.category_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.category_var, width=35).grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Preço").grid(row=2, column=0, sticky="w", pady=4)
        self.price_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.price_var, width=35).grid(row=2, column=1, pady=4)

        ttk.Label(frame, text="Quantidade").grid(row=3, column=0, sticky="w", pady=4)
        self.quantity_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.quantity_var, width=35).grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Estoque mínimo").grid(row=4, column=0, sticky="w", pady=4)
        self.min_stock_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.min_stock_var, width=35).grid(row=4, column=1, pady=4)

        ttk.Button(frame, text="Salvar", command=self.save).grid(row=5, column=1, sticky="e", pady=16)

    def fill_form(self) -> None:
        self.name_var.set(self.product.name)
        self.category_var.set(self.product.category)
        self.price_var.set(str(self.product.price))
        self.quantity_var.set(str(self.product.quantity))
        self.min_stock_var.set(str(self.product.min_stock))

    def save(self) -> None:
        try:
            price = float(self.price_var.get())
            quantity = int(self.quantity_var.get())
            min_stock = int(self.min_stock_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Preço, quantidade e estoque mínimo devem ser numéricos.")
            return

        if self.product is None:
            errors = self.service.create_product(
                self.name_var.get(),
                self.category_var.get(),
                price,
                quantity,
                min_stock,
            )
        else:
            errors = self.service.update_product(
                self.product.id,
                self.name_var.get(),
                self.category_var.get(),
                price,
                quantity,
                min_stock,
            )

        if errors:
            messagebox.showerror("Erro de validação", "\n".join(errors))
            return

        messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
        self.destroy()