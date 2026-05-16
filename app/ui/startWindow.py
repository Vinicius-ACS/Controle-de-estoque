import tkinter as tk
from tkinter import ttk

from app.service import ProductService
from app.ui.loginDialog import LoginDialog
from app.ui.mainWindow import MainWindow
from app.ui.registerDialog import RegisterDialog
from app.userService import UserService


class StartWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.user_service = UserService()
        self.product_service = ProductService()

        self.title("Sistema de Controle de Estoque")
        self.geometry("560x360")
        self.resizable(False, False)
        self.configure(background="#EEF2FF")

        self.apply_styles()
        self.create_widgets()

    def apply_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), background="#FFFFFF", foreground="#111827")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), background="#FFFFFF", foreground="#4B5563")

    def create_widgets(self) -> None:
        container = tk.Frame(self, bg="#EEF2FF")
        container.pack(fill="both", expand=True, padx=28, pady=28)

        card = ttk.Frame(container, padding=30, style="Card.TFrame")
        card.pack(fill="both", expand=True)

        title = ttk.Label(card, text="📦 Controle de Estoque", style="Title.TLabel")
        title.pack(pady=(4, 10))

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
        helper.pack(pady=(0, 24))

        self.create_main_button(
            card,
            text="🔐 Entrar no sistema",
            command=self.open_login,
            background="#2563EB",
        ).pack(pady=8)

        self.create_main_button(
            card,
            text="📝 Cadastrar novo usuário",
            command=self.open_register,
            background="#7C3AED",
        ).pack(pady=8)

    def create_main_button(self, parent, text: str, command, background: str) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=30,
            bg=background,
            fg="#FFFFFF",
            activebackground=background,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10,
        )

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
