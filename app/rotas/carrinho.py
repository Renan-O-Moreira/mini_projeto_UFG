"""Rotas relacionadas ao carrinho de compras."""

from fastapi import APIRouter, HTTPException, Response

from app.banco_dados.conexao import obter_conexao
from app.modelos.carrinho import (
    AtualizacaoQuantidade,
    ItemCarrinhoDetalhado,
    ItemCarrinhoEntrada,
)
from app.repositorios.repositorio_carrinho import (
    adicionar_item,
    atualizar_quantidade,
    listar_itens,
    remover_item,
)

roteador = APIRouter(prefix="/api/carrinho", tags=["carrinho"])


@roteador.get("", response_model=list[ItemCarrinhoDetalhado])
def rota_listar_carrinho() -> list[ItemCarrinhoDetalhado]:
    """Retorna todos os itens atualmente no carrinho de compras."""
    try:
        with obter_conexao() as conexao:
            return listar_itens(conexao)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.post("", response_model=ItemCarrinhoDetalhado, status_code=201)
def rota_incluir_item(item: ItemCarrinhoEntrada) -> ItemCarrinhoDetalhado:
    """Inclui um item no carrinho, ou soma a quantidade se já existir."""
    try:
        with obter_conexao() as conexao:
            return adicionar_item(
                conexao, item.produto_id, item.nome_cor, item.quantidade
            )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.patch("/{item_id}", response_model=ItemCarrinhoDetalhado)
def rota_alterar_quantidade(
    item_id: int, dados: AtualizacaoQuantidade
) -> ItemCarrinhoDetalhado:
    """Altera a quantidade de um item já existente no carrinho."""
    try:
        with obter_conexao() as conexao:
            return atualizar_quantidade(conexao, item_id, dados.quantidade)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro


@roteador.delete("/{item_id}", status_code=204)
def rota_remover_item(item_id: int) -> Response:
    """Remove um item do carrinho."""
    try:
        with obter_conexao() as conexao:
            remover_item(conexao, item_id)
        return Response(status_code=204)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro
