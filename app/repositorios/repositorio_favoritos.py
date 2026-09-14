"""Acesso a dados de produtos favoritados no banco SQLite."""

import sqlite3

from app.modelos.produto import Produto
from app.repositorios.repositorio_produtos import obter_produto_por_id


def adicionar_favorito(conexao: sqlite3.Connection, produto_id: int) -> None:
    """Marca um produto como favorito.

    A operação é idempotente: marcar o mesmo produto duas vezes não
    gera duplicidade. Levanta `ValueError` se o produto não existir.
    """
    if obter_produto_por_id(conexao, produto_id) is None:
        raise ValueError(f"Produto {produto_id} não encontrado")

    try:
        conexao.execute(
            "INSERT OR IGNORE INTO favoritos (produto_id) VALUES (?)",
            (produto_id,),
        )
        conexao.commit()
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao adicionar favorito: {erro}") from erro


def listar_favoritos(conexao: sqlite3.Connection) -> list[Produto]:
    """Retorna os produtos atualmente marcados como favoritos."""
    try:
        linhas = conexao.execute(
            "SELECT produto_id FROM favoritos ORDER BY id"
        ).fetchall()
        produtos = [
            obter_produto_por_id(conexao, linha["produto_id"]) for linha in linhas
        ]
        return [produto for produto in produtos if produto is not None]
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao listar favoritos: {erro}") from erro


def remover_favorito(conexao: sqlite3.Connection, produto_id: int) -> None:
    """Remove um produto dos favoritos.

    Levanta `ValueError` se o produto não estiver favoritado.
    """
    existe = conexao.execute(
        "SELECT 1 FROM favoritos WHERE produto_id = ?", (produto_id,)
    ).fetchone()
    if existe is None:
        raise ValueError(f"Produto {produto_id} não está nos favoritos")

    try:
        conexao.execute("DELETE FROM favoritos WHERE produto_id = ?", (produto_id,))
        conexao.commit()
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao remover favorito: {erro}") from erro
