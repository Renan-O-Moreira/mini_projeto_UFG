"""Testes unitários do modelo de dados de favorito (ciclo TDD 1)."""

import pytest
from pydantic import ValidationError

from app.modelos.favorito import EntradaFavorito


def test_cria_entrada_favorito_valida() -> None:
    entrada = EntradaFavorito(produto_id=1)

    assert entrada.produto_id == 1


def test_entrada_favorito_rejeita_produto_id_zero() -> None:
    with pytest.raises(ValidationError):
        EntradaFavorito(produto_id=0)


def test_entrada_favorito_rejeita_produto_id_negativo() -> None:
    with pytest.raises(ValidationError):
        EntradaFavorito(produto_id=-1)
