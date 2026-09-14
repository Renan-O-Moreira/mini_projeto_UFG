"""Rotas relacionadas ao cálculo de frete."""

from fastapi import APIRouter, HTTPException

from app.modelos.frete import ResultadoFrete
from app.servicos.servico_frete import calcular_frete

roteador = APIRouter(prefix="/api/frete", tags=["frete"])


@roteador.get("/{cep}", response_model=ResultadoFrete)
def rota_calcular_frete(cep: str) -> ResultadoFrete:
    """Calcula o frete simulado para o CEP informado."""
    try:
        return calcular_frete(cep)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
