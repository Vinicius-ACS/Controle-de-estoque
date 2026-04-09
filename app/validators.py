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

def validate_movement(quantity: int) -> list[str]:
    errors: list[str] = []
    if quantity <= 0:
        errors.append("A quantidade deve ser maior que zero.")
    return errors


def validate_user_data(name: str, user_id: str, email: str, password: str) -> list[str]:
    errors: list[str] = []

    if not name.strip():
        errors.append("O nome é obrigatório.")
    if not user_id.strip():
        errors.append("O ID do usuário é obrigatório.")
    if not email.strip():
        errors.append("O e-mail é obrigatório.")
    if "@" not in email or "." not in email:
        errors.append("Informe um e-mail válido.")
    if not password.strip():
        errors.append("A senha é obrigatória.")
    if len(password) < 4:
        errors.append("A senha deve ter pelo menos 4 caracteres.")

    return errors


def validate_login_data(user_id: str, password: str) -> list[str]:
    errors: list[str] = []

    if not user_id.strip():
        errors.append("Informe o ID do usuário.")
    if not password.strip():
        errors.append("Informe a senha.")

    return errors