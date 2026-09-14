"""Testes unitários dos modelos de dados de cupom (ciclo TDD 1)."""

import pytest
from pydantic import ValidationError

from app.modelos.cupom import Cupom, EntradaAplicarCupom


def test_cria_cupom_valido() -> None:
    cupom = Cupom(codigo="DESCONTO10", percentual_desconto=10.0)

    assert cupom.codigo == "DESCONTO10"
    assert cupom.percentual_desconto == 10.0


def test_cupom_rejeita_percentual_zero() -> None:
    with pytest.raises(ValidationError):
        Cupom(codigo="INVALIDO", percentual_desconto=0)


def test_cupom_rejeita_percentual_acima_de_cem() -> None:
    with pytest.raises(ValidationError):
        Cupom(codigo="INVALIDO", percentual_desconto=101)


def test_entrada_aplicar_cupom_valida() -> None:
    entrada = EntradaAplicarCupom(codigo="desconto10", valor_total=100.0)

    assert entrada.codigo == "desconto10"
    assert entrada.valor_total == 100.0


def test_entrada_aplicar_cupom_rejeita_valor_total_negativo() -> None:
    with pytest.raises(ValidationError):
        EntradaAplicarCupom(codigo="DESCONTO10", valor_total=-10.0)
