"""Testes unitários dos modelos de dados de frete (ciclo TDD 1)."""

import pytest
from pydantic import ValidationError

from app.modelos.frete import EntradaCalcularFrete, ResultadoFrete


def test_cria_entrada_calcular_frete_valida() -> None:
    entrada = EntradaCalcularFrete(cep="74000-000")

    assert entrada.cep == "74000-000"


def test_entrada_calcular_frete_rejeita_cep_vazio() -> None:
    with pytest.raises(ValidationError):
        EntradaCalcularFrete(cep="")


def test_cria_resultado_frete_valido() -> None:
    resultado = ResultadoFrete(cep="74000-000", valor_frete=25.0, prazo_dias=6)

    assert resultado.valor_frete == 25.0
    assert resultado.prazo_dias == 6
