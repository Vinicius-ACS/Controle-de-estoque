from app.validators import validate_product_data, validate_movement


def test_validate_product_data_success() -> None:
    errors = validate_product_data("Arroz", "Alimentos", 10.0, 5, 2)
    assert errors == []


def test_validate_movement_invalid() -> None:
    errors = validate_movement(0)
    assert "A quantidade deve ser maior que zero." in errors