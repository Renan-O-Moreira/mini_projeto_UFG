"""Testes unitários dos modelos de dados do carrinho (ciclo TDD 1)."""

import pytest
from pydantic import ValidationError

from app.modelos.carrinho import ItemCarrinhoEntrada, ItemCarrinhoDetalhado


def test_cria_item_carrinho_entrada_valido() -> None:
    item = ItemCarrinhoEntrada(produto_id=1, nome_cor="Branca", quantidade=2)

    assert item.produto_id == 1
    assert item.quantidade == 2


def test_item_carrinho_entrada_rejeita_quantidade_zero() -> None:
    with pytest.raises(ValidationError):
        ItemCarrinhoEntrada(produto_id=1, nome_cor="Branca", quantidade=0)


def test_item_carrinho_entrada_rejeita_quantidade_negativa() -> None:
    with pytest.raises(ValidationError):
        ItemCarrinhoEntrada(produto_id=1, nome_cor="Branca", quantidade=-1)


def test_cria_item_carrinho_detalhado_calcula_subtotal() -> None:
    item = ItemCarrinhoDetalhado(
        id=1,
        produto_id=1,
        nome_produto="Camiseta Básica",
        nome_cor="Branca",
        preco_unitario=59.90,
        quantidade=3,
    )

    assert item.subtotal == pytest.approx(179.70)
