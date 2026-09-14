"""Modelos de dados relacionados a produtos favoritados."""

from pydantic import BaseModel, Field


class EntradaFavorito(BaseModel):
    """Dados recebidos para marcar um produto como favorito."""

    produto_id: int = Field(gt=0)
