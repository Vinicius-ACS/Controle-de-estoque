import tkinter as tk
from tkinter import ttk, messagebox


class MovementDialog(tk.Toplevel):
    def __init__(self, parent, service, product_id: int, movement_type: str):
        super().__init__(parent)
        self.service = service
        self.product_id = product_id
        self.movement_type = movement_type

        self.title("Movimentação de Estoque")
        self.geometry("360x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        title_text = "📥 Registrar entrada" if self.movement_type == "entrada" else "📤 Registrar saída"
        ttk.Label(frame, text=title_text, font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        ttk.Label(frame, text="Quantidade").grid(row=1, column=0, sticky="w", pady=8)
        self.quantity_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.quantity_var, width=22).grid(row=1, column=1, pady=8, sticky="ew")

        frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Salvar", command=self.save).grid(row=2, column=1, sticky="e", pady=(20, 0))

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