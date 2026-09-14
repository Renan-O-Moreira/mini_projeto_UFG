"""Testes unitários do repositório de produtos (ciclo TDD 2 e 3)."""

import sqlite3

from app.repositorios.repositorio_produtos import (
    PRODUTOS_INICIAIS,
    listar_produtos,
    obter_produto_por_id,
    popular_produtos_iniciais,
)


def test_listar_produtos_retorna_lista_vazia_quando_nao_ha_produtos(
    conexao_teste: sqlite3.Connection,
) -> None:
    assert listar_produtos(conexao_teste) == []


def test_popular_produtos_iniciais_insere_os_tres_produtos(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_produtos_iniciais(conexao_teste)

    produtos = listar_produtos(conexao_teste)

    assert len(produtos) == len(PRODUTOS_INICIAIS)
    assert {produto.nome for produto in produtos} == {
        produto["nome"] for produto in PRODUTOS_INICIAIS
    }


def test_popular_produtos_iniciais_e_idempotente(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_produtos_iniciais(conexao_teste)
    popular_produtos_iniciais(conexao_teste)

    assert len(listar_produtos(conexao_teste)) == len(PRODUTOS_INICIAIS)


def test_listar_produtos_inclui_as_cores_de_cada_produto(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_produtos_iniciais(conexao_teste)

    for produto in listar_produtos(conexao_teste):
        assert len(produto.cores) >= 1


def test_obter_produto_por_id_retorna_o_produto_correto(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_produtos_iniciais(conexao_teste)
    primeiro_produto = listar_produtos(conexao_teste)[0]

    encontrado = obter_produto_por_id(conexao_teste, primeiro_produto.id)

    assert encontrado is not None
    assert encontrado.id == primeiro_produto.id


def test_obter_produto_por_id_retorna_none_para_id_inexistente(
    conexao_teste: sqlite3.Connection,
) -> None:
    assert obter_produto_por_id(conexao_teste, 999) is None
