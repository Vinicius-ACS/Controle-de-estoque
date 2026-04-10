import tkinter as tk
from tkinter import ttk, messagebox

from app.userService import UserService


class RegisterDialog(tk.Toplevel):
    def __init__(self, parent, user_service: UserService):
        super().__init__(parent)
        self.user_service = user_service

        self.title("Cadastro de Usuário")
        self.geometry("470x360")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.apply_styles()
        self.create_widgets()

    def apply_styles(self) -> None:
        style = ttk.Style()
        style.configure("DialogTitle.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("DialogText.TLabel", font=("Segoe UI", 10))

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="📝 Novo cadastro", style="DialogTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        subtitle = ttk.Label(
            frame,
            text="Preencha os dados abaixo para criar seu acesso ao sistema.",
            style="DialogText.TLabel",
            wraplength=380,
            justify="left",
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ttk.Label(frame, text="Nome").grid(row=2, column=0, sticky="w", pady=6)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=self.name_var, width=32)
        name_entry.grid(row=2, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="ID do usuário").grid(row=3, column=0, sticky="w", pady=6)
        self.user_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.user_id_var, width=32).grid(
            row=3, column=1, pady=6, sticky="ew"
        )

        ttk.Label(frame, text="E-mail").grid(row=4, column=0, sticky="w", pady=6)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=32).grid(
            row=4, column=1, pady=6, sticky="ew"
        )

        ttk.Label(frame, text="Senha").grid(row=5, column=0, sticky="w", pady=6)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=32, show="*").grid(
            row=5, column=1, pady=6, sticky="ew"
        )

        frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Cadastrar usuário", command=self.register).grid(
            row=6, column=1, sticky="e", pady=(18, 0)
        )

        name_entry.focus()

    def register(self) -> None:
        errors = self.user_service.register_user(
            self.name_var.get(),
            self.user_id_var.get(),
            self.email_var.get(),
            self.password_var.get(),
        )

        if errors:
            messagebox.showerror("Erro de validação", "\n".join(errors))
            return

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
        self.destroy()