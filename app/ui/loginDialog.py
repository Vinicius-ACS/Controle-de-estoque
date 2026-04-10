import tkinter as tk
from tkinter import ttk, messagebox

from app.userService import UserService


class LoginDialog(tk.Toplevel):
    def __init__(self, parent, user_service: UserService):
        super().__init__(parent)
        self.user_service = user_service
        self.logged_user = None

        self.title("Entrar no Sistema")
        self.geometry("420x260")
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

        title = ttk.Label(frame, text="🔐 Login", style="DialogTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        subtitle = ttk.Label(
            frame,
            text="Informe seu ID de usuário e sua senha para acessar o sistema.",
            style="DialogText.TLabel",
            wraplength=340,
            justify="left",
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ttk.Label(frame, text="ID do usuário").grid(row=2, column=0, sticky="w", pady=8)
        self.user_id_var = tk.StringVar()
        user_entry = ttk.Entry(frame, textvariable=self.user_id_var, width=30)
        user_entry.grid(row=2, column=1, pady=8, sticky="ew")

        ttk.Label(frame, text="Senha").grid(row=3, column=0, sticky="w", pady=8)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=self.password_var, width=30, show="*")
        password_entry.grid(row=3, column=1, pady=8, sticky="ew")

        frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Entrar", command=self.login).grid(
            row=4, column=1, sticky="e", pady=(18, 0)
        )

        user_entry.focus()

    def login(self) -> None:
        errors, user = self.user_service.login_user(
            self.user_id_var.get(),
            self.password_var.get(),
        )

        if errors:
            messagebox.showerror("Erro de login", "\n".join(errors))
            return

        self.logged_user = user
        messagebox.showinfo("Sucesso", f"Bem-vindo(a), {user.name}!")
        self.destroy()