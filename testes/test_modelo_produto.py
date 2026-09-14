"""Testes unitários do modelo de dados Produto (ciclo TDD 1)."""

import pytest
from pydantic import ValidationError

from app.modelos.produto import CorProduto, Produto


def test_cria_produto_valido_com_cores() -> None:
    produto = Produto(
        id=1,
        nome="Camiseta Básica",
        descricao="Camiseta 100% algodão.",
        preco=59.90,
        cores=[CorProduto(nome_cor="Branca", url_imagem="/img/branca.png")],
    )

    assert produto.nome == "Camiseta Básica"
    assert produto.cores[0].nome_cor == "Branca"


def test_produto_sem_cores_usa_lista_vazia_por_padrao() -> None:
    produto = Produto(id=1, nome="Camiseta", descricao="desc", preco=10.0)

    assert produto.cores == []


def test_produto_rejeita_preco_negativo() -> None:
    with pytest.raises(ValidationError):
        Produto(id=1, nome="Camiseta", descricao="desc", preco=-5.0)
