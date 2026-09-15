/**
 * Renderiza a página de produtos favoritados.
 */

async function carregarFavoritos() {
  const grade = document.getElementById("grade-favoritos");

  try {
    const favoritos = await requisitarApi("/favoritos");

    if (favoritos.length === 0) {
      grade.innerHTML = '<p class="vazio">Você ainda não favoritou nenhum produto.</p>';
      return;
    }

    grade.innerHTML = "";
    favoritos.forEach((produto) => grade.appendChild(criarCardFavorito(produto)));
  } catch (erro) {
    grade.innerHTML = `<p>Não foi possível carregar os favoritos: ${erro.message}</p>`;
  }
}

function criarCardFavorito(produto) {
  const card = document.createElement("article");
  card.className = "card";
  const primeiraCor = produto.cores[0];

  const foto = document.createElement("div");
  foto.className = "foto";
  const imagem = document.createElement("img");
  imagem.src = primeiraCor.url_imagem;
  imagem.alt = produto.nome;
  foto.appendChild(imagem);

  const corpo = document.createElement("div");
  corpo.className = "card-corpo";

  const titulo = document.createElement("h3");
  titulo.textContent = produto.nome;

  const linhaPreco = document.createElement("div");
  linhaPreco.className = "preco-linha";
  const preco = document.createElement("span");
  preco.className = "preco";
  preco.textContent = formatarMoeda(produto.preco);
  linhaPreco.appendChild(preco);

  const botaoRemover = document.createElement("button");
  botaoRemover.className = "add-btn";
  botaoRemover.type = "button";
  botaoRemover.textContent = "Remover dos favoritos";
  botaoRemover.addEventListener("click", async () => {
    await requisitarApi(`/favoritos/${produto.id}`, { method: "DELETE" });
    card.remove();
    const grade = document.getElementById("grade-favoritos");
    if (!grade.querySelector(".card")) {
      grade.innerHTML = '<p class="vazio">Você ainda não favoritou nenhum produto.</p>';
    }
  });

  corpo.append(titulo, linhaPreco, botaoRemover);
  card.append(foto, corpo);
  return card;
}

document.addEventListener("DOMContentLoaded", carregarFavoritos);
