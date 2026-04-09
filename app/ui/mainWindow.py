import tkinter as tk
from tkinter import ttk, messagebox

from app.ui.productDialog import ProductDialog
from app.ui.movementDialog import MovementDialog


class MainWindow(tk.Tk):
    def __init__(self, service) -> None:
        super().__init__()
        self.service = service
        self.product_repo = service.product_repo

        self.title("Controle de Estoque")
        self.geometry("950x560")
        self.minsize(900, 500)

        self.configure_ui()
        self.create_widgets()
        self.load_products()

    def configure_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def create_widgets(self) -> None:
        header = ttk.Frame(self, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        title = ttk.Label(header, text="Controle de Estoque", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, padx=12, sticky="ew")
        search_entry.bind("<KeyRelease>", lambda event: self.search_products())

        search_button = ttk.Button(header, text="Pesquisar", command=self.search_products)
        search_button.grid(row=0, column=2, padx=4)

        table_frame = ttk.Frame(self, padding=(12, 0, 12, 12))
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
        self.tree.column("name", width=220)
        self.tree.column("category", width=160)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("min_stock", width=120, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        actions = ttk.Frame(self, padding=(12, 0, 12, 12))
        actions.grid(row=2, column=0, sticky="ew")

        ttk.Button(actions, text="Novo produto", command=self.add_product).pack(side="left", padx=4)
        ttk.Button(actions, text="Editar", command=self.edit_product).pack(side="left", padx=4)
        ttk.Button(actions, text="Entrada", command=self.add_movement_in).pack(side="left", padx=4)
        ttk.Button(actions, text="Saída", command=self.add_movement_out).pack(side="left", padx=4)
        ttk.Button(actions, text="Excluir", command=self.delete_product).pack(side="left", padx=4)
        ttk.Button(actions, text="Atualizar", command=self.load_products).pack(side="left", padx=4)

    def load_products(self) -> None:
        self.clear_table()
        for product in self.product_repo.list_all():
            status = "Baixo" if product.quantity <= product.min_stock else "OK"
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
            )

    def clear_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def search_products(self) -> None:
        term = self.search_var.get().strip()
        self.clear_table()
        products = self.product_repo.search_by_name(term) if term else self.product_repo.list_all()

        for product in products:
            status = "Baixo" if product.quantity <= product.min_stock else "OK"
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