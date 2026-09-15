/**
 * Renderiza o catálogo de produtos e trata as interações do card:
 * troca de cor (com troca de foto), quantidade e favoritar.
 */

async function carregarCatalogo() {
  const grade = document.getElementById("grade-produtos");

  try {
    const [produtos, favoritos] = await Promise.all([
      requisitarApi("/produtos"),
      requisitarApi("/favoritos"),
    ]);
    const idsFavoritados = new Set(favoritos.map((produto) => produto.id));

    grade.innerHTML = "";
    produtos.forEach((produto) => grade.appendChild(criarCardProduto(produto, idsFavoritados.has(produto.id))));
  } catch (erro) {
    grade.innerHTML = `<p>Não foi possível carregar o catálogo: ${erro.message}</p>`;
  }
}

function criarCardProduto(produto, estaFavoritado) {
  const card = document.createElement("article");
  card.className = "card";

  let corSelecionada = produto.cores[0];
  let quantidade = 1;

  const foto = document.createElement("div");
  foto.className = "foto";
  const imagem = document.createElement("img");
  imagem.src = corSelecionada.url_imagem;
  imagem.alt = `${produto.nome} na cor ${corSelecionada.nome_cor}`;
  foto.appendChild(imagem);

  const botaoFavoritar = document.createElement("button");
  botaoFavoritar.className = "fav-btn";
  botaoFavoritar.type = "button";
  botaoFavoritar.dataset.favoritado = String(estaFavoritado);
  botaoFavoritar.textContent = estaFavoritado ? "♥" : "♡";
  botaoFavoritar.setAttribute("aria-label", "Favoritar produto");
  botaoFavoritar.addEventListener("click", () => alternarFavorito(produto.id, botaoFavoritar));
  foto.appendChild(botaoFavoritar);

  const corpo = document.createElement("div");
  corpo.className = "card-corpo";

  const titulo = document.createElement("h3");
  titulo.textContent = produto.nome;

  const descricao = document.createElement("p");
  descricao.className = "desc";
  descricao.textContent = produto.descricao;

  const listaCores = document.createElement("div");
  listaCores.className = "cores";
  produto.cores.forEach((cor) => {
    const botaoCor = document.createElement("button");
    botaoCor.type = "button";
    botaoCor.className = "cor" + (cor.nome_cor === corSelecionada.nome_cor ? " selecionada" : "");
    botaoCor.style.background = corParaCss(cor.nome_cor);
    botaoCor.title = cor.nome_cor;
    botaoCor.setAttribute("aria-label", `Cor ${cor.nome_cor}`);
    botaoCor.addEventListener("click", () => {
      corSelecionada = cor;
      imagem.src = cor.url_imagem;
      imagem.alt = `${produto.nome} na cor ${cor.nome_cor}`;
      listaCores.querySelectorAll(".cor").forEach((el) => el.classList.remove("selecionada"));
      botaoCor.classList.add("selecionada");
    });
    listaCores.appendChild(botaoCor);
  });

  const linhaQuantidade = document.createElement("div");
  linhaQuantidade.className = "qtd-linha";
  const botaoMenos = document.createElement("button");
  botaoMenos.type = "button";
  botaoMenos.className = "qtd-btn";
  botaoMenos.textContent = "−";
  const valorQuantidade = document.createElement("span");
  valorQuantidade.className = "qtd-valor";
  valorQuantidade.textContent = quantidade;
  const botaoMais = document.createElement("button");
  botaoMais.type = "button";
  botaoMais.className = "qtd-btn";
  botaoMais.textContent = "+";
  botaoMenos.addEventListener("click", () => {
    if (quantidade > 1) {
      quantidade -= 1;
      valorQuantidade.textContent = quantidade;
    }
  });
  botaoMais.addEventListener("click", () => {
    quantidade += 1;
    valorQuantidade.textContent = quantidade;
  });
  linhaQuantidade.append(botaoMenos, valorQuantidade, botaoMais);

  const linhaPreco = document.createElement("div");
  linhaPreco.className = "preco-linha";
  const preco = document.createElement("span");
  preco.className = "preco";
  preco.textContent = formatarMoeda(produto.preco);
  linhaPreco.appendChild(preco);

  const botaoAdicionar = document.createElement("button");
  botaoAdicionar.className = "add-btn";
  botaoAdicionar.type = "button";
  botaoAdicionar.textContent = "Adicionar ao carrinho";
  botaoAdicionar.addEventListener("click", async () => {
    botaoAdicionar.disabled = true;
    botaoAdicionar.textContent = "Adicionando...";
    try {
      await requisitarApi("/carrinho", {
        method: "POST",
        body: JSON.stringify({
          produto_id: produto.id,
          nome_cor: corSelecionada.nome_cor,
          quantidade,
        }),
      });
      botaoAdicionar.textContent = "Adicionado!";
      await atualizarBadgeCarrinho();
      setTimeout(() => {
        botaoAdicionar.textContent = "Adicionar ao carrinho";
        botaoAdicionar.disabled = false;
      }, 1200);
    } catch (erro) {
      botaoAdicionar.textContent = "Erro ao adicionar";
      botaoAdicionar.disabled = false;
    }
  });

  corpo.append(titulo, descricao, listaCores, linhaQuantidade, linhaPreco, botaoAdicionar);
  card.append(foto, corpo);
  return card;
}

