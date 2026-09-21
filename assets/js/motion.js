/* Movimento do site: entrada no scroll e header que encolhe.
   A classe .motion no <html> e posta por um script inline no <head>; este
   arquivo so age se ela existir. Sem JavaScript, a pagina fica estatica e
   inteira visivel — nunca em branco esperando um script que falhou. */
(function () {
  "use strict";

  var raiz = document.documentElement;
  if (!raiz.classList.contains("motion")) return;

  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Entrada no scroll ---------------------------------------------------
     IntersectionObserver e o sensor nativo que avisa quando um elemento
     entra na tela. A alternativa — medir a posicao de tudo a cada rolagem —
     roda na thread principal e trava o scroll.                             */
  var SELETORES = [
    ".secao .filete", ".titulo-secao", ".marco", ".card", ".depoimento",
    ".ficha > div", ".texto-institucional p", ".sobre-grid > div",
    ".galeria-item", ".cta-ilhabela h2", ".cta-ilhabela p", ".cta-ilhabela .btn",
    ".secao-cinza > .wrap > p", ".cadastro-caixa"
  ].join(",");

  var pendentes = [];

  function revelar(el, instantaneo) {
    if (instantaneo) {
      el.classList.add("instantaneo", "visivel");
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { el.classList.remove("instantaneo"); });
      });
    } else {
      el.classList.add("visivel");
    }
    var i = pendentes.indexOf(el);
    if (i >= 0) pendentes.splice(i, 1);
    if (observador) observador.unobserve(el);
  }

  var observador = null;
  if (!reduzido && "IntersectionObserver" in window) {
    observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) revelar(e.target, false);
      });
    // threshold 0: o filete tem 3px de altura e qualquer fracao dele conta.
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
  }

  /* O observador so avisa quando o estado de intersecao MUDA. Num salto —
     link de ancora, recarregar no meio da pagina, restauracao de scroll —
     o elemento vai de "abaixo da tela" direto para "acima da tela" sem
     nunca intersectar, e nenhum evento dispara: o conteudo ficaria preso
     invisivel. Esta varredura, limitada ao que ainda falta e no maximo a
     cada 250ms, cobre esse caso.                                          */
  function varrer() {
    if (!pendentes.length) return;
    var alturaTela = window.innerHeight || 0;
    pendentes.slice().forEach(function (el) {
      if (el.getBoundingClientRect().top < alturaTela) revelar(el, true);
    });
  }

  function registrar(elementos) {
    var alturaTela = window.innerHeight || 0;
    // Agrupa pelo elemento pai, nao pelo nome da classe: irmaos com classe
    // diferente — o marco em destaque da linha do tempo, por exemplo —
    // cairiam em grupos separados e entrariam fora de ordem.
    var grupos = new Map();

    Array.prototype.forEach.call(elementos, function (el) {
      if (el.dataset.revelado) return;
      el.dataset.revelado = "1";

      // Escalona os irmaos: 0, 1, 2... ate 5 (300ms).
      var pai = el.parentNode;
      var n = (grupos.get(pai) || 0) + 1;
      grupos.set(pai, n);
      el.style.setProperty("--atraso", Math.min(n - 1, 5));

      if (!observador) { revelar(el, true); return; }

      // Ja na tela ou acima dela quando a pagina abriu: aparece sem animar.
      // Animar o que ja esta visivel competiria com a pintura inicial e
      // atrasaria o LCP.
      if (el.getBoundingClientRect().top < alturaTela) { revelar(el, true); return; }

      pendentes.push(el);
      observador.observe(el);
    });
  }

  registrar(document.querySelectorAll(SELETORES));

  // A galeria e montada por galeria.js, que roda depois deste arquivo.
  document.addEventListener("galeria:pronta", function () {
    registrar(document.querySelectorAll(".galeria-item"));
  });

  /* --- Header que encolhe -------------------------------------------------- */
  var topo = document.querySelector(".topo");
  if (topo) {
    var limite = 90;
    var agendado = false;

    var ultimaVarredura = 0;

    function avaliar() {
      topo.classList.toggle("compacto", window.scrollY > limite);
      var agora = Date.now();
      if (agora - ultimaVarredura > 250) { ultimaVarredura = agora; varrer(); }
      agendado = false;
    }
    // O evento de scroll dispara muito mais que 60 vezes por segundo.
    // requestAnimationFrame agrupa tudo num unico ajuste por quadro.
    window.addEventListener("scroll", function () {
      if (agendado) return;
      agendado = true;
      requestAnimationFrame(avaliar);
    }, { passive: true });
    avaliar();
  }
})();
