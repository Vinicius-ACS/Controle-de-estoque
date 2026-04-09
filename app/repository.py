from app.database import get_connection
from app.models import Product

class ProductRepository:
    def create(self, product: Product) -> None:
        conn = get_connection()
        conn.execute(
            "INSERT INTO products (name, category, price, quantity, min_stock) VALUES (?, ?, ?, ?, ?)",
            (product.name, product.category, product.price, product.quantity, product.min_stock),
        )
        conn.commit()
        conn.close()
    
    def list_all(self) -> list[Product]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, name, category, price, quantity, min_stock FROM products ORDER BY name"
        ).fetchall()
        conn.close()
        return [
            Product(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                price=row["price"],
                quantity=row["quantity"],
                min_stock=row["min_stock"]
            )
            for row in rows
        ]
    
    def search_by_name(self, term: str) -> list[Product]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, name, category, price, quantity, min_stock FROM products WHERE name LIKE ? ORDER BY name",
            (f"%{term}%",),
        ).fetchall
        conn.close()
        return[
            Product(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                price=row["price"],
                quantity=row["quantity"],
                min_stock=row["min_stock"],
            )
            for row in rows
        ]
    
    def update(self, product: Product) -> None:
        conn = get_connection()
        conn.execute(
            """
            UPDATE products
            SET name = ?, category = ?, price = ?, quantity = ?, min_stock = ?
            WHERE id = ?
            """,
            (product.name, product.category, product.price, product.quantity, product.min_stock, product.id),
        )
        conn.commit()
        conn.close()

    def delete(self, product_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    def get_by_id(self, product_id: int) -> Product | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, name, category, price, quantity, min_stock FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        conn.close()

        if row is None:
            return None
        
        return Product(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            price=row["price"],
            quantity=row["quantity"],
            min_stock=row["min_stock"],
        )
    
    def update_quantity(self, product_id: int, new_quantity: int) -> None:
        conn = get_connection()
        conn.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        conn.close()

class MovementRepository:
    def create(self, product_id: int, movement_type: str, quantity: int) -> None:
        conn = get_connection()
        conn.execute(
            "INSERT INTO movements (product_id, movement_type, quantity) VALUES (?, ?, ?)",
            (product_id, movement_type, quantity),
        )
        conn.commit()
        conn.close()