async function alternarFavorito(produtoId, botao) {
  const estaFavoritado = botao.dataset.favoritado === "true";
  try {
    if (estaFavoritado) {
      await requisitarApi(`/favoritos/${produtoId}`, { method: "DELETE" });
    } else {
      await requisitarApi("/favoritos", {
        method: "POST",
        body: JSON.stringify({ produto_id: produtoId }),
      });
    }
    botao.dataset.favoritado = String(!estaFavoritado);
    botao.textContent = !estaFavoritado ? "♥" : "♡";
  } catch (erro) {
    // Mantém o estado anterior caso a requisição falhe.
  }
}

function corParaCss(nomeCor) {
  const mapaCores = {
    branca: "#F4F1E8",
    preta: "#15171B",
    cinza: "#9AA3AC",
    azul: "#3D6FB4",
    verde: "#3B6650",
  };
  return mapaCores[nomeCor.toLowerCase()] || "#CCCCCC";
}

function exibirMensagemCep(texto, tipo) {
  const elemento = document.getElementById("mensagem-cep-catalogo");
  elemento.textContent = texto;
  elemento.className = `mensagem ${tipo}`;
}

async function calcularFreteNoCatalogo() {
  const campoCep = document.getElementById("campo-cep-catalogo");
  const cep = campoCep.value.trim();
  if (!cep) return;

  const caixaEndereco = document.getElementById("caixa-endereco-catalogo");
  caixaEndereco.classList.remove("visivel");

  const [frete, endereco] = await Promise.allSettled([
    requisitarApi(`/frete/${encodeURIComponent(cep)}`),
    requisitarApi(`/endereco/${encodeURIComponent(cep)}`),
  ]);

  if (frete.status === "fulfilled") {
    localStorage.setItem("lojaUfgUltimoCep", cep);
    exibirMensagemCep(
      `Frete para ${frete.value.cep}: ${formatarMoeda(frete.value.valor_frete)} · Prazo: ${frete.value.prazo_dias} dia(s)`,
      "sucesso"
    );
  } else {
    exibirMensagemCep(frete.reason.message, "erro");
  }

  if (endereco.status === "fulfilled") {
    const dados = endereco.value;
    caixaEndereco.textContent = `${dados.logradouro ? dados.logradouro + ", " : ""}${dados.bairro ? dados.bairro + " — " : ""}${dados.cidade}/${dados.estado}`;
    caixaEndereco.classList.remove("erro");
    caixaEndereco.classList.add("visivel");
  } else {
    caixaEndereco.textContent = endereco.reason.message;
    caixaEndereco.classList.add("visivel", "erro");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarCatalogo();

  const campoCep = document.getElementById("campo-cep-catalogo");
  const cepSalvo = localStorage.getItem("lojaUfgUltimoCep");
  if (campoCep && cepSalvo) {
    campoCep.value = cepSalvo;
  }
  document.getElementById("botao-cep-catalogo").addEventListener("click", calcularFreteNoCatalogo);
});
