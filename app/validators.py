def validate_product_data(name: str, category: str, price: float, quantity: int, min_stock: int) -> list[str]:
    errors: list[str] = []

    if not name.strip():
        errors.append("O nome do produto é obrigatorio.")
    if not category.strip():
        errors.append("A categoria é obrigatoria.")
    if price < 0:
        errors.append("O preço não pode ser negativo.")
    if quantity < 0:
        errors.append("A quantidade não pode ser negativa.")
    if min_stock < 0:
        errors.append("O estoque mínimo não pode ser negativo.")

    return errors


def validate_movement(quantity: int) -> list[str]:
    errors: list[str] = []
    if quantity <= 0:
        errors.append("A quantidade deve ser maior que zero.")


    return errors

