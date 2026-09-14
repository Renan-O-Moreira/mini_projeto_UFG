"""Modelos de dados relacionados a produtos."""

from pydantic import BaseModel, Field


class CorProduto(BaseModel):
    """Representa uma opção de cor disponível para um produto."""

    nome_cor: str
    url_imagem: str


class Produto(BaseModel):
    """Representa um produto do catálogo da loja."""

    id: int
    nome: str
    descricao: str
    preco: float = Field(ge=0)
    cores: list[CorProduto] = Field(default_factory=list)
