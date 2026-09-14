"""Rotas relacionadas à busca de endereço a partir do CEP (API ViaCEP)."""

import httpx
from fastapi import APIRouter, HTTPException

from app.modelos.endereco import Endereco
from app.servicos.servico_endereco import (
    EnderecoNaoEncontradoError,
    buscar_endereco_por_cep,
)

roteador = APIRouter(prefix="/api/endereco", tags=["endereco"])


def _obter_cliente_http() -> httpx.Client | None:
    """Retorna o cliente HTTP a ser usado na consulta à ViaCEP.

    Retorna `None` para que o serviço crie e gerencie seu próprio
    cliente HTTP real; este ponto de extensão existe para que os
    testes de integração possam substituí-lo por um cliente simulado.
    """
    return None


@roteador.get("/{cep}", response_model=Endereco)
def rota_buscar_endereco(cep: str) -> Endereco:
    """Busca o endereço correspondente ao CEP informado, via ViaCEP."""
    try:
        return buscar_endereco_por_cep(cep, cliente_http=_obter_cliente_http())
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    except EnderecoNaoEncontradoError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
