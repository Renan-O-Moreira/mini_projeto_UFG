"""Testes de integração do endpoint de cupom (ciclo TDD 4)."""

import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


def test_aplicar_cupom_valido_retorna_200(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post(
        "/api/cupom/aplicar", json={"codigo": "BEMVINDO10", "valor_total": 100.0}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["valor_desconto"] == pytest.approx(10.0)
    assert corpo["valor_total_com_desconto"] == pytest.approx(90.0)


def test_aplicar_cupom_e_insensivel_a_maiusculas(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post(
        "/api/cupom/aplicar", json={"codigo": "bemvindo10", "valor_total": 100.0}
    )

    assert resposta.status_code == 200


def test_aplicar_cupom_inexistente_retorna_404(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post(
        "/api/cupom/aplicar", json={"codigo": "NAOEXISTE", "valor_total": 100.0}
    )

    assert resposta.status_code == 404


def test_aplicar_cupom_com_valor_total_negativo_retorna_422(
    cliente_teste: TestClient,
) -> None:
    resposta = cliente_teste.post(
        "/api/cupom/aplicar", json={"codigo": "BEMVINDO10", "valor_total": -10.0}
    )

    assert resposta.status_code == 422
