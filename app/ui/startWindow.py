import tkinter as tk
from tkinter import ttk

from app.service import ProductService
from app.userService import UserService
from app.ui.loginDialog import LoginDialog
from app.ui.registerDialog import RegisterDialog
from app.ui.mainWindow import MainWindow


class StartWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.user_service = UserService()
        self.product_service = ProductService()

        self.title("Sistema de Controle de Estoque")
        self.geometry("500x320")
        self.resizable(False, False)

        self.apply_styles()
        self.create_widgets()

    def apply_styles(self) -> None:
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Main.TButton", font=("Segoe UI", 10))

    def create_widgets(self) -> None:
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, padding=24)
        card.pack(expand=True)

        title = ttk.Label(
            card,
            text="📦 Controle de Estoque",
            style="Title.TLabel",
        )
        title.pack(pady=(0, 10))

        subtitle = ttk.Label(
            card,
            text="Gerencie seus produtos com segurança e praticidade.",
            style="Subtitle.TLabel",
            justify="center",
        )
        subtitle.pack(pady=(0, 6))

        helper = ttk.Label(
            card,
            text="Escolha uma opção para continuar no sistema.",
            style="Subtitle.TLabel",
            justify="center",
        )
        helper.pack(pady=(0, 22))

        ttk.Button(
            card,
            text="Entrar no sistema",
            command=self.open_login,
            width=28,
            style="Main.TButton",
        ).pack(pady=8)

        ttk.Button(
            card,
            text="Cadastrar novo usuário",
            command=self.open_register,
            width=28,
            style="Main.TButton",
        ).pack(pady=8)

    def open_register(self) -> None:
        dialog = RegisterDialog(self, self.user_service)
        self.wait_window(dialog)

    def open_login(self) -> None:
        dialog = LoginDialog(self, self.user_service)
        self.wait_window(dialog)

        if getattr(dialog, "logged_user", None) is not None:
            self.destroy()
            app = MainWindow(self.product_service, dialog.logged_user)
            app.mainloop()