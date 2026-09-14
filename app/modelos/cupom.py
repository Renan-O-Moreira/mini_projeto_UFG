"""Modelos de dados relacionados a cupons de desconto."""

from pydantic import BaseModel, Field


class Cupom(BaseModel):
    """Representa um cupom de desconto cadastrado."""

    codigo: str
    percentual_desconto: float = Field(gt=0, le=100)


class EntradaAplicarCupom(BaseModel):
    """Dados recebidos para aplicar um cupom sobre um valor total."""

    codigo: str
    valor_total: float = Field(ge=0)


class ResultadoCupom(BaseModel):
    """Resultado da aplicação de um cupom sobre um valor total."""

    codigo: str
    percentual_desconto: float
    valor_desconto: float
    valor_total_com_desconto: float
