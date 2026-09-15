/**
 * Renderiza o carrinho de compras: itens, cupom de desconto,
 * cálculo de frete/endereço por CEP e o resumo total da compra.
 */

let cupomAplicado = null; // { codigo, percentual }
let valorFrete = 0;

async function carregarCarrinho() {
  const lista = document.getElementById("lista-carrinho");
  const resumo = document.getElementById("resumo-carrinho");

  try {
    const itens = await requisitarApi("/carrinho");

    if (itens.length === 0) {
      lista.innerHTML = '<p class="vazio">Seu carrinho está vazio.</p>';
      resumo.style.display = "none";
      return;
    }

    lista.innerHTML = "";
    itens.forEach((item) => lista.appendChild(criarLinhaItem(item)));

    resumo.style.display = "flex";
    atualizarResumo(itens);
  } catch (erro) {
    lista.innerHTML = `<p>Não foi possível carregar o carrinho: ${erro.message}</p>`;
  }
}

function criarLinhaItem(item) {
  const linha = document.createElement("div");
  linha.className = "item-carrinho";

  const imagem = document.createElement("img");
  imagem.alt = item.nome_produto;
  imagem.src = "";
  buscarImagemDoItem(item).then((url) => { imagem.src = url; });

  const info = document.createElement("div");
  info.className = "item-info";
  const titulo = document.createElement("h3");
  titulo.textContent = item.nome_produto;
  const detalhe = document.createElement("span");
  detalhe.textContent = `Cor: ${item.nome_cor} · ${formatarMoeda(item.preco_unitario)} cada`;
  info.append(titulo, detalhe);

  const linhaQuantidade = document.createElement("div");
  linhaQuantidade.className = "qtd-linha";
  const botaoMenos = document.createElement("button");
  botaoMenos.type = "button";
  botaoMenos.className = "qtd-btn";
  botaoMenos.textContent = "−";
  const valorQuantidade = document.createElement("span");
  valorQuantidade.className = "qtd-valor";
  valorQuantidade.textContent = item.quantidade;
  const botaoMais = document.createElement("button");
  botaoMais.type = "button";
  botaoMais.className = "qtd-btn";
  botaoMais.textContent = "+";

  botaoMenos.addEventListener("click", async () => {
    if (item.quantidade <= 1) return;
    await alterarQuantidade(item.id, item.quantidade - 1);
  });
  botaoMais.addEventListener("click", async () => {
    await alterarQuantidade(item.id, item.quantidade + 1);
  });
  linhaQuantidade.append(botaoMenos, valorQuantidade, botaoMais);

  const botaoRemover = document.createElement("button");
  botaoRemover.className = "item-remover";
  botaoRemover.type = "button";
  botaoRemover.textContent = "Remover";
  botaoRemover.addEventListener("click", async () => {
    await requisitarApi(`/carrinho/${item.id}`, { method: "DELETE" });
    await atualizarBadgeCarrinho();
    await carregarCarrinho();
  });

  linha.append(imagem, info, linhaQuantidade, botaoRemover);
  return linha;
}

async function buscarImagemDoItem(item) {
  try {
    const produto = await requisitarApi(`/produtos/${item.produto_id}`);
    const cor = produto.cores.find((c) => c.nome_cor === item.nome_cor);
    return cor ? cor.url_imagem : produto.cores[0].url_imagem;
  } catch (erro) {
    return "";
  }
}

async function alterarQuantidade(itemId, novaQuantidade) {
  await requisitarApi(`/carrinho/${itemId}`, {
    method: "PATCH",
    body: JSON.stringify({ quantidade: novaQuantidade }),
  });
  await atualizarBadgeCarrinho();
  await carregarCarrinho();
}

function calcularSubtotal(itens) {
  return itens.reduce((soma, item) => soma + item.subtotal, 0);
}

function calcularValorDesconto(subtotal) {
  if (!cupomAplicado) return 0;
  return Math.round(subtotal * (cupomAplicado.percentual / 100) * 100) / 100;
}

function atualizarResumo(itens) {
  const subtotal = calcularSubtotal(itens);
  const valorDesconto = calcularValorDesconto(subtotal);
  document.getElementById("resumo-subtotal").textContent = formatarMoeda(subtotal);

  const linhaDesconto = document.getElementById("linha-desconto");
  if (valorDesconto > 0) {
    linhaDesconto.style.display = "flex";
    document.getElementById("desconto-label").textContent = `Desconto (${cupomAplicado.codigo})`;
    document.getElementById("resumo-desconto").textContent = `- ${formatarMoeda(valorDesconto)}`;
  } else {
    linhaDesconto.style.display = "none";
  }

  const linhaFrete = document.getElementById("linha-frete");
  if (valorFrete > 0) {
    linhaFrete.style.display = "flex";
    document.getElementById("resumo-frete").textContent = formatarMoeda(valorFrete);
  } else {
    linhaFrete.style.display = "none";
  }

  const total = subtotal - valorDesconto + valorFrete;
  document.getElementById("resumo-total").textContent = formatarMoeda(total);
}

function exibirMensagem(elementoId, texto, tipo) {
  const elemento = document.getElementById(elementoId);
  elemento.textContent = texto;
  elemento.className = `mensagem ${tipo}`;
}

async function aplicarCupom() {
  const campoCupom = document.getElementById("campo-cupom");
  const codigo = campoCupom.value.trim();
  if (!codigo) return;

  try {
    const itens = await requisitarApi("/carrinho");
    const subtotal = calcularSubtotal(itens);
    const resultado = await requisitarApi("/cupom/aplicar", {
      method: "POST",
      body: JSON.stringify({ codigo, valor_total: subtotal }),
    });
    cupomAplicado = { codigo: resultado.codigo, percentual: resultado.percentual_desconto };
    exibirMensagem("mensagem-cupom", `Cupom aplicado: -${resultado.percentual_desconto}%`, "sucesso");
    atualizarResumo(itens);
  } catch (erro) {
    exibirMensagem("mensagem-cupom", erro.message, "erro");
  }
}

async function calcularFreteECep() {
  const campoCep = document.getElementById("campo-cep");
  const cep = campoCep.value.trim();
  if (!cep) return;

  const caixaEndereco = document.getElementById("caixa-endereco");
  caixaEndereco.classList.remove("visivel", "erro");
  exibirMensagem("mensagem-cep", "", "");

  try {
    const endereco = await requisitarApi(`/endereco/${encodeURIComponent(cep)}`);
    caixaEndereco.textContent = `${endereco.logradouro ? endereco.logradouro + ", " : ""}${endereco.bairro ? endereco.bairro + " — " : ""}${endereco.cidade}/${endereco.estado}`;
    caixaEndereco.classList.add("visivel");
    localStorage.setItem("lojaUfgUltimoCep", cep);

    try {
      const frete = await requisitarApi(`/frete/${encodeURIComponent(cep)}`);
      valorFrete = frete.valor_frete;
      exibirMensagem(
        "mensagem-cep",
        `Frete: ${formatarMoeda(frete.valor_frete)} · Prazo: ${frete.prazo_dias} dia(s)`,
        "sucesso"
      );
      const itens = await requisitarApi("/carrinho");
      atualizarResumo(itens);
    } catch (erroFrete) {
      exibirMensagem("mensagem-cep", erroFrete.message, "erro");
    }
  } catch (erroEndereco) {
    caixaEndereco.textContent = erroEndereco.message;
    caixaEndereco.classList.add("visivel", "erro");
    valorFrete = 0;
    const itens = await requisitarApi("/carrinho");
    atualizarResumo(itens);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarCarrinho();

  const campoCep = document.getElementById("campo-cep");
  const cepSalvo = localStorage.getItem("lojaUfgUltimoCep");
  if (cepSalvo) {
    campoCep.value = cepSalvo;
  }

  document.getElementById("botao-cupom").addEventListener("click", aplicarCupom);
  document.getElementById("botao-cep").addEventListener("click", calcularFreteECep);
});
