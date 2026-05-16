import tkinter as tk
from tkinter import messagebox, ttk


class MovementDialog(tk.Toplevel):
    def __init__(self, parent, service, product_id: int, movement_type: str):
        super().__init__(parent)
        self.service = service
        self.product_id = product_id
        self.movement_type = movement_type

        self.title("Movimentação de Estoque")
        self.geometry("380x230")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(background="#F3F4F6")

        self.apply_styles()
        self.create_widgets()

    def apply_styles(self) -> None:
        style = ttk.Style()
        style.configure("DialogCard.TFrame", background="#FFFFFF")
        style.configure("DialogTitle.TLabel", font=("Segoe UI", 15, "bold"), background="#FFFFFF", foreground="#111827")
        style.configure("DialogText.TLabel", font=("Segoe UI", 10), background="#FFFFFF", foreground="#374151")

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=22, style="DialogCard.TFrame")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        title_text = "📥 Registrar entrada" if self.movement_type == "entrada" else "📤 Registrar saída"
        ttk.Label(frame, text=title_text, style="DialogTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        ttk.Label(frame, text="Quantidade", style="DialogText.TLabel").grid(row=1, column=0, sticky="w", pady=8)
        self.quantity_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.quantity_var, width=22).grid(row=1, column=1, pady=8, sticky="ew")

        frame.columnconfigure(1, weight=1)

        buttons = ttk.Frame(frame, style="DialogCard.TFrame")
        buttons.grid(row=2, column=1, sticky="e", pady=(22, 0))

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
