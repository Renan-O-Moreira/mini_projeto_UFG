"""Integração com a API pública ViaCEP para busca de endereço por CEP."""

import re

import httpx

from app.modelos.endereco import Endereco

URL_BASE_VIACEP = "https://viacep.com.br/ws"
PADRAO_CEP = re.compile(r"^\d{5}-?\d{3}$")


class EnderecoNaoEncontradoError(Exception):
    """Levantada quando o CEP é válido no formato, mas não existe."""


def buscar_endereco_por_cep(
    cep: str, cliente_http: httpx.Client | None = None
) -> Endereco:
    """Busca o endereço correspondente a um CEP na API ViaCEP.

    Levanta `ValueError` se o CEP estiver em formato inválido,
    `EnderecoNaoEncontradoError` se o CEP não existir, e `RuntimeError`
    em caso de falha de comunicação com a API.
    """
    if not PADRAO_CEP.match(cep):
        raise ValueError(f"CEP '{cep}' está em formato inválido")

    cep_formatado = _formatar_cep(cep)
    cliente = cliente_http if cliente_http is not None else httpx.Client(timeout=5.0)
    deve_fechar_cliente = cliente_http is None

    try:
        resposta = cliente.get(f"{URL_BASE_VIACEP}/{cep_formatado}/json/")
        resposta.raise_for_status()
        dados = resposta.json()
    except httpx.HTTPError as erro:
        raise RuntimeError(f"Falha ao consultar o CEP {cep}: {erro}") from erro
    finally:
        if deve_fechar_cliente:
            cliente.close()

    if dados.get("erro"):
        raise EnderecoNaoEncontradoError(f"CEP {cep} não encontrado")

    return Endereco(
        cep=dados.get("cep", cep_formatado),
        logradouro=dados.get("logradouro") or "",
        bairro=dados.get("bairro") or "",
        cidade=dados.get("localidade") or "",
        estado=dados.get("uf") or "",
    )


def _formatar_cep(cep: str) -> str:
    """Normaliza o CEP para o formato `NNNNN-NNN` esperado pela ViaCEP."""
    apenas_digitos = re.sub(r"\D", "", cep)
    return f"{apenas_digitos[:5]}-{apenas_digitos[5:]}"
