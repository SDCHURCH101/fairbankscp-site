/* Fairbanks Commercial Properties — original site script, 2026 */
(function () {
  "use strict";

  /* ---- theme ---------------------------------------------------------- */
  var KEY = "fcp-theme";
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(t) {
    if (t) document.documentElement.setAttribute("data-theme", t);
    else document.documentElement.removeAttribute("data-theme");
  }
  apply(stored());
  function current() {
    var s = stored();
    if (s) return s;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-theme-toggle]");
    if (!b) return;
    var next = current() === "dark" ? "light" : "dark";
    apply(next);
    try { localStorage.setItem(KEY, next); } catch (err) {}
    label();
  });
  function label() {
    var t = current() === "dark" ? "Light mode" : "Dark mode";
    Array.prototype.forEach.call(document.querySelectorAll("[data-theme-toggle]"), function (b) { b.textContent = t; });
  }

  /* ---- mobile nav ------------------------------------------------------ */
  function nav() {
    var b = document.querySelector(".burger"), n = document.getElementById("nav");
    if (!b || !n) return;
    b.addEventListener("click", function () {
      var open = n.classList.toggle("open");
      b.setAttribute("aria-expanded", open ? "true" : "false");
    });
    n.addEventListener("click", function (e) { if (e.target.tagName === "A") { n.classList.remove("open"); b.setAttribute("aria-expanded", "false"); } });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && n.classList.contains("open")) { n.classList.remove("open"); b.setAttribute("aria-expanded", "false"); b.focus(); }
    });
  }

  /* ---- availability filters -------------------------------------------- */
  function filters() {
    var root = document.getElementById("filters");
    if (!root) return;
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-space]"));
    var out = document.getElementById("fcount"), empty = document.getElementById("fempty");
    var state = { group: "all" };

    function run() {
      var n = 0;
      cards.forEach(function (c) {
        var ok = state.group === "all" || c.getAttribute("data-group") === state.group;
        c.hidden = !ok;
        if (ok) n++;
      });
      if (out) out.textContent = n + (n === 1 ? " space" : " spaces");
      if (empty) empty.hidden = n !== 0;
      try {
        var u = new URL(window.location.href);
        if (state.group === "all") u.searchParams.delete("type"); else u.searchParams.set("type", state.group);
        history.replaceState(null, "", u);
      } catch (e) {}
    }
    root.addEventListener("click", function (e) {
      var c = e.target.closest(".chip");
      if (!c) return;
      state.group = c.getAttribute("data-group");
      Array.prototype.forEach.call(root.querySelectorAll(".chip"), function (x) {
        x.setAttribute("aria-pressed", x === c ? "true" : "false");
      });
      run();
    });
    try {
      var pre = new URL(window.location.href).searchParams.get("type");
      if (pre) {
        var hit = root.querySelector('.chip[data-group="' + CSS.escape(pre) + '"]');
        if (hit) hit.click(); else run();
      } else run();
    } catch (e) { run(); }
  }

  /* ---- gallery lightbox ------------------------------------------------- */
  function lightbox() {
    var gal = document.querySelector("[data-gallery]");
    if (!gal) return;
    var shots = Array.prototype.slice.call(gal.querySelectorAll("button[data-full]"));
    if (!shots.length) return;
    var i = 0, last = null;
    var box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Photo viewer");
    box.innerHTML =
      '<button class="lb__x" aria-label="Close">&times;</button>' +
      '<button class="lb__nav p" aria-label="Previous">&#8249;</button>' +
      '<button class="lb__nav n" aria-label="Next">&#8250;</button>' +
      '<img alt=""><p class="lb__cap"></p>';
    document.body.appendChild(box);
    var img = box.querySelector("img"), cap = box.querySelector(".lb__cap");

    function show(k) {
      i = (k + shots.length) % shots.length;
      var b = shots[i];
      img.src = b.getAttribute("data-full");
      img.alt = b.getAttribute("data-alt") || "";
      cap.textContent = (i + 1) + " of " + shots.length + ". " + (b.getAttribute("data-alt") || "");
    }
    function open(k) {
      last = document.activeElement;
      show(k);
      box.classList.add("open");
      document.body.style.overflow = "hidden";
      box.querySelector(".lb__x").focus();
    }
    function close() {
      box.classList.remove("open");
      document.body.style.overflow = "";
      if (last && last.focus) last.focus();
    }
    shots.forEach(function (b, k) { b.addEventListener("click", function () { open(k); }); });
    box.querySelector(".lb__x").addEventListener("click", close);
    box.querySelector(".lb__nav.p").addEventListener("click", function () { show(i - 1); });
    box.querySelector(".lb__nav.n").addEventListener("click", function () { show(i + 1); });
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    document.addEventListener("keydown", function (e) {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(i - 1);
      else if (e.key === "ArrowRight") show(i + 1);
    });
  }

  /* ---- year ------------------------------------------------------------- */
  function year() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (e) {
      e.textContent = new Date().getFullYear();
    });
  }

  function init() { label(); nav(); filters(); lightbox(); year(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
