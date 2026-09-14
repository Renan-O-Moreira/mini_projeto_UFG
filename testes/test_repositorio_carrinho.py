"""Testes unitários do repositório de carrinho (ciclo TDD 2 e 3)."""

import sqlite3

import pytest

from app.repositorios.repositorio_carrinho import (
    adicionar_item,
    listar_itens,
    remover_item,
    atualizar_quantidade,
)


def test_listar_itens_retorna_lista_vazia_para_carrinho_novo(
    conexao_teste: sqlite3.Connection,
) -> None:
    assert listar_itens(conexao_teste) == []


def test_adicionar_item_inclui_no_carrinho(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    item = adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Branca", quantidade=2)

    assert item.produto_id == 1
    assert item.nome_cor == "Branca"
    assert item.quantidade == 2

    itens = listar_itens(conexao_com_produtos)
    assert len(itens) == 1


def test_adicionar_mesmo_produto_e_cor_soma_quantidade(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Branca", quantidade=2)
    item = adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Branca", quantidade=3)

    assert item.quantidade == 5
    assert len(listar_itens(conexao_com_produtos)) == 1


def test_adicionar_item_com_produto_inexistente_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        adicionar_item(conexao_com_produtos, produto_id=999, nome_cor="Branca", quantidade=1)


def test_adicionar_item_com_cor_invalida_para_o_produto_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Roxa", quantidade=1)


def test_remover_item_exclui_do_carrinho(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    item = adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Branca", quantidade=1)

    remover_item(conexao_com_produtos, item.id)

    assert listar_itens(conexao_com_produtos) == []


def test_remover_item_inexistente_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        remover_item(conexao_com_produtos, 999)


def test_atualizar_quantidade_altera_o_item(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    item = adicionar_item(conexao_com_produtos, produto_id=1, nome_cor="Branca", quantidade=1)

    item_atualizado = atualizar_quantidade(conexao_com_produtos, item.id, 10)

    assert item_atualizado.quantidade == 10


def test_atualizar_quantidade_de_item_inexistente_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        atualizar_quantidade(conexao_com_produtos, 999, 5)
