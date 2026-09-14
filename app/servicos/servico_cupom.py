"""Regras de negócio de cálculo de desconto por cupom."""

from app.modelos.cupom import Cupom, ResultadoCupom


def calcular_desconto(cupom: Cupom, valor_total: float) -> ResultadoCupom:
    """Calcula o desconto de um cupom sobre um valor total.

    O desconto é aplicado como um percentual simples sobre `valor_total`.
    """
    valor_desconto = round(valor_total * (cupom.percentual_desconto / 100), 2)
    valor_total_com_desconto = round(valor_total - valor_desconto, 2)

    return ResultadoCupom(
        codigo=cupom.codigo,
        percentual_desconto=cupom.percentual_desconto,
        valor_desconto=valor_desconto,
        valor_total_com_desconto=valor_total_com_desconto,
    )
