from dataclasses import dataclass

@dataclass
class Product:
    id: int | None
    name: str
    category: str
    price: float
    quantity: int
    min_stock: int