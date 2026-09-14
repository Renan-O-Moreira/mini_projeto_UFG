"""Testes unitários do serviço de cálculo de frete simulado (ciclo TDD 2)."""

import pytest

from app.servicos.servico_frete import calcular_frete


def test_calcular_frete_com_cep_valido_e_formatado_retorna_resultado() -> None:
    resultado = calcular_frete("74000-000")

    assert resultado.cep == "74000-000"
    assert resultado.valor_frete > 0
    assert resultado.prazo_dias > 0


def test_calcular_frete_aceita_cep_sem_hifen() -> None:
    resultado = calcular_frete("74000000")

    assert resultado.valor_frete > 0


def test_calcular_frete_com_mesmo_primeiro_digito_tem_mesmo_valor() -> None:
    resultado_1 = calcular_frete("74000-000")
    resultado_2 = calcular_frete("74999-999")

    assert resultado_1.valor_frete == resultado_2.valor_frete
    assert resultado_1.prazo_dias == resultado_2.prazo_dias


def test_calcular_frete_com_regioes_diferentes_tem_valores_diferentes() -> None:
    resultado_regiao_0 = calcular_frete("01000-000")
    resultado_regiao_9 = calcular_frete("90000-000")

    assert resultado_regiao_0.valor_frete != resultado_regiao_9.valor_frete


def test_calcular_frete_com_cep_de_formato_invalido_gera_erro() -> None:
    with pytest.raises(ValueError):
        calcular_frete("123")


def test_calcular_frete_com_cep_nao_numerico_gera_erro() -> None:
    with pytest.raises(ValueError):
        calcular_frete("abcde-fgh")
