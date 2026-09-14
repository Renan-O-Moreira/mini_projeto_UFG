"""Testes unitários do serviço de cálculo de desconto (ciclo TDD 3)."""

import pytest

from app.modelos.cupom import Cupom
from app.servicos.servico_cupom import calcular_desconto


def test_calcular_desconto_aplica_percentual_corretamente() -> None:
    cupom = Cupom(codigo="BEMVINDO10", percentual_desconto=10.0)

    resultado = calcular_desconto(cupom, valor_total=200.0)

    assert resultado.valor_desconto == pytest.approx(20.0)
    assert resultado.valor_total_com_desconto == pytest.approx(180.0)
    assert resultado.codigo == "BEMVINDO10"


def test_calcular_desconto_com_percentual_de_cem_zera_o_total() -> None:
    cupom = Cupom(codigo="GRATIS", percentual_desconto=100.0)

    resultado = calcular_desconto(cupom, valor_total=50.0)

    assert resultado.valor_total_com_desconto == pytest.approx(0.0)


def test_calcular_desconto_com_valor_total_zero_retorna_zero() -> None:
    cupom = Cupom(codigo="BEMVINDO10", percentual_desconto=10.0)

    resultado = calcular_desconto(cupom, valor_total=0.0)

    assert resultado.valor_desconto == pytest.approx(0.0)
    assert resultado.valor_total_com_desconto == pytest.approx(0.0)
