import tkinter as tk
from tkinter import messagebox, ttk

from app.userService import UserService


class RegisterDialog(tk.Toplevel):
    def __init__(self, parent, user_service: UserService):
        super().__init__(parent)
        self.user_service = user_service

        self.title("Cadastro de Usuário")
        self.geometry("490x390")
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

        title = ttk.Label(frame, text="📝 Novo cadastro", style="DialogTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        subtitle = ttk.Label(
            frame,
            text="Preencha os dados abaixo para criar seu acesso ao sistema.",
            style="DialogText.TLabel",
            wraplength=390,
            justify="left",
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ttk.Label(frame, text="Nome", style="DialogText.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=self.name_var, width=32)
        name_entry.grid(row=2, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="ID do usuário", style="DialogText.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        self.user_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.user_id_var, width=32).grid(row=3, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="E-mail", style="DialogText.TLabel").grid(row=4, column=0, sticky="w", pady=6)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=32).grid(row=4, column=1, pady=6, sticky="ew")

        ttk.Label(frame, text="Senha", style="DialogText.TLabel").grid(row=5, column=0, sticky="w", pady=6)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=32, show="*").grid(row=5, column=1, pady=6, sticky="ew")

        frame.columnconfigure(1, weight=1)

        buttons = ttk.Frame(frame, style="DialogCard.TFrame")
        buttons.grid(row=6, column=1, sticky="e", pady=(18, 0))

        self.create_button(buttons, "Cancelar", self.destroy, "#6B7280").pack(side="left", padx=(0, 8))
        self.create_button(buttons, "Cadastrar usuário", self.register, "#7C3AED").pack(side="left")

        name_entry.focus()

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
