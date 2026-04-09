from dataclasses import dataclass

@dataclass
class Product:
    id: int | None
    name: str
    category: str
    price: float
    quantity: int
    min_stock: int

@dataclass
class User:
    id: int | None
    name: str
    user_id: str
    email: str
    password: str