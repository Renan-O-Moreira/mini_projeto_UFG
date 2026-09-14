"""Testes de integração do endpoint de endereço/CEP (ciclo TDD 3)."""

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao
from app.rotas import endereco as modulo_rota_endereco


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


def _simular_cliente_viacep(monkeypatch, dados_json: dict, status_code: int = 200) -> None:
    def manipulador(requisicao: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=dados_json)

    cliente_falso = httpx.Client(transport=httpx.MockTransport(manipulador))
    monkeypatch.setattr(modulo_rota_endereco, "_obter_cliente_http", lambda: cliente_falso)


def test_buscar_endereco_com_cep_valido_retorna_200(
    cliente_teste: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _simular_cliente_viacep(
        monkeypatch,
        {
            "cep": "74000-000",
            "logradouro": "Avenida Central",
            "bairro": "Centro",
            "localidade": "Goiânia",
            "uf": "GO",
        },
    )

    resposta = cliente_teste.get("/api/endereco/74000-000")

    assert resposta.status_code == 200
    assert resposta.json()["cidade"] == "Goiânia"


def test_buscar_endereco_com_cep_inexistente_retorna_404(
    cliente_teste: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _simular_cliente_viacep(monkeypatch, {"erro": True})

    resposta = cliente_teste.get("/api/endereco/00000-000")

    assert resposta.status_code == 404


def test_buscar_endereco_com_formato_invalido_retorna_400(
    cliente_teste: TestClient,
) -> None:
    resposta = cliente_teste.get("/api/endereco/123")

    assert resposta.status_code == 400
