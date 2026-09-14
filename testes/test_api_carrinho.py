"""Testes de integração dos endpoints do carrinho (ciclo TDD 4)."""

import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


def test_listar_carrinho_vazio_retorna_200(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.get("/api/carrinho")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_incluir_item_no_carrinho_retorna_201(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post(
        "/api/carrinho",
        json={"produto_id": 1, "nome_cor": "Branca", "quantidade": 2},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["produto_id"] == 1
    assert corpo["quantidade"] == 2
    assert corpo["subtotal"] == pytest.approx(119.80)


def test_incluir_item_com_produto_inexistente_retorna_400(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.post(
        "/api/carrinho",
        json={"produto_id": 999, "nome_cor": "Branca", "quantidade": 1},
    )

    assert resposta.status_code == 400


def test_alterar_quantidade_de_item_retorna_200(cliente_teste: TestClient) -> None:
    item = cliente_teste.post(
        "/api/carrinho",
        json={"produto_id": 1, "nome_cor": "Branca", "quantidade": 1},
    ).json()

    resposta = cliente_teste.patch(
        f"/api/carrinho/{item['id']}", json={"quantidade": 7}
    )

    assert resposta.status_code == 200
    assert resposta.json()["quantidade"] == 7


def test_alterar_quantidade_de_item_inexistente_retorna_404(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.patch("/api/carrinho/999", json={"quantidade": 1})

    assert resposta.status_code == 404


def test_excluir_item_do_carrinho_retorna_204(cliente_teste: TestClient) -> None:
    item = cliente_teste.post(
        "/api/carrinho",
        json={"produto_id": 1, "nome_cor": "Branca", "quantidade": 1},
    ).json()

    resposta = cliente_teste.delete(f"/api/carrinho/{item['id']}")

    assert resposta.status_code == 204
    assert cliente_teste.get("/api/carrinho").json() == []


def test_excluir_item_inexistente_retorna_404(cliente_teste: TestClient) -> None:
    resposta = cliente_teste.delete("/api/carrinho/999")

    assert resposta.status_code == 404
