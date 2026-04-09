import tkinter as tk
from tkinter import ttk, messagebox

from app.service import ProductService


class MovementDialog(tk.Toplevel):
    def __init__(self, parent, service: ProductService, product_id: int, movement_type: str):
        super().__init__(parent)
        self.service = service
        self.product_id = product_id
        self.movement_type = movement_type

        self.title(f"Registrar {movement_type}")
        self.geometry("320x160")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Quantidade").grid(row=0, column=0, sticky="w", pady=8)
        self.quantity_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.quantity_var, width=20).grid(row=0, column=1, pady=8)

        ttk.Button(frame, text="Salvar", command=self.save).grid(row=1, column=1, sticky="e", pady=16)

    def save(self) -> None:
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade válida.")
            return

        if self.movement_type == "entrada":
            errors = self.service.add_stock(self.product_id, quantity)
        else:
            errors = self.service.remove_stock(self.product_id, quantity)

        if errors:
            messagebox.showerror("Erro", "\n".join(errors))
            return

        messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso.")
        self.destroy()