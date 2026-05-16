import tkinter as tk
from tkinter import messagebox, ttk

from app.userService import UserService


class LoginDialog(tk.Toplevel):
    def __init__(self, parent, user_service: UserService):
        super().__init__(parent)
        self.user_service = user_service
        self.logged_user = None

        self.title("Entrar no Sistema")
        self.geometry("440x290")
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
        style.configure("DialogText.TLabel", font=("Segoe UI", 10), background="#FFFFFF", foreground="#4B5563")

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=22, style="DialogCard.TFrame")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        title = ttk.Label(frame, text="🔐 Login", style="DialogTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        subtitle = ttk.Label(
            frame,
            text="Informe seu ID de usuário e sua senha para acessar o sistema.",
            style="DialogText.TLabel",
            wraplength=350,
            justify="left",
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ttk.Label(frame, text="ID do usuário", style="DialogText.TLabel").grid(row=2, column=0, sticky="w", pady=8)
        self.user_id_var = tk.StringVar()
        user_entry = ttk.Entry(frame, textvariable=self.user_id_var, width=30)
        user_entry.grid(row=2, column=1, pady=8, sticky="ew")

        ttk.Label(frame, text="Senha", style="DialogText.TLabel").grid(row=3, column=0, sticky="w", pady=8)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=self.password_var, width=30, show="*")
        password_entry.grid(row=3, column=1, pady=8, sticky="ew")

        frame.columnconfigure(1, weight=1)

        buttons = ttk.Frame(frame, style="DialogCard.TFrame")
        buttons.grid(row=4, column=1, sticky="e", pady=(18, 0))

        self.create_button(buttons, "Cancelar", self.destroy, "#6B7280").pack(side="left", padx=(0, 8))
        self.create_button(buttons, "Entrar", self.login, "#2563EB").pack(side="left")

        user_entry.focus()

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
