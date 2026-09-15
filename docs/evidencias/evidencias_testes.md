# Evidências de Testes Automatizados

Este documento registra a execução da suíte de testes automatizados do
projeto, como evidência de que o software funciona conforme
especificado. A saída completa e literal do terminal está anexada em
[`saida_pytest_completa.txt`](saida_pytest_completa.txt).

## Ambiente de execução

| Item | Valor |
|---|---|
| Data da execução | 2026-09-15 |
| Python | 3.11.15 |
| pytest | 9.1.1 |
| FastAPI | 0.141.1 |
| httpx | 0.28.1 |
| Comando executado | `pytest testes/ -v` |
| Banco de dados | SQLite em memória (`:memory:`), isolado do banco de produção (`dados/loja.sqlite`) |

## Resultado

```
======================== 84 passed, 2 warnings in 0.65s ========================
```

**84 de 84 testes passando (100%).** Os 2 avisos (`warnings`) são
depreciações de bibliotecas de terceiros (`starlette`/`fastapi`) sem
relação com o código do projeto e não afetam o funcionamento da
aplicação.

## Metodologia

Todos os módulos do backend foram desenvolvidos seguindo o ciclo
**TDD (Test-Driven Development) — Red, Green, Refactor**: o teste era
escrito e confirmado como falho antes de qualquer código de produção
existir (Red); em seguida, implementava-se o código mínimo necessário
para o teste passar (Green); por fim, o código era refatorado para
incorporar proteções adicionais reveladas pelos próprios testes
(Refactor). Os testes só eram movidos para a pasta `testes/` do
repositório depois de confirmados como passando.

## Distribuição dos testes por tipo

| Tipo de teste | Quantidade | Descrição |
|---|---|---|
| Testes de modelo (`test_modelo_*.py`) | 20 | Validação dos modelos Pydantic (produto, carrinho, cupom, frete, endereço, favorito) |
| Testes de repositório (`test_repositorio_*.py`) | 25 | Acesso a dados e regras de persistência no SQLite |
| Testes de serviço (`test_servico_*.py`) | 14 | Regras de negócio puras (cálculo de desconto, frete, integração com ViaCEP) |
| Testes de API/integração (`test_api_*.py`) | 23 | Comportamento HTTP completo de cada endpoint (via `TestClient` do FastAPI) |
| Teste de integração ponta a ponta | 1 | Fluxo completo de compra: catálogo → carrinho → cupom → frete → CEP → favoritos |
| **Total** | **84** | |

## Distribuição dos testes por módulo funcional

| Módulo | Arquivo(s) | Quantidade |
|---|---|---|
| Produtos | `test_modelo_produto.py`, `test_repositorio_produtos.py`, `test_api_produtos.py` | 12 |
| Carrinho | `test_modelo_carrinho.py`, `test_repositorio_carrinho.py`, `test_api_carrinho.py` | 20 |
| Cupom de desconto | `test_modelo_cupom.py`, `test_repositorio_cupons.py`, `test_servico_cupom.py`, `test_api_cupom.py` | 16 |
| Frete | `test_modelo_frete.py`, `test_servico_frete.py`, `test_api_frete.py` | 11 |
| Endereço (ViaCEP) | `test_modelo_endereco.py`, `test_servico_endereco.py`, `test_api_endereco.py` | 10 |
| Favoritos | `test_modelo_favorito.py`, `test_repositorio_favoritos.py`, `test_api_favoritos.py` | 14 |
| Integração ponta a ponta | `test_integracao_fluxo_completo.py` | 1 |
| **Total** | | **84** |

## Falha real identificada e corrigida durante o TDD

Durante o ciclo Red-Green-Refactor do módulo de produtos, o primeiro
teste de integração da API falhou com erro `500 Internal Server Error`
em vez do esperado `200 OK`. A causa raiz identificada foi uma
dependência frágil: a aplicação só criava o esquema do banco de dados
no evento de `lifespan` do FastAPI, então qualquer código que abrisse
uma conexão fora desse fluxo (como o teste, inicialmente) quebrava.
A correção (etapa *Refactor*) tornou `obter_conexao()` autossuficiente,
garantindo o esquema do banco a cada conexão — eliminando essa classe
de falha silenciosa. Essa é a evidência mais concreta de que o processo
de TDD adotado cumpriu seu papel de revelar e proteger contra bugs
reais, e não apenas validar o comportamento já esperado.

## Falha real identificada durante testes manuais (perspectiva do avaliador)

Além das falhas capturadas pelo TDD durante o desenvolvimento, uma
falha de frontend foi identificada posteriormente ao testar o sistema
seguindo o próprio passo a passo de instalação e uso, do ponto de
vista de um avaliador: ao informar um CEP inexistente (ex:
`00000000`), o sistema calculava e exibia o frete normalmente, mas não
informava que o endereço não foi encontrado — a busca falhava em
silêncio. A causa e a correção completa (incluindo evidência visual
antes/depois) estão documentadas em
[`correcao_cep_nao_encontrado.md`](correcao_cep_nao_encontrado.md).

## Como reproduzir esta evidência

```bash
pip install -r requirements-dev.txt
pytest testes/ -v
```
