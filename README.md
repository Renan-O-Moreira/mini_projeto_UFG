# 🛒 Loja Virtual — Mini-Projeto UFG

> Simulação de página de vendas de produtos com carrinho de compras,
> cálculo de frete/desconto e integração com API de CEP, desenvolvida
> como MVP para o laboratório de Inteligência Artificial Generativa da
> Pós-Graduação em Engenharia de Software da UFG.

<!-- TODO: adicionar banner do projeto em docs/imagens/banner.png -->

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.11x-009688">
  <img alt="Licença" src="https://img.shields.io/badge/licença-ver%20LICENSE-lightgrey">
</p>

## Descrição do projeto

Este projeto é um **MVP (Produto Mínimo Viável)** que simula uma loja
virtual com três produtos, permitindo explorar, na prática, o uso de
Inteligência Artificial Generativa em diferentes etapas do ciclo de vida
do desenvolvimento de software: geração de código, testes automatizados,
documentação e refatoração.

A aplicação roda em **servidor local** e pode ser **empacotada** para
ser testada em outra máquina pelo avaliador da atividade, sem custos com
APIs ou serviços pagos.

### Funcionalidades principais

- 🛍️ Catálogo com 3 produtos, cada um com fotos e opções de cor
- 🛒 Carrinho de compras: incluir, excluir e alterar quantidade de itens
- ⭐ Favoritar produtos, com página dedicada de favoritos
- 🏷️ Aplicação de cupom de desconto sobre o valor da compra
- 📍 Busca de endereço a partir do CEP (API pública ViaCEP)
- 🚚 Cálculo de frete simulado a partir do CEP informado
- 📑 Documentação interativa da API (Swagger/OpenAPI, gerada pelo FastAPI)

---

## Sumário

- [Descrição do projeto](#descrição-do-projeto)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação passo a passo](#instalação-passo-a-passo)
- [Uso e exemplos](#uso-e-exemplos)
- [Exemplos de requisições para os endpoints principais](#exemplos-de-requisições-para-os-endpoints-principais)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como a IA acelerou este projeto](#como-a-ia-acelerou-este-projeto)
- [Capturas de tela](#capturas-de-tela)
- [Versão de entrega](#versão-de-entrega)
- [Limitações e próximos passos](#limitações-e-próximos-passos)
- [Autores e contribuição](#autores-e-contribuição)
- [Licença](#licença)

---

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Backend | [Python 3.11+](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/) |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |
| Banco de dados | [SQLite](https://www.sqlite.org/) (nativo do Python, via `sqlite3`) |
| Validação de dados | [Pydantic](https://docs.pydantic.dev/) |
| Frontend | HTML5 + CSS3 + JavaScript (vanilla) |
| API de CEP | [ViaCEP](https://viacep.com.br/) (pública e gratuita) |
| Testes | [pytest](https://docs.pytest.org/) + [httpx](https://www.python-httpx.org/) |
| Documentação de API | Swagger UI / ReDoc (gerados automaticamente pelo FastAPI) |

> _Esta tabela será atualizada conforme novas dependências forem
> adicionadas ao projeto._

---

## Pré-requisitos

- [Python 3.11 ou superior](https://www.python.org/downloads/) instalado
- [pip](https://pip.pypa.io/en/stable/installation/) (geralmente já
  incluso na instalação do Python)
- Navegador web atualizado (Chrome, Firefox, Edge, etc.)
- Conexão com a internet (apenas para a consulta de CEP via ViaCEP)

> _Nenhuma chave de API ou serviço pago é necessário para executar o
> projeto._

---

## Instalação passo a passo

> _Seção em construção — será detalhada conforme o projeto avança._

```bash
# 1. Clonar o repositório
git clone https://github.com/Renan-O-Moreira/mini_projeto_UFG.git
cd mini_projeto_UFG

# 2. Criar e ativar um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Iniciar a aplicação
python main.py
```

Após iniciar, acesse:

- Aplicação: <http://localhost:8000>
- Documentação interativa da API (Swagger): <http://localhost:8000/docs>

---

## Uso e exemplos

> _Seção em construção — será preenchida com o passo a passo de uso da
> aplicação (navegação pelo catálogo, carrinho, cupom, frete e
> favoritos) conforme as funcionalidades forem implementadas._

---

## Exemplos de requisições para os endpoints principais

> _Seção em construção — será preenchida com exemplos de requisições
> (`curl`/HTTP) para os principais endpoints da API assim que forem
> implementados._

```bash
# Exemplo (placeholder): consultar produtos disponíveis
curl -X GET "http://localhost:8000/api/produtos"
```

---

## Estrutura do projeto

> _Seção em construção — será preenchida com a árvore de diretórios do
> projeto assim que a estrutura inicial for criada._

```text
mini_projeto_UFG/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── ...
```

---

## Como a IA acelerou este projeto

> _Seção em construção — será documentada ao longo do desenvolvimento,
> registrando em quais etapas (geração de código, testes, documentação,
> refatoração, revisão) a IA generativa foi utilizada e qual foi o
> ganho observado._

---

## Capturas de tela

> _Seção em construção — screenshots e GIFs demonstrando o
> funcionamento da aplicação serão adicionados aqui conforme as telas
> forem implementadas._

<!-- Exemplo de formato a ser usado:
![Tela do catálogo](docs/imagens/catalogo.png)
![Fluxo do carrinho de compras](docs/imagens/carrinho.gif)
-->

---

## Versão de entrega

| Versão | Data | Descrição |
|---|---|---|
| `v1.0.0` | _a definir_ | Versão final de entrega da atividade |

---

## Limitações e próximos passos

### Limitações conhecidas

- Cálculo de frete é **simulado** com base em regras locais (não
  utiliza API paga de transportadoras/Correios)
- Catálogo restrito a 3 produtos fixos, sem cadastro dinâmico de novos
  produtos
- Sem autenticação de usuários (favoritos e carrinho são de sessão
  única, sem múltiplos usuários)

### Próximos passos (fora do escopo do MVP)

- Autenticação e múltiplos usuários
- Integração com API real de frete
- Painel administrativo para cadastro de produtos
- Persistência de carrinho entre sessões/dispositivos

---

## Autores e contribuição

| Nome | Contato |
|---|---|
| Renan O. Moreira | reom19@gmail.com |

Contribuições são bem-vindas por meio de _issues_ e _pull requests_.

---

## Licença

Este projeto está licenciado sob os termos definidos no arquivo
[LICENSE](LICENSE).
