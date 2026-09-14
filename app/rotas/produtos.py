"""Rotas relacionadas ao catálogo de produtos."""

from fastapi import APIRouter, HTTPException

from app.banco_dados.conexao import obter_conexao
from app.modelos.produto import Produto
from app.repositorios.repositorio_produtos import (
    listar_produtos,
    obter_produto_por_id,
)

roteador = APIRouter(prefix="/api/produtos", tags=["produtos"])


@roteador.get("", response_model=list[Produto])
def rota_listar_produtos() -> list[Produto]:
    """Retorna a lista de todos os produtos do catálogo."""
    try:
        with obter_conexao() as conexao:
            return listar_produtos(conexao)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.get("/{produto_id}", response_model=Produto)
def rota_obter_produto(produto_id: int) -> Produto:
    """Retorna um produto específico pelo id, ou erro 404 se não existir."""
    try:
        with obter_conexao() as conexao:
            produto = obter_produto_por_id(conexao, produto_id)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro

    if produto is None:
        raise HTTPException(
            status_code=404, detail=f"Produto {produto_id} não encontrado"
        )
    return produto
