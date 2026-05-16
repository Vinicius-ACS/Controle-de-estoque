import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from app.exchange_service import ExchangeService

from app.ui.movementDialog import MovementDialog
from app.ui.productDialog import ProductDialog


class MainWindow(tk.Tk):
    def __init__(self, service, logged_user) -> None:
        super().__init__()
        self.service = service
        self.product_repo = service.product_repo
        self.logged_user = logged_user
        self.exchange_queue: queue.Queue[str] = queue.Queue()
        self.exchange_loading = False

        self.title("Sistema de Controle de Estoque")
        self.geometry("1050x620")
        self.minsize(980, 560)
        self.configure(background="#F3F4F6")

        self.apply_styles()
        self.configure_ui()
        self.create_widgets()
        self.load_products()
        self.after(600, self.start_exchange_rate_load)

    def apply_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#F3F4F6")
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("HeaderTitle.TLabel", font=("Segoe UI", 20, "bold"), background="#FFFFFF", foreground="#111827")
        style.configure("HeaderText.TLabel", font=("Segoe UI", 10), background="#FFFFFF", foreground="#4B5563")
        style.configure("Exchange.TLabel", font=("Segoe UI", 10, "bold"), background="#FFFFFF", foreground="#047857")
        style.configure("Search.TLabel", font=("Segoe UI", 10, "bold"), background="#FFFFFF", foreground="#374151")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E5E7EB", foreground="#111827")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, fieldbackground="#FFFFFF")
        style.map("Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])

    def configure_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def create_widgets(self) -> None:
        header = ttk.Frame(self, padding=16, style="Card.TFrame")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 10))
        header.columnconfigure(1, weight=1)

        title = ttk.Label(header, text="📦 Controle de Estoque", style="HeaderTitle.TLabel")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(
            header,
            text="Gerencie produtos, entradas e saídas com praticidade.",
            style="HeaderText.TLabel",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        user_label = ttk.Label(
            header,
            text=f"👤 Usuário logado: {self.logged_user.name} | ID: {self.logged_user.user_id}",
            style="HeaderText.TLabel",
        )
        user_label.grid(row=2, column=0, sticky="w", pady=(6, 0))

        self.exchange_label = ttk.Label(
            header,
            text="💵 Dólar: carregando...",
            style="Exchange.TLabel",
        )
        self.exchange_label.grid(row=3, column=0, sticky="w", pady=(6, 0))

        search_box = ttk.Frame(header, style="Card.TFrame")
        search_box.grid(row=0, column=1, rowspan=4, sticky="e")
        search_box.columnconfigure(0, weight=1)

        ttk.Label(search_box, text="Buscar produto", style="Search.TLabel").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_box, textvariable=self.search_var, width=30)
        search_entry.grid(row=1, column=0, padx=(0, 8), pady=(4, 0), sticky="ew")
        search_entry.bind("<KeyRelease>", lambda _event: self.search_products())

        self.create_button(
            search_box,
            text="🔎 Pesquisar",
            command=self.search_products,
            background="#2563EB",
            row=1,
            column=1,
            sticky="ew",
        )

        table_frame = ttk.Frame(self, padding=(16, 0, 16, 12), style="App.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("id", "name", "category", "price", "quantity", "min_stock", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        headings = {
            "id": "ID",
            "name": "Produto",
            "category": "Categoria",
            "price": "Preço",
            "quantity": "Quantidade",
            "min_stock": "Estoque mínimo",
            "status": "Status",
        }

        for col, text in headings.items():
            self.tree.heading(col, text=text)

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=240)
        self.tree.column("category", width=170)
        self.tree.column("price", width=110, anchor="e")
        self.tree.column("quantity", width=110, anchor="center")
        self.tree.column("min_stock", width=130, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.tag_configure("odd", background="#F9FAFB")
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("low_stock", foreground="#DC2626")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        actions = ttk.Frame(self, padding=(16, 0, 16, 16), style="App.TFrame")
        actions.grid(row=2, column=0, sticky="ew")

        self.create_button(actions, "➕ Novo produto", self.add_product, "#16A34A").pack(side="left", padx=4)
        self.create_button(actions, "✏ Editar", self.edit_product, "#F59E0B", foreground="#111827").pack(side="left", padx=4)
        self.create_button(actions, "📥 Entrada", self.add_movement_in, "#0EA5E9").pack(side="left", padx=4)
        self.create_button(actions, "📤 Saída", self.add_movement_out, "#6366F1").pack(side="left", padx=4)
        self.create_button(actions, "🗑 Excluir", self.delete_product, "#DC2626").pack(side="left", padx=4)
        self.create_button(actions, "🔄 Atualizar", self.refresh_all, "#374151").pack(side="left", padx=4)

    def create_button(
        self,
        parent,
        text: str,
        command,
        background: str,
        foreground: str = "#FFFFFF",
        row: int | None = None,
        column: int | None = None,
        sticky: str | None = None,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=7,
        )
        if row is not None and column is not None:
            button.grid(row=row, column=column, sticky=sticky, pady=(4, 0))
        return button

    def refresh_all(self) -> None:
        self.load_products()
        self.start_exchange_rate_load()

    def start_exchange_rate_load(self) -> None:
        if self.exchange_loading:
            return

        self.exchange_loading = True
        self.clear_exchange_queue()
        self.exchange_label.config(text="💵 Dólar: carregando...")

        thread = threading.Thread(target=self.fetch_exchange_rate, daemon=True)
        thread.start()

        self.after(100, self.process_exchange_queue)
        self.after(12000, self.exchange_timeout)

    def clear_exchange_queue(self) -> None:
        while not self.exchange_queue.empty():
            try:
                self.exchange_queue.get_nowait()
            except queue.Empty:
                break

    def fetch_exchange_rate(self) -> None:
        try:
            data = ExchangeService().get_usd_brl_rate()
            text = f"💵 Dólar hoje: {self.format_money(data['bid'])}"

            if data.get("date"):
                text += f" • atualizado em {data['date']}"

        except Exception as error:
            print(f"Erro ao buscar dólar: {error}")
            text = "💵 Dólar: indisponível. Clique em Atualizar."

        self.exchange_queue.put(text)

    def process_exchange_queue(self) -> None:
        try:
            text = self.exchange_queue.get_nowait()
        except queue.Empty:
            if self.exchange_loading and self.winfo_exists():
                self.after(100, self.process_exchange_queue)
            return

        self.exchange_loading = False
        self.exchange_label.config(text=text)

    def exchange_timeout(self) -> None:
        if self.exchange_loading:
            self.exchange_loading = False
            self.exchange_label.config(text="💵 Dólar: indisponível. Clique em Atualizar.")

    def format_money(self, value: float) -> str:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def load_products(self) -> None:
        self.clear_table()
        products = self.product_repo.list_all()

        for index, product in enumerate(products):
            status = "Estoque baixo" if product.quantity <= product.min_stock else "OK"

            row_tags = []
            row_tags.append("even" if index % 2 == 0 else "odd")

            if product.quantity <= product.min_stock:
                row_tags.append("low_stock")

            self.tree.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    product.category,
                    f"R$ {product.price:.2f}",
                    product.quantity,
                    product.min_stock,
                    status,
                ),
                tags=tuple(row_tags),
            )

    def clear_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def search_products(self) -> None:
        term = self.search_var.get().strip()
        self.clear_table()
        products = self.product_repo.search_by_name(term) if term else self.product_repo.list_all()

        for index, product in enumerate(products):
            status = "Estoque baixo" if product.quantity <= product.min_stock else "OK"

            row_tags = []
            row_tags.append("even" if index % 2 == 0 else "odd")

            if product.quantity <= product.min_stock:
                row_tags.append("low_stock")

            self.tree.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    product.category,
                    f"R$ {product.price:.2f}",
                    product.quantity,
                    product.min_stock,
                    status,
                ),
                tags=tuple(row_tags),
            )

    def get_selected_product_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return None

        values = self.tree.item(selected[0], "values")
        return int(values[0])

    def add_product(self) -> None:
        dialog = ProductDialog(self, self.service)
        self.wait_window(dialog)
        self.load_products()

    def edit_product(self) -> None:
        product_id = self.get_selected_product_id()
        if product_id is None:
            return

        product = self.product_repo.get_by_id(product_id)
        if product is None:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        dialog = ProductDialog(self, self.service, product)
        self.wait_window(dialog)
        self.load_products()

    def add_movement_in(self) -> None:
        product_id = self.get_selected_product_id()
        if product_id is None:
            return

        dialog = MovementDialog(self, self.service, product_id, "entrada")
        self.wait_window(dialog)
        self.load_products()

    def add_movement_out(self) -> None:
        product_id = self.get_selected_product_id()
        if product_id is None:
            return

        dialog = MovementDialog(self, self.service, product_id, "saida")
        self.wait_window(dialog)
        self.load_products()

    def delete_product(self) -> None:
        product_id = self.get_selected_product_id()
        if product_id is None:
            return

        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir o produto?")
        if confirm:
            self.product_repo.delete(product_id)
            self.load_products()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
