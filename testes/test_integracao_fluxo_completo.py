"""Teste de integração do fluxo completo da loja virtual.

Simula a jornada de um cliente ponta a ponta, exercitando todos os
módulos do backend em conjunto: catálogo de produtos, carrinho de
compras, cupom de desconto, cálculo de frete, busca de endereço por
CEP e favoritos.
"""

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import aplicacao
from app.rotas import endereco as modulo_rota_endereco


@pytest.fixture
def cliente_teste():
    with TestClient(aplicacao) as cliente:
        yield cliente


@pytest.fixture(autouse=True)
def simular_viacep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Substitui o cliente HTTP da ViaCEP por um cliente simulado.

    Evita que o teste de integração dependa de acesso real à
    internet, mantendo-o determinístico e executável em qualquer
    ambiente (inclusive sandboxes sem acesso à rede externa).
    """

    def manipulador(requisicao: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "cep": "74000-000",
                "logradouro": "Avenida Central",
                "bairro": "Centro",
                "localidade": "Goiânia",
                "uf": "GO",
            },
        )

    cliente_falso = httpx.Client(transport=httpx.MockTransport(manipulador))
    monkeypatch.setattr(
        modulo_rota_endereco, "_obter_cliente_http", lambda: cliente_falso
    )


def test_fluxo_completo_da_loja_virtual(cliente_teste: TestClient) -> None:
    # 1. Cliente consulta o catálogo de produtos.
    resposta_produtos = cliente_teste.get("/api/produtos")
    assert resposta_produtos.status_code == 200
    produtos = resposta_produtos.json()
    assert len(produtos) == 3

    primeiro_produto = produtos[0]
    segundo_produto = produtos[1]
    cor_primeiro_produto = primeiro_produto["cores"][0]["nome_cor"]
    cor_segundo_produto = segundo_produto["cores"][0]["nome_cor"]

    # 2. Cliente inclui dois produtos diferentes no carrinho.
    resposta_item_1 = cliente_teste.post(
        "/api/carrinho",
        json={
            "produto_id": primeiro_produto["id"],
            "nome_cor": cor_primeiro_produto,
            "quantidade": 2,
        },
    )
    assert resposta_item_1.status_code == 201
    item_1 = resposta_item_1.json()

    resposta_item_2 = cliente_teste.post(
        "/api/carrinho",
        json={
            "produto_id": segundo_produto["id"],
            "nome_cor": cor_segundo_produto,
            "quantidade": 1,
        },
    )
    assert resposta_item_2.status_code == 201

    # 3. Cliente altera a quantidade do primeiro item.
    resposta_atualizacao = cliente_teste.patch(
        f"/api/carrinho/{item_1['id']}", json={"quantidade": 3}
    )
    assert resposta_atualizacao.status_code == 200
    assert resposta_atualizacao.json()["quantidade"] == 3

    # 4. Cliente consulta o carrinho e calcula o valor total dos itens.
    itens_carrinho = cliente_teste.get("/api/carrinho").json()
    assert len(itens_carrinho) == 2
    valor_total_carrinho = sum(item["subtotal"] for item in itens_carrinho)

    # 5. Cliente aplica um cupom de desconto sobre o valor total.
    resposta_cupom = cliente_teste.post(
        "/api/cupom/aplicar",
        json={"codigo": "BEMVINDO10", "valor_total": valor_total_carrinho},
    )
    assert resposta_cupom.status_code == 200
    resultado_cupom = resposta_cupom.json()
    assert resultado_cupom["valor_total_com_desconto"] == pytest.approx(
        valor_total_carrinho * 0.9
    )

    # 6. Cliente informa o CEP e obtém o endereço de entrega.
    resposta_endereco = cliente_teste.get("/api/endereco/74000-000")
    assert resposta_endereco.status_code == 200
    assert resposta_endereco.json()["cidade"] == "Goiânia"

    # 7. Cliente calcula o frete para o mesmo CEP.
    resposta_frete = cliente_teste.get("/api/frete/74000-000")
    assert resposta_frete.status_code == 200
    valor_frete = resposta_frete.json()["valor_frete"]

    # 8. Valor final da compra = total com desconto + frete.
    valor_final = resultado_cupom["valor_total_com_desconto"] + valor_frete
    assert valor_final > 0

    # 9. Cliente favorita o primeiro produto e confirma na lista de favoritos.
    resposta_favoritar = cliente_teste.post(
        "/api/favoritos", json={"produto_id": primeiro_produto["id"]}
    )
    assert resposta_favoritar.status_code == 201

    favoritos = cliente_teste.get("/api/favoritos").json()
    assert any(produto["id"] == primeiro_produto["id"] for produto in favoritos)

    # 10. Cliente remove o segundo item do carrinho.
    item_2_id = cliente_teste.get("/api/carrinho").json()[1]["id"]
    resposta_remocao = cliente_teste.delete(f"/api/carrinho/{item_2_id}")
    assert resposta_remocao.status_code == 204
    assert len(cliente_teste.get("/api/carrinho").json()) == 1

    # 11. Cliente desfavorita o produto.
    resposta_desfavoritar = cliente_teste.delete(
        f"/api/favoritos/{primeiro_produto['id']}"
    )
    assert resposta_desfavoritar.status_code == 204
    assert cliente_teste.get("/api/favoritos").json() == []
