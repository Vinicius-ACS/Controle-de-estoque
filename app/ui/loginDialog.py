import tkinter as tk
from tkinter import ttk, messagebox

from app.userService import UserService


class LoginDialog(tk.Toplevel):
    def __init__(self, parent, user_service: UserService):
        super().__init__(parent)
        self.user_service = user_service
        self.logged_user = None

        self.title("Entrar no Sistema")
        self.geometry("380x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ID do usuário").grid(row=0, column=0, sticky="w", pady=8)
        self.user_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.user_id_var, width=28).grid(row=0, column=1, pady=8)

        ttk.Label(frame, text="Senha").grid(row=1, column=0, sticky="w", pady=8)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=28, show="*").grid(row=1, column=1, pady=8)

        ttk.Button(frame, text="Entrar", command=self.login).grid(
            row=2, column=1, sticky="e", pady=20
        )

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