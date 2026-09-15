# Correção: testes de API poluídos pelo banco de dados real

## Como o problema foi encontrado

O avaliador, testando o projeto em sua própria máquina (Windows, via
Git Bash), seguiu o passo a passo documentado: deixou o servidor
(`python main.py`) rodando em um terminal enquanto usava a aplicação
manualmente pelo navegador, e rodou a suíte de testes
(`pytest testes/ -v`) em um segundo terminal, sem apagar nada entre um
passo e outro. O resultado foram **4 falhas**, todas com o mesmo
padrão: dados de execuções anteriores (itens de carrinho inseridos
manualmente pelo navegador) aparecendo onde os testes esperavam um
carrinho vazio ou uma quantidade específica. Exemplo do erro reportado:

```
AssertionError: assert [{'id': 1, 'produto_id': 1, 'nome_produto': 'Camiseta Básica', ...}] == []
```

## Causa raiz

A função `obter_conexao()` (em `app/banco_dados/conexao.py`) definia o
caminho do banco de dados como um **valor padrão de parâmetro**:

```python
def obter_conexao(caminho_banco: Path = CAMINHO_BANCO_DADOS) -> sqlite3.Connection:
```

Em Python, valores padrão de parâmetros são calculados **uma única
vez**, no momento em que a função é definida (ou seja, quando o módulo
é importado) — não a cada chamada. Isso significa que, embora os
testes de repositório (`test_repositorio_*.py`) já usassem
corretamente um banco SQLite em memória via fixture, os testes que
sobem a aplicação real via `TestClient` (`test_api_*.py` e o teste de
integração ponta a ponta) sempre acabavam usando o banco de dados real
do projeto (`dados/loja.sqlite`) — o mesmo arquivo usado quando alguém
roda `python main.py` e usa o site pelo navegador.

Esse problema já existia desde a implementação do módulo de produtos,
mas nunca havia sido percebido durante o desenvolvimento porque o
banco de dados real era manualmente apagado antes de cada execução da
suíte de testes. A validação feita pelo avaliador, exatamente como um
usuário real faria (servidor rodando + testes em paralelo, sem apagar
nada), foi o que expôs essa falha de isolamento.

## Correção aplicada

1. **`app/banco_dados/conexao.py`**: os parâmetros `caminho_banco` de
   `obter_conexao()` e `inicializar_banco()` passaram a ser opcionais
   (`Path | None = None`), resolvidos dinamicamente dentro da função a
   partir de `app.config.CAMINHO_BANCO_DADOS` a cada chamada, em vez de
   fixados na definição da função.
2. **`testes/conftest.py`**: nova fixture `banco_de_dados_isolado`,
   marcada como `autouse=True` (aplicada automaticamente a **todo**
   teste, sem precisar ser referenciada), que substitui
   `app.config.CAMINHO_BANCO_DADOS` por um arquivo SQLite temporário e
   exclusivo daquele teste (via `tmp_path` do pytest), garantindo que
   nenhum teste jamais leia ou escreva no banco de dados real.

## Validação da correção

Reproduzi o cenário relatado: subi o servidor real, inseri um item no
carrinho manualmente (via `curl`, simulando o uso pelo navegador) e,
com o servidor ainda rodando e o item ainda no banco, executei a suíte
de testes **sem apagar nada**:

```bash
# Servidor rodando e com 1 item no carrinho (inserido manualmente)
curl -s http://127.0.0.1:8000/api/carrinho
# [{"id":1,"produto_id":1,"nome_produto":"Camiseta Básica", ..., "quantidade":5, ...}]

# Testes executados em paralelo, sem apagar dados/loja.sqlite
pytest testes/ -v
# ======================== 84 passed, 2 warnings in 0.89s ========================

# Banco de dados real permanece intacto após os testes
curl -s http://127.0.0.1:8000/api/carrinho
# [{"id":1,"produto_id":1,"nome_produto":"Camiseta Básica", ..., "quantidade":5, ...}]
```

**84 de 84 testes passando**, e o item inserido manualmente no
carrinho continuou intacto no banco real após a execução — confirmando
que os testes não leem nem escrevem mais nesse arquivo. A saída
completa está em
[`saida_pytest_completa.txt`](saida_pytest_completa.txt).
