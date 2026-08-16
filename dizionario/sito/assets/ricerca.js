/*
  La ricerca del dizionario.

  Non scarica nessun indice e non chiama nessun servizio: le chiavi di
  ricerca sono gia' nel documento, in data-testo, gia' senza accenti.
  Sessanta voci stanno in una pagina, e una ricerca che filtra il DOM
  non ha modo di rompersi per una fetch andata male su un hosting
  condiviso.

  Sulle pagine senza elementi filtrabili il modulo resta un GET verso
  l'indice, che filtra leggendo ?q=.
*/

(function () {
  "use strict";

  var campo = document.getElementById("q");
  var filtrabili = Array.prototype.slice.call(
    document.querySelectorAll(".filtrabile"));
  var esito = document.querySelector(".esito");
  if (!campo || !filtrabili.length) return;

  var contenitori = Array.prototype.slice.call(
    document.querySelectorAll(".contenitore"));

  function ripulisci(t) {
    return t.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }

  function filtra(chiave) {
    var q = ripulisci(chiave.trim());
    var parole = q ? q.split(/\s+/) : [];
    var visti = 0;

    filtrabili.forEach(function (el) {
      var testo = el.getAttribute("data-testo") || "";
      var ok = parole.every(function (p) { return testo.indexOf(p) !== -1; });
      el.hidden = !ok;
      if (ok) visti++;
    });

    // Un gruppo senza voci superstiti sparisce con la sua intestazione,
    // altrimenti la pagina si riempie di titoli che non hanno sotto nulla.
    contenitori.forEach(function (c) {
      var vivi = c.querySelectorAll(".filtrabile:not([hidden])").length;
      var sezione = c.closest("section") || c;
      sezione.hidden = vivi === 0;
    });

    if (!esito) return;
    if (!parole.length) {
      esito.hidden = true;
      esito.textContent = "";
    } else {
      esito.hidden = false;
      esito.textContent = visti === 0
        ? 'Nessuna voce per "' + chiave.trim() + '". '
          + "Il dizionario è di sessanta voci: se il termine manca, si "
          + "propone con una pull request."
        : visti + (visti === 1 ? " voce" : " voci") + ' per "'
          + chiave.trim() + '".';
    }
  }

  var iniziale = new URLSearchParams(location.search).get("q");
  if (iniziale) {
    campo.value = iniziale;
    filtra(iniziale);
  }

  campo.addEventListener("input", function () { filtra(campo.value); });

  campo.form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    filtra(campo.value);
  });

  // La barra si raggiunge da tastiera senza toccare il mouse.
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "/" || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var dove = document.activeElement;
    if (dove && /^(INPUT|TEXTAREA|SELECT)$/.test(dove.tagName)) return;
    ev.preventDefault();
    campo.focus();
    campo.select();
  });
})();
