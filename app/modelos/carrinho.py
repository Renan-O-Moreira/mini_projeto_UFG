"""Modelos de dados relacionados ao carrinho de compras."""

from pydantic import BaseModel, Field, computed_field


class ItemCarrinhoEntrada(BaseModel):
    """Dados recebidos ao incluir um item no carrinho."""

    produto_id: int
    nome_cor: str
    quantidade: int = Field(gt=0)


class AtualizacaoQuantidade(BaseModel):
    """Dados recebidos ao alterar a quantidade de um item do carrinho."""

    quantidade: int = Field(gt=0)


class ItemCarrinhoDetalhado(BaseModel):
    """Representa um item do carrinho já enriquecido com dados do produto."""

    id: int
    produto_id: int
    nome_produto: str
    nome_cor: str
    preco_unitario: float = Field(ge=0)
    quantidade: int = Field(gt=0)

    @computed_field
    @property
    def subtotal(self) -> float:
        """Calcula o subtotal do item (preço unitário x quantidade)."""
        return round(self.preco_unitario * self.quantidade, 2)
