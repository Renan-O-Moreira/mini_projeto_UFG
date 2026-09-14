"""Testes de integração dos endpoints de favoritos (ciclo TDD 3)."""

import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


def test_listar_favoritos_vazio_retorna_200(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/favoritos")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_adicionar_favorito_retorna_201(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post("/api/favoritos", json={"produto_id": 1})

    assert resposta.status_code == 201
    assert len(cliente_teste.get("/api/favoritos").json()) == 1


def test_adicionar_favorito_com_produto_inexistente_retorna_400(
    cliente_teste: TestClient,
) -> None:
    resposta = cliente_teste.post("/api/favoritos", json={"produto_id": 999})

    assert resposta.status_code == 400


def test_remover_favorito_retorna_204(cliente_teste: TestClient) -> None:
    cliente_teste.post("/api/favoritos", json={"produto_id": 1})

    resposta = cliente_teste.delete("/api/favoritos/1")

    assert resposta.status_code == 204
    assert cliente_teste.get("/api/favoritos").json() == []


def test_remover_favorito_inexistente_retorna_404(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.delete("/api/favoritos/1")

    assert resposta.status_code == 404
