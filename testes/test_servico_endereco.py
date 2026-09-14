"""Testes unitários do serviço de busca de endereço via CEP (ciclo TDD 2)."""

import httpx
import pytest

from app.servicos.servico_endereco import (
    EnderecoNaoEncontradoError,
    buscar_endereco_por_cep,
)


def _cliente_com_resposta(dados_json: dict, status_code: int = 200) -> httpx.Client:
    def manipulador(requisicao: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=dados_json)

    transporte = httpx.MockTransport(manipulador)
    return httpx.Client(transport=transporte)


def test_buscar_endereco_por_cep_valido_retorna_endereco_preenchido() -> None:
    cliente = _cliente_com_resposta(
        {
            "cep": "74000-000",
            "logradouro": "Avenida Central",
            "bairro": "Centro",
            "localidade": "Goiânia",
            "uf": "GO",
        }
    )

    endereco = buscar_endereco_por_cep("74000-000", cliente_http=cliente)

    assert endereco.cidade == "Goiânia"
    assert endereco.estado == "GO"
    assert endereco.logradouro == "Avenida Central"


def test_buscar_endereco_por_cep_aceita_cep_sem_hifen() -> None:
    cliente = _cliente_com_resposta(
        {
            "cep": "74000-000",
            "logradouro": "Avenida Central",
            "bairro": "Centro",
            "localidade": "Goiânia",
            "uf": "GO",
        }
    )

    endereco = buscar_endereco_por_cep("74000000", cliente_http=cliente)

    assert endereco.cep == "74000-000"


def test_buscar_endereco_com_cep_inexistente_gera_erro_de_nao_encontrado() -> None:
    cliente = _cliente_com_resposta({"erro": True})

    with pytest.raises(EnderecoNaoEncontradoError):
        buscar_endereco_por_cep("00000-000", cliente_http=cliente)


def test_buscar_endereco_com_formato_invalido_gera_value_error() -> None:
    with pytest.raises(ValueError):
        buscar_endereco_por_cep("123", cliente_http=_cliente_com_resposta({}))


def test_buscar_endereco_com_falha_de_rede_gera_runtime_error() -> None:
    def manipulador(requisicao: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("falha simulada de rede", request=requisicao)

    cliente = httpx.Client(transport=httpx.MockTransport(manipulador))

    with pytest.raises(RuntimeError):
        buscar_endereco_por_cep("74000-000", cliente_http=cliente)
