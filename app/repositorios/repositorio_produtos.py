"""Acesso a dados de produtos no banco SQLite."""

import sqlite3

from app.modelos.produto import CorProduto, Produto

PRODUTOS_INICIAIS = [
    {
        "nome": "Camiseta Básica",
        "descricao": "Camiseta 100% algodão, corte tradicional.",
        "preco": 59.90,
        "cores": [
            {"nome_cor": "Branca", "url_imagem": "/imagens/produtos/camiseta_branca.svg"},
            {"nome_cor": "Preta", "url_imagem": "/imagens/produtos/camiseta_preta.svg"},
        ],
    },
    {
        "nome": "Tênis Esportivo",
        "descricao": "Tênis leve para corrida e caminhada.",
        "preco": 199.90,
        "cores": [
            {"nome_cor": "Cinza", "url_imagem": "/imagens/produtos/tenis_cinza.svg"},
            {"nome_cor": "Azul", "url_imagem": "/imagens/produtos/tenis_azul.svg"},
        ],
    },
    {
        "nome": "Mochila Casual",
        "descricao": "Mochila resistente com compartimento para notebook.",
        "preco": 149.90,
        "cores": [
            {"nome_cor": "Preta", "url_imagem": "/imagens/produtos/mochila_preta.svg"},
            {"nome_cor": "Verde", "url_imagem": "/imagens/produtos/mochila_verde.svg"},
        ],
    },
]


def popular_produtos_iniciais(conexao: sqlite3.Connection) -> None:
    """Insere os produtos iniciais caso a tabela de produtos esteja vazia."""
    try:
        cursor = conexao.execute("SELECT COUNT(*) AS total FROM produtos")
        total_produtos = cursor.fetchone()["total"]
        if total_produtos > 0:
            return

        for produto in PRODUTOS_INICIAIS:
            cursor = conexao.execute(
                "INSERT INTO produtos (nome, descricao, preco) VALUES (?, ?, ?)",
                (produto["nome"], produto["descricao"], produto["preco"]),
            )
            produto_id = cursor.lastrowid
            for cor in produto["cores"]:
                conexao.execute(
                    """
                    INSERT INTO cores_produto (produto_id, nome_cor, url_imagem)
                    VALUES (?, ?, ?)
                    """,
                    (produto_id, cor["nome_cor"], cor["url_imagem"]),
                )
        conexao.commit()
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Falha ao popular produtos iniciais: {erro}") from erro


def listar_produtos(conexao: sqlite3.Connection) -> list[Produto]:
    """Retorna todos os produtos cadastrados, com suas respectivas cores."""
    try:
        linhas_produtos = conexao.execute(
            "SELECT id, nome, descricao, preco FROM produtos ORDER BY id"
        ).fetchall()

        produtos = []
        for linha in linhas_produtos:
            cores = _obter_cores_do_produto(conexao, linha["id"])
            produtos.append(
                Produto(
                    id=linha["id"],
                    nome=linha["nome"],
                    descricao=linha["descricao"],
                    preco=linha["preco"],
                    cores=cores,
                )
            )
        return produtos
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao listar produtos: {erro}") from erro


def obter_produto_por_id(conexao: sqlite3.Connection, produto_id: int) -> Produto | None:
    """Retorna um produto específico pelo seu id, ou `None` se não existir."""
    try:
        linha = conexao.execute(
            "SELECT id, nome, descricao, preco FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()

        if linha is None:
            return None

        cores = _obter_cores_do_produto(conexao, produto_id)
        return Produto(
            id=linha["id"],
            nome=linha["nome"],
            descricao=linha["descricao"],
            preco=linha["preco"],
            cores=cores,
        )
    except sqlite3.Error as erro:
        raise RuntimeError(f"Falha ao obter produto {produto_id}: {erro}") from erro


def _obter_cores_do_produto(
    conexao: sqlite3.Connection, produto_id: int
) -> list[CorProduto]:
    """Retorna as opções de cor cadastradas para um produto."""
    linhas_cores = conexao.execute(
        "SELECT nome_cor, url_imagem FROM cores_produto WHERE produto_id = ?",
        (produto_id,),
    ).fetchall()
    return [
        CorProduto(nome_cor=cor["nome_cor"], url_imagem=cor["url_imagem"])
        for cor in linhas_cores
    ]
