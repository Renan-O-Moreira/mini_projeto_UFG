"""Fixtures compartilhadas entre os testes."""

import sqlite3

import pytest

from app.config import CAMINHO_ESQUEMA_SQL
from app.repositorios.repositorio_produtos import popular_produtos_iniciais


@pytest.fixture
def conexao_teste() -> sqlite3.Connection:
    """Fornece uma conexão SQLite em memória, com o esquema já criado.

    Usar um banco em memória garante que os testes não interfiram no
    banco de dados real da aplicação (`dados/loja.sqlite`).
    """
    conexao = sqlite3.connect(":memory:")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    script_sql = CAMINHO_ESQUEMA_SQL.read_text(encoding="utf-8")
    conexao.executescript(script_sql)

    yield conexao

    conexao.close()


@pytest.fixture
def conexao_com_produtos(conexao_teste: sqlite3.Connection) -> sqlite3.Connection:
    """Conexão de teste já populada com os produtos iniciais."""
    popular_produtos_iniciais(conexao_teste)
    return conexao_teste
