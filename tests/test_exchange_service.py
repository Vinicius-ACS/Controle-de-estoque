import json
from unittest.mock import patch

from app.exchange_service import ExchangeService


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(
            {
                "USDBRL": {
                    "name": "Dólar Americano/Real Brasileiro",
                    "bid": "5.4321",
                    "ask": "5.4521",
                    "create_date": "2026-05-16 10:00:00",
                }
            }
        ).encode("utf-8")


def test_get_usd_brl_rate_success():
    with patch("app.exchange_service.urlopen", return_value=FakeResponse()):
        data = ExchangeService().get_usd_brl_rate()

    assert data["name"] == "Dólar Americano/Real Brasileiro"
    assert data["bid"] == 5.4321
    assert data["ask"] == 5.4521
    assert data["date"] == "2026-05-16 10:00:00"