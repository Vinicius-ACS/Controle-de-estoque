from app.models import Product
from app.repository import ProductRepository, MovementRepository
from app.validators import validate_product_data, validate_movement


class ProductService:
    def __init__(self) -> None:
        self.product_repo = ProductRepository()
        self.movement_repo = MovementRepository()

    def create_product(self, name: str, category: str, price: float, quantity: int, min_stock: int) -> list[str]:
        errors = validate_product_data(name, category, price, quantity, min_stock)
        if errors:
            return errors

        product = Product(
            id=None,
            name=name.strip(),
            category=category.strip(),
            price=price,
            quantity=quantity,
            min_stock=min_stock,
        )
        self.product_repo.create(product)
        return []

    def update_product(self, product_id: int, name: str, category: str, price: float, quantity: int, min_stock: int) -> list[str]:
        errors = validate_product_data(name, category, price, quantity, min_stock)
        if errors:
            return errors

        product = Product(
            id=product_id,
            name=name.strip(),
            category=category.strip(),
            price=price,
            quantity=quantity,
            min_stock=min_stock,
        )
        self.product_repo.update(product)
        return []

    def add_stock(self, product_id: int, quantity: int) -> list[str]:
        errors = validate_movement(quantity)
        if errors:
            return errors

        product = self.product_repo.get_by_id(product_id)
        if product is None:
            return ["Produto não encontrado."]

        new_quantity = product.quantity + quantity
        self.product_repo.update_quantity(product_id, new_quantity)
        self.movement_repo.create(product_id, "entrada", quantity)
        return []

    def remove_stock(self, product_id: int, quantity: int) -> list[str]:
        errors = validate_movement(quantity)
        if errors:
            return errors

        product = self.product_repo.get_by_id(product_id)
        if product is None:
            return ["Produto não encontrado."]

        if quantity > product.quantity:
            return ["Quantidade de saída maior que o estoque disponível."]

        new_quantity = product.quantity - quantity
        self.product_repo.update_quantity(product_id, new_quantity)
        self.movement_repo.create(product_id, "saida", quantity)
        return []