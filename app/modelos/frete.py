"""Modelos de dados relacionados ao cálculo de frete."""

from pydantic import BaseModel, Field


class EntradaCalcularFrete(BaseModel):
    """Dados recebidos para calcular o frete a partir de um CEP."""

    cep: str = Field(min_length=1)


class ResultadoFrete(BaseModel):
    """Resultado do cálculo de frete simulado para um CEP."""

    cep: str
    valor_frete: float = Field(ge=0)
    prazo_dias: int = Field(gt=0)
