from app.service import ProductService


def test_service_instance() -> None:
    service = ProductService()
    assert service is not None