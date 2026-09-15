/**
 * Funções auxiliares para comunicação com a API da Loja UFG.
 */

const URL_BASE_API = "/api";

async function requisitarApi(caminho, opcoes = {}) {
  const resposta = await fetch(`${URL_BASE_API}${caminho}`, {
    headers: { "Content-Type": "application/json" },
    ...opcoes,
  });

  if (resposta.status === 204) {
    return null;
  }

  const dados = await resposta.json().catch(() => null);

  if (!resposta.ok) {
    const mensagem = dados && dados.detail ? dados.detail : "Erro ao comunicar com o servidor";
    throw new Error(mensagem);
  }

  return dados;
}

function formatarMoeda(valor) {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

async function atualizarBadgeCarrinho() {
  const elementoBadge = document.getElementById("badge-carrinho");
  if (!elementoBadge) return;

  try {
    const itens = await requisitarApi("/carrinho");
    const totalItens = itens.reduce((soma, item) => soma + item.quantidade, 0);
    elementoBadge.textContent = totalItens;
  } catch (erro) {
    elementoBadge.textContent = "0";
  }
}

/**
 * Insere a barra de letreiro com os cupons de desconto disponíveis
 * no topo de todas as páginas do site.
 */
function inserirLetreiroCupons() {
  const mensagem = "Use o cupom BEMVINDO10 e ganhe 10% de desconto no carrinho — ou PRIMEIRACOMPRA20 para 20% off.";

  const barra = document.createElement("div");
  barra.className = "letreiro-barra";
  barra.setAttribute("role", "status");

  const conteudo = document.createElement("div");
  conteudo.className = "letreiro-conteudo";
  conteudo.innerHTML = `<span>🎟️ ${mensagem}</span><span>🎟️ ${mensagem}</span>`;

  barra.appendChild(conteudo);
  document.body.insertBefore(barra, document.body.firstChild);
}

document.addEventListener("DOMContentLoaded", () => {
  atualizarBadgeCarrinho();
  inserirLetreiroCupons();
});
