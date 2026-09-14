"""Testes de integração do endpoint de frete (ciclo TDD 3)."""

import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


def test_calcular_frete_com_cep_valido_retorna_200(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/frete/74000-000")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["valor_frete"] > 0
    assert corpo["prazo_dias"] > 0


def test_calcular_frete_com_cep_invalido_retorna_400(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/frete/123")

    assert resposta.status_code == 400
