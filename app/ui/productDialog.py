import tkinter as tk
from tkinter import messagebox, ttk

from app.models import Product


class ProductDialog(tk.Toplevel):
    def __init__(self, parent, service, product: Product | None = None):
        super().__init__(parent)
        self.service = service
        self.product = product

        self.title("Produto")
        self.geometry("480x390")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(background="#F3F4F6")

        self.apply_styles()
        self.create_widgets()
        if self.product:
            self.fill_form()

    def apply_styles(self) -> None:
        style = ttk.Style()
        style.configure("DialogCard.TFrame", background="#FFFFFF")
        style.configure("DialogTitle.TLabel", font=("Segoe UI", 15, "bold"), background="#FFFFFF", foreground="#111827")
        style.configure("DialogText.TLabel", font=("Segoe UI", 10), background="#FFFFFF", foreground="#374151")

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=22, style="DialogCard.TFrame")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        title_text = "✏ Editar produto" if self.product else "➕ Novo produto"
        ttk.Label(frame, text=title_text, style="DialogTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )

        ttk.Label(frame, text="Nome", style="DialogText.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=34).grid(row=1, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="Categoria", style="DialogText.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.category_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.category_var, width=34).grid(row=2, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="Preço", style="DialogText.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        self.price_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.price_var, width=34).grid(row=3, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="Quantidade", style="DialogText.TLabel").grid(row=4, column=0, sticky="w", pady=6)
        self.quantity_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.quantity_var, width=34).grid(row=4, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="Estoque mínimo", style="DialogText.TLabel").grid(row=5, column=0, sticky="w", pady=6)
        self.min_stock_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.min_stock_var, width=34).grid(row=5, column=1, pady=6, sticky="ew")

        frame.columnconfigure(1, weight=1)

        buttons = ttk.Frame(frame, style="DialogCard.TFrame")
        buttons.grid(row=6, column=1, sticky="e", pady=(22, 0))

        self.create_button(buttons, "Cancelar", self.destroy, "#6B7280").pack(side="left", padx=(0, 8))
        self.create_button(buttons, "Salvar", self.save, "#16A34A").pack(side="left")

    def create_button(self, parent, text: str, command, background: str) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg="#FFFFFF",
            activebackground=background,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
        )

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
