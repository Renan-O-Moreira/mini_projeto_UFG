"""Modelos de dados relacionados a endereços."""

from pydantic import BaseModel


class Endereco(BaseModel):
    """Representa um endereço obtido a partir de um CEP."""

    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
