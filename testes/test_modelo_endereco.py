"""Testes unitários do modelo de dados de endereço (ciclo TDD 1)."""

from app.modelos.endereco import Endereco


def test_cria_endereco_valido() -> None:
    endereco = Endereco(
        cep="74000-000",
        logradouro="Avenida Central",
        bairro="Centro",
        cidade="Goiânia",
        estado="GO",
    )

    assert endereco.cep == "74000-000"
    assert endereco.cidade == "Goiânia"
    assert endereco.estado == "GO"


def test_endereco_aceita_logradouro_e_bairro_vazios() -> None:
    endereco = Endereco(
        cep="74000-000",
        logradouro="",
        bairro="",
        cidade="Goiânia",
        estado="GO",
    )

    assert endereco.logradouro == ""
