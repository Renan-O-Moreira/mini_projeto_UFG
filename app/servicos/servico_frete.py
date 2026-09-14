"""Regras de negócio de cálculo de frete simulado por região de CEP.

O frete é simulado localmente a partir do primeiro dígito do CEP (que,
no Brasil, indica a macrorregião de destino), sem depender de nenhuma
API paga de transportadora ou dos Correios.
"""

import re

from app.modelos.frete import ResultadoFrete

TABELA_FRETE_POR_REGIAO = {
    "0": {"valor_frete": 15.0, "prazo_dias": 3},
    "1": {"valor_frete": 18.0, "prazo_dias": 4},
    "2": {"valor_frete": 20.0, "prazo_dias": 5},
    "3": {"valor_frete": 22.0, "prazo_dias": 5},
    "4": {"valor_frete": 25.0, "prazo_dias": 6},
    "5": {"valor_frete": 28.0, "prazo_dias": 6},
    "6": {"valor_frete": 30.0, "prazo_dias": 7},
    "7": {"valor_frete": 32.0, "prazo_dias": 7},
    "8": {"valor_frete": 35.0, "prazo_dias": 8},
    "9": {"valor_frete": 40.0, "prazo_dias": 10},
}

PADRAO_CEP = re.compile(r"^\d{5}-?\d{3}$")


def calcular_frete(cep: str) -> ResultadoFrete:
    """Calcula o frete simulado para um CEP.

    Levanta `ValueError` se o CEP não estiver no formato `NNNNN-NNN`
    ou `NNNNNNNN`.
    """
    if not PADRAO_CEP.match(cep):
        raise ValueError(f"CEP '{cep}' está em formato inválido")

    primeiro_digito = cep[0]
    regiao = TABELA_FRETE_POR_REGIAO[primeiro_digito]

    return ResultadoFrete(
        cep=cep,
        valor_frete=regiao["valor_frete"],
        prazo_dias=regiao["prazo_dias"],
    )
