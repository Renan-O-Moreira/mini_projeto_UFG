"""Acesso a dados do carrinho de compras no banco SQLite."""

import sqlite3

from app.modelos.carrinho import ItemCarrinhoDetalhado


def adicionar_item(
    conexao: sqlite3.Connection,
    produto_id: int,
    nome_cor: str,
    quantidade: int,
) -> ItemCarrinhoDetalhado:
    """Inclui um item no carrinho, ou soma a quantidade se já existir.

    Levanta `ValueError` se o produto não existir ou se a cor informada
    não for uma opção válida para esse produto.
    """
    _validar_produto_e_cor(conexao, produto_id, nome_cor)

    try:
        item_existente = conexao.execute(
            "SELECT id, quantidade FROM itens_carrinho WHERE produto_id = ? AND nome_cor = ?",
            (produto_id, nome_cor),
        ).fetchone()

        if item_existente is not None:
            nova_quantidade = item_existente["quantidade"] + quantidade
            conexao.execute(
                "UPDATE itens_carrinho SET quantidade = ? WHERE id = ?",
                (nova_quantidade, item_existente["id"]),
            )
            item_id = item_existente["id"]
        else:
            cursor = conexao.execute(
                """
                INSERT INTO itens_carrinho (produto_id, nome_cor, quantidade)
                VALUES (?, ?, ?)
                """,
                (produto_id, nome_cor, quantidade),
            )
            item_id = cursor.lastrowid

        conexao.commit()
        return _obter_item_detalhado(conexao, item_id)
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao adicionar item ao carrinho: {erro}") from erro


def listar_itens(conexao: sqlite3.Connection) -> list[ItemCarrinhoDetalhado]:
    """Retorna todos os itens atualmente no carrinho, com dados do produto."""
    try:
        linhas = conexao.execute(
            "SELECT id FROM itens_carrinho ORDER BY id"
        ).fetchall()
        return [_obter_item_detalhado(conexao, linha["id"]) for linha in linhas]
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao listar itens do carrinho: {erro}") from erro


def atualizar_quantidade(
    conexao: sqlite3.Connection, item_id: int, quantidade: int
) -> ItemCarrinhoDetalhado:
    """Altera a quantidade de um item do carrinho.

    Levanta `ValueError` se o item não existir.
    """
    _garantir_item_existe(conexao, item_id)
    try:
        conexao.execute(
            "UPDATE itens_carrinho SET quantidade = ? WHERE id = ?",
            (quantidade, item_id),
        )
        conexao.commit()
        return _obter_item_detalhado(conexao, item_id)
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao atualizar quantidade do item: {erro}") from erro


def remover_item(conexao: sqlite3.Connection, item_id: int) -> None:
    """Remove um item do carrinho.

    Levanta `ValueError` se o item não existir.
    """
    _garantir_item_existe(conexao, item_id)
    try:
        conexao.execute("DELETE FROM itens_carrinho WHERE id = ?", (item_id,))
        conexao.commit()
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao remover item do carrinho: {erro}") from erro


def _validar_produto_e_cor(
    conexao: sqlite3.Connection, produto_id: int, nome_cor: str
) -> None:
    """Garante que o produto exista e que a cor seja válida para ele."""
    cor_valida = conexao.execute(
        "SELECT 1 FROM cores_produto WHERE produto_id = ? AND nome_cor = ?",
        (produto_id, nome_cor),
    ).fetchone()
    if cor_valida is None:
        raise ValueError(
            f"Cor '{nome_cor}' inválida para o produto {produto_id}, "
            "ou produto inexistente"
        )


def _garantir_item_existe(conexao: sqlite3.Connection, item_id: int) -> None:
    """Levanta `ValueError` se o item do carrinho não existir."""
    existe = conexao.execute(
        "SELECT 1 FROM itens_carrinho WHERE id = ?", (item_id,)
    ).fetchone()
    if existe is None:
        raise ValueError(f"Item {item_id} não encontrado no carrinho")


def _obter_item_detalhado(
    conexao: sqlite3.Connection, item_id: int
) -> ItemCarrinhoDetalhado:
    """Monta um `ItemCarrinhoDetalhado` a partir do id do item no carrinho."""
    linha = conexao.execute(
        """
        SELECT
            itens_carrinho.id AS id,
            itens_carrinho.produto_id AS produto_id,
            itens_carrinho.nome_cor AS nome_cor,
            itens_carrinho.quantidade AS quantidade,
            produtos.nome AS nome_produto,
            produtos.preco AS preco_unitario
        FROM itens_carrinho
        JOIN produtos ON produtos.id = itens_carrinho.produto_id
        WHERE itens_carrinho.id = ?
        """,
        (item_id,),
    ).fetchone()
    return ItemCarrinhoDetalhado(
        id=linha["id"],
        produto_id=linha["produto_id"],
        nome_produto=linha["nome_produto"],
        nome_cor=linha["nome_cor"],
        preco_unitario=linha["preco_unitario"],
        quantidade=linha["quantidade"],
    )
