from unittest.mock import Mock, patch

import pytest

from src.external_api import API_URL, convert_to_rub


@pytest.mark.parametrize("currency_code", ["USD", "EUR"])
def test_convert_to_rub_uses_api_for_foreign_currency(currency_code: str) -> None:
    transaction = {
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"code": currency_code},
        }
    }

    with (
        patch("src.external_api.API_KEY", "test-api-key"),
        patch("src.external_api.requests.get") as mock_get,
    ):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "900000.0"}
        mock_get.return_value = mock_response

        result = convert_to_rub(transaction)

    assert result == 900000.0
    assert isinstance(result, float)
    mock_get.assert_called_once_with(
        API_URL,
        params={"amount": "9824.07", "from": currency_code, "to": "RUB"},
        headers={"apikey": "test-api-key"},
    )
    mock_response.raise_for_status.assert_called_once_with()


def test_convert_to_rub_returns_rub_without_api_call() -> None:
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"},
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_to_rub(transaction)

    assert result == 100.50
    assert isinstance(result, float)
    mock_get.assert_not_called()


def test_convert_to_rub_requires_api_key() -> None:
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }

    with (
        patch("src.external_api.API_KEY", None),
        patch("src.external_api.requests.get") as mock_get,
        pytest.raises(ValueError, match="EXCHANGE_RATES_API_KEY"),
    ):
        convert_to_rub(transaction)

    mock_get.assert_not_called()
