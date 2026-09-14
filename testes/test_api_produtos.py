"""Testes de integração dos endpoints de produtos (ciclo TDD 4)."""

import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao


@pytest.fixture
def cliente_teste():
    """Cliente de testes que aciona o ciclo de vida (lifespan) da aplicação."""
    with TestClient(aplicacao) as cliente:
        yield cliente


def test_listar_produtos_retorna_200_e_tres_produtos(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/produtos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_obter_produto_existente_retorna_200(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/produtos/1")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == 1


def test_obter_produto_inexistente_retorna_404(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/produtos/999")

    assert resposta.status_code == 404
