"""Rotas relacionadas a produtos favoritados."""

from fastapi import APIRouter, HTTPException, Response

from app.banco_dados.conexao import obter_conexao
from app.modelos.favorito import EntradaFavorito
from app.modelos.produto import Produto
from app.repositorios.repositorio_favoritos import (
    adicionar_favorito,
    listar_favoritos,
    remover_favorito,
)

roteador = APIRouter(prefix="/api/favoritos", tags=["favoritos"])


@roteador.get("", response_model=list[Produto])
def rota_listar_favoritos() -> list[Produto]:
    """Retorna todos os produtos atualmente marcados como favoritos."""
    try:
        with obter_conexao() as conexao:
            return listar_favoritos(conexao)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.post("", status_code=201)
def rota_adicionar_favorito(entrada: EntradaFavorito) -> Response:
    """Marca um produto como favorito."""
    try:
        with obter_conexao() as conexao:
            adicionar_favorito(conexao, entrada.produto_id)
        return Response(status_code=201)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.delete("/{produto_id}", status_code=204)
def rota_remover_favorito(produto_id: int) -> Response:
    """Remove um produto dos favoritos."""
    try:
        with obter_conexao() as conexao:
            remover_favorito(conexao, produto_id)
        return Response(status_code=204)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro
