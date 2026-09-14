"""Testes unitários do repositório de cupons (ciclo TDD 2)."""

import sqlite3

from app.repositorios.repositorio_cupons import (
    CUPONS_INICIAIS,
    obter_cupom_por_codigo,
    popular_cupons_iniciais,
)


def test_obter_cupom_inexistente_retorna_none(
    conexao_teste: sqlite3.Connection,
) -> None:
    assert obter_cupom_por_codigo(conexao_teste, "NAOEXISTE") is None


def test_popular_cupons_iniciais_insere_os_cupons(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_cupons_iniciais(conexao_teste)

    primeiro_codigo = CUPONS_INICIAIS[0]["codigo"]
    cupom = obter_cupom_por_codigo(conexao_teste, primeiro_codigo)

    assert cupom is not None
    assert cupom.codigo == primeiro_codigo


def test_popular_cupons_iniciais_e_idempotente(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_cupons_iniciais(conexao_teste)
    popular_cupons_iniciais(conexao_teste)

    total = conexao_teste.execute("SELECT COUNT(*) AS total FROM cupons").fetchone()[
        "total"
    ]
    assert total == len(CUPONS_INICIAIS)


def test_obter_cupom_por_codigo_e_insensivel_a_maiusculas(
    conexao_teste: sqlite3.Connection,
) -> None:
    popular_cupons_iniciais(conexao_teste)
    primeiro_codigo = CUPONS_INICIAIS[0]["codigo"]

    cupom = obter_cupom_por_codigo(conexao_teste, primeiro_codigo.lower())

    assert cupom is not None
    assert cupom.codigo == primeiro_codigo
