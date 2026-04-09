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

        self.title("Acesso ao Sistema")
        self.geometry("420x250")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(
            frame,
            text="Controle de Estoque",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(10, 10))

        subtitle = ttk.Label(
            frame,
            text="Selecione uma opção para continuar",
            font=("Segoe UI", 10),
        )
        subtitle.pack(pady=(0, 20))

        ttk.Button(
            frame,
            text="Entrar",
            command=self.open_login,
            width=25,
        ).pack(pady=8)

        ttk.Button(
            frame,
            text="Cadastrar",
            command=self.open_register,
            width=25,
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