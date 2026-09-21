/* Formulario de cadastro para novidades dos proximos empreendimentos.

   O destino e definido em window.CADASTRO_ENDPOINT, no HTML. Enquanto
   estiver vazio o formulario recusa o envio com uma mensagem clara, em vez
   de fingir sucesso e perder o cadastro — e tools/checar_pendencias.sh
   bloqueia a publicacao. */
(function () {
  "use strict";

  var form = document.querySelector("[data-cadastro]");
  if (!form) return;

  var estado = form.querySelector(".cadastro-estado");
  var botao = form.querySelector('button[type="submit"]');
  var consentimento = form.querySelector(".consentimento");
  var textoBotao = botao ? botao.textContent : "";

  function avisar(texto, tipo) {
    estado.textContent = texto;
    estado.setAttribute("data-tipo", tipo);
  }

  function marcar(campo, invalido) {
    campo.setAttribute("aria-invalid", invalido ? "true" : "false");
  }

  // Deliberadamente permissivo: a validacao de formato so pega erro de
  // digitacao obvio. Quem valida e-mail de verdade e o e-mail de confirmacao.
  function emailPlausivel(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  }

  function validar() {
    var ok = true;
    var nome = form.elements.nome;
    var email = form.elements.email;
    var aceite = form.elements.aceite;

    var nomeOk = nome.value.trim().length >= 2;
    marcar(nome, !nomeOk);
    ok = ok && nomeOk;

    var emailOk = emailPlausivel(email.value.trim());
    marcar(email, !emailOk);
    ok = ok && emailOk;

    consentimento.setAttribute("data-invalido", aceite.checked ? "false" : "true");
    ok = ok && aceite.checked;

    return ok;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    avisar("", "");

    // Robo preencheu o campo escondido: responde como sucesso e nao envia.
    if (form.elements.site && form.elements.site.value) {
      avisar("Cadastro recebido. Obrigado!", "ok");
      form.reset();
      return;
    }

    if (!validar()) {
      avisar("Confira os campos destacados.", "erro");
      var primeiro = form.querySelector('[aria-invalid="true"]');
      if (primeiro) primeiro.focus();
      return;
    }

    var destino = window.CADASTRO_ENDPOINT;
    if (!destino) {
      avisar("Formulário ainda não configurado. Nenhum dado foi enviado.", "erro");
      return;
    }

    botao.disabled = true;
    botao.textContent = "Enviando...";
    avisar("", "");

    var dados = new FormData(form);
    dados.delete("site");
    dados.append("origem", "site institucional PRIMOR");

    fetch(destino, { method: "POST", body: dados, headers: { Accept: "application/json" } })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        form.reset();
        consentimento.setAttribute("data-invalido", "false");
        avisar("Cadastro recebido. Você será avisado sobre os próximos empreendimentos.", "ok");
      })
      .catch(function () {
        avisar("Não foi possível enviar agora. Tente novamente em instantes.", "erro");
      })
      .finally(function () {
        botao.disabled = false;
        botao.textContent = textoBotao;
      });
  });

  // Tira o destaque de erro assim que a pessoa corrige.
  form.addEventListener("input", function (e) {
    if (e.target.getAttribute("aria-invalid") === "true") marcar(e.target, false);
    if (e.target.name === "aceite" && e.target.checked) {
      consentimento.setAttribute("data-invalido", "false");
    }
  });
})();
