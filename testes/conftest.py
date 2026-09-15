"""Fixtures compartilhadas entre os testes."""

import sqlite3
from pathlib import Path

import pytest

from app import config
from app.config import CAMINHO_ESQUEMA_SQL
from app.repositorios.repositorio_produtos import popular_produtos_iniciais


@pytest.fixture(autouse=True)
def banco_de_dados_isolado(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Isola cada teste em um banco de dados SQLite temporário e exclusivo.

    Sem esta fixture, testes que sobem a aplicação real via `TestClient`
    (ex.: `test_api_*.py`) acabam lendo e escrevendo no banco de dados
    de produção (`dados/loja.sqlite`), poluindo a suíte com dados de
    execuções manuais anteriores (ex.: itens de carrinho deixados por
    testes feitos pelo navegador). Isso é aplicado automaticamente a
    todos os testes, sem precisar ser referenciado explicitamente.
    """
    caminho_temporario = tmp_path / "teste_loja.sqlite"
    monkeypatch.setattr(config, "CAMINHO_BANCO_DADOS", caminho_temporario)


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
