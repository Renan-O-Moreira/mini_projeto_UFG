"""Acesso a dados de cupons de desconto no banco SQLite."""

import sqlite3

from app.modelos.cupom import Cupom

CUPONS_INICIAIS = [
    {"codigo": "BEMVINDO10", "percentual_desconto": 10.0},
    {"codigo": "FRETEGRATIS20", "percentual_desconto": 20.0},
]


def popular_cupons_iniciais(conexao: sqlite3.Connection) -> None:
    """Insere os cupons iniciais caso a tabela de cupons esteja vazia."""
    try:
        total = conexao.execute("SELECT COUNT(*) AS total FROM cupons").fetchone()[
            "total"
        ]
        if total > 0:
            return

        for cupom in CUPONS_INICIAIS:
            conexao.execute(
                "INSERT INTO cupons (codigo, percentual_desconto) VALUES (?, ?)",
                (cupom["codigo"], cupom["percentual_desconto"]),
            )
        conexao.commit()
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao popular cupons iniciais: {erro}") from erro


def obter_cupom_por_codigo(conexao: sqlite3.Connection, codigo: str) -> Cupom | None:
    """Retorna um cupom pelo código, ou `None` se não existir.

    A busca não diferencia maiúsculas de minúsculas.
    """
    try:
        linha = conexao.execute(
            "SELECT codigo, percentual_desconto FROM cupons WHERE UPPER(codigo) = UPPER(?)",
            (codigo,),
        ).fetchone()

        if linha is None:
            return None

        return Cupom(
            codigo=linha["codigo"], percentual_desconto=linha["percentual_desconto"]
        )
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao obter cupom '{codigo}': {erro}") from erro
