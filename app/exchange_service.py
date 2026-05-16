from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ExchangeService:
    """Busca a cotação do dólar em reais.

    Usa apenas bibliotecas padrão do Python para evitar dependência extra
    e reduzir problemas com ambiente virtual.
    """

    API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    def get_usd_brl_rate(self) -> dict[str, Any]:
        request = Request(
            self.API_URL,
            headers={"User-Agent": "controle-estoque-python/1.0"},
        )

        try:
            with urlopen(request, timeout=8) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Não foi possível carregar a cotação do dólar: {exc}") from exc

        usd_brl = data.get("USDBRL")
        if not usd_brl:
            raise RuntimeError("Resposta da API não contém a chave USDBRL.")

        try:
            bid = float(usd_brl["bid"])
            ask = float(usd_brl["ask"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Resposta da API está incompleta: {exc}") from exc

        return {
            "name": usd_brl.get("name", "Dólar Americano/Real Brasileiro"),
            "bid": bid,
            "ask": ask,
            "date": usd_brl.get("create_date", ""),
        }
