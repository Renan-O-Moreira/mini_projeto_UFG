"""Funções de conexão e inicialização do banco de dados SQLite."""

import sqlite3
from pathlib import Path

from app.config import CAMINHO_BANCO_DADOS, CAMINHO_ESQUEMA_SQL


def obter_conexao(caminho_banco: Path = CAMINHO_BANCO_DADOS) -> sqlite3.Connection:
    """Abre e retorna uma conexão com o banco de dados SQLite.

    A conexão é configurada para retornar linhas como `sqlite3.Row`,
    permitindo acesso aos campos pelo nome da coluna. O esquema é
    garantido a cada conexão (via `CREATE TABLE IF NOT EXISTS`), para
    que a API não falhe caso seja acionada antes do evento de
    `lifespan` da aplicação ter sido executado (ex.: em testes ou
    scripts que abrem a conexão diretamente).
    """
    try:
        caminho_banco.parent.mkdir(parents=True, exist_ok=True)
        conexao = sqlite3.connect(caminho_banco)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        _garantir_esquema(conexao)
        return conexao
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao conectar ao banco de dados: {erro}") from erro


def inicializar_banco(caminho_banco: Path = CAMINHO_BANCO_DADOS) -> None:
    """Cria as tabelas do banco de dados a partir do script de esquema.

    É seguro chamar esta função múltiplas vezes: o script utiliza
    `CREATE TABLE IF NOT EXISTS` para cada tabela.
    """
    try:
        with obter_conexao(caminho_banco) as conexao:
            _garantir_esquema(conexao)
    except (sqlite3.Error, OSError) as erro:
        raise RuntimeError(f"Falha ao inicializar o banco de dados: {erro}") from erro


def _garantir_esquema(conexao: sqlite3.Connection) -> None:
    """Executa o script de esquema, criando tabelas ainda não existentes."""
    script_sql = CAMINHO_ESQUEMA_SQL.read_text(encoding="utf-8")
    conexao.executescript(script_sql)
