/* Galeria + lightbox das paginas de vitrine (Enseada / Lagoa).
   As fotos sao declaradas em cada pagina na constante FOTOS, so DEPOIS da
   catalogacao manual (tools/folha_de_contato.py -> catalogo.csv).
   Nada e pre-carregado: o lightbox so busca a imagem cheia quando abre. */
(function () {
  "use strict";

  var grade = document.querySelector("[data-galeria]");
  if (!grade) return;

  var fotos = window.FOTOS || [];

  if (!fotos.length) {
    grade.innerHTML =
      '<p class="galeria-vazia">Galeria aguardando catalogacao das fotos. ' +
      "Rode <code>tools/folha_de_contato.py</code>, confirme a area de cada " +
      "foto e preencha a constante <code>FOTOS</code> nesta pagina.</p>";
    return;
  }

  // --- Cards -------------------------------------------------------------
  fotos.forEach(function (foto, i) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "galeria-item";
    b.setAttribute("aria-label", "Ampliar: " + foto.alt);
    b.dataset.indice = i;
    b.innerHTML =
      '<img src="' + foto.thumb + '" alt="' + foto.alt + '" loading="lazy" decoding="async">' +
      (foto.legenda ? '<span class="galeria-legenda">' + foto.legenda + "</span>" : "");
    grade.appendChild(b);
  });

  // --- Lightbox ----------------------------------------------------------
  var atual = 0;
  var caixa = document.createElement("div");
  caixa.className = "lightbox";
  caixa.setAttribute("role", "dialog");
  caixa.setAttribute("aria-modal", "true");
  caixa.hidden = true;
  caixa.innerHTML =
    '<button class="lb-fechar" type="button" aria-label="Fechar">&times;</button>' +
    '<button class="lb-nav lb-anterior" type="button" aria-label="Anterior">&#8249;</button>' +
    '<figure class="lb-palco"><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-nav lb-proxima" type="button" aria-label="Proxima">&#8250;</button>';
  document.body.appendChild(caixa);

  var img = caixa.querySelector("img");
  var legenda = caixa.querySelector("figcaption");
  var abridor = null;

  function mostrar(i) {
    atual = (i + fotos.length) % fotos.length;
    var foto = fotos[atual];
    img.src = foto.full;
    img.alt = foto.alt;
    legenda.textContent = foto.legenda || "";
    legenda.hidden = !foto.legenda;
  }

  function abrir(i) {
    abridor = document.activeElement;
    mostrar(i);
    caixa.hidden = false;
    document.body.style.overflow = "hidden";
    caixa.querySelector(".lb-fechar").focus();
  }

  function fechar() {
    caixa.hidden = true;
    img.src = "";
    document.body.style.overflow = "";
    if (abridor) abridor.focus();
  }

  grade.addEventListener("click", function (e) {
    var item = e.target.closest(".galeria-item");
    if (item) abrir(Number(item.dataset.indice));
  });

  caixa.addEventListener("click", function (e) {
    if (e.target.closest(".lb-fechar") || e.target === caixa) return fechar();
    if (e.target.closest(".lb-anterior")) return mostrar(atual - 1);
    if (e.target.closest(".lb-proxima")) return mostrar(atual + 1);
  });

  document.addEventListener("keydown", function (e) {
    if (caixa.hidden) return;
    if (e.key === "Escape") fechar();
    if (e.key === "ArrowLeft") mostrar(atual - 1);
    if (e.key === "ArrowRight") mostrar(atual + 1);
  });
})();
