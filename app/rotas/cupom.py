"""Rotas relacionadas à aplicação de cupons de desconto."""

from fastapi import APIRouter, HTTPException

from app.banco_dados.conexao import obter_conexao
from app.modelos.cupom import EntradaAplicarCupom, ResultadoCupom
from app.repositorios.repositorio_cupons import obter_cupom_por_codigo
from app.servicos.servico_cupom import calcular_desconto

roteador = APIRouter(prefix="/api/cupom", tags=["cupom"])


@roteador.post("/aplicar", response_model=ResultadoCupom)
def rota_aplicar_cupom(entrada: EntradaAplicarCupom) -> ResultadoCupom:
    """Valida um cupom pelo código e calcula o desconto sobre o valor total."""
    try:
        with obter_conexao() as conexao:
            cupom = obter_cupom_por_codigo(conexao, entrada.codigo)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro

    if cupom is None:
        raise HTTPException(
            status_code=404, detail=f"Cupom '{entrada.codigo}' não encontrado"
        )

    return calcular_desconto(cupom, entrada.valor_total)
