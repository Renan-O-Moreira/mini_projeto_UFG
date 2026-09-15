"""Ponto de entrada da aplicação FastAPI da loja virtual."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.banco_dados.conexao import inicializar_banco, obter_conexao
from app.repositorios.repositorio_cupons import popular_cupons_iniciais
from app.repositorios.repositorio_produtos import popular_produtos_iniciais
from app.rotas.carrinho import roteador as roteador_carrinho
from app.rotas.cupom import roteador as roteador_cupom
from app.rotas.endereco import roteador as roteador_endereco
from app.rotas.favoritos import roteador as roteador_favoritos
from app.rotas.frete import roteador as roteador_frete
from app.rotas.produtos import roteador as roteador_produtos


@asynccontextmanager
async def ciclo_de_vida(aplicacao: FastAPI):
    """Inicializa o banco de dados e popula os dados iniciais ao iniciar a aplicação."""
    inicializar_banco()
    with obter_conexao() as conexao:
        popular_produtos_iniciais(conexao)
        popular_cupons_iniciais(conexao)
    yield


aplicacao = FastAPI(
    title="Loja UFG",
    description="API da simulação de loja virtual desenvolvida como MVP.",
    version="0.1.0",
    lifespan=ciclo_de_vida,
)

aplicacao.include_router(roteador_produtos)
aplicacao.include_router(roteador_carrinho)
aplicacao.include_router(roteador_cupom)
aplicacao.include_router(roteador_frete)
aplicacao.include_router(roteador_endereco)
aplicacao.include_router(roteador_favoritos)

aplicacao.mount(
    "/", StaticFiles(directory="frontend", html=True), name="frontend"
)
