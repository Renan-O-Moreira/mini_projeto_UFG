"""Testes unitários do repositório de favoritos (ciclo TDD 2)."""

import sqlite3

import pytest

from app.repositorios.repositorio_favoritos import (
    adicionar_favorito,
    listar_favoritos,
    remover_favorito,
)


def test_listar_favoritos_retorna_lista_vazia_quando_nao_ha_favoritos(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    assert listar_favoritos(conexao_com_produtos) == []


def test_adicionar_favorito_inclui_produto_na_listagem(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    adicionar_favorito(conexao_com_produtos, produto_id=1)

    favoritos = listar_favoritos(conexao_com_produtos)

    assert len(favoritos) == 1
    assert favoritos[0].id == 1


def test_adicionar_mesmo_favorito_duas_vezes_e_idempotente(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    adicionar_favorito(conexao_com_produtos, produto_id=1)
    adicionar_favorito(conexao_com_produtos, produto_id=1)

    assert len(listar_favoritos(conexao_com_produtos)) == 1


def test_adicionar_favorito_com_produto_inexistente_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        adicionar_favorito(conexao_com_produtos, produto_id=999)


def test_remover_favorito_exclui_da_listagem(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    adicionar_favorito(conexao_com_produtos, produto_id=1)

    remover_favorito(conexao_com_produtos, produto_id=1)

    assert listar_favoritos(conexao_com_produtos) == []


def test_remover_favorito_inexistente_gera_erro(
    conexao_com_produtos: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError):
        remover_favorito(conexao_com_produtos, produto_id=1)
