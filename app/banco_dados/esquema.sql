-- Esquema do banco de dados da loja virtual (SQLite)
-- Este script é executado na inicialização da aplicação, caso as
-- tabelas ainda não existam.

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS cores_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    nome_cor TEXT NOT NULL,
    url_imagem TEXT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS itens_carrinho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    nome_cor TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    percentual_desconto REAL NOT NULL CHECK (
        percentual_desconto > 0 AND percentual_desconto <= 100
    )
);
