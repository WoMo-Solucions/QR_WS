// statics/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  // ✅ El VCF está junto a index.html

  const vcfUrl = "./statics/womo.vcf";

  // --- Cargar CSS si no está (sin romper nada de tu HTML) ---
  try {
    const stylesheets = Array.from(document.styleSheets || []);
    if (!stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'))) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = './statics/css/styles.css';
      document.head.appendChild(link);
    }
  } catch (e) {
    // algunos navegadores bloquean acceso a document.styleSheets cross-origin; no es crítico
  }

  // --- Leer y procesar VCF ---
  fetch(vcfUrl, { cache: "no-store" })
    .then(response => response.text())
    .then(data => {
      const getLine = (re) => ((data.match(re) || [])[1] || "").trim();

      const nombre    = getLine(/^FN:(.*)$/m);
      const empresa   = getLine(/^ORG:(.*)$/m);
      const cargo     = getLine(/^TITLE:(.*)$/m);
      const telefono  = getLine(/^TEL:(.*)$/m);
      const email     = getLine(/^EMAIL:(.*)$/m);
      const ubicacion = getLine(/^ADR;TYPE=home:;;(.*?);;;;$/m);
      const nota      = getLine(/^NOTE:(.*)$/m);
      const cred      = (getLine(/^ROLE:(.*)$/m) || getLine(/^X-CREDENCIAL:(.*)$/m));

      const urls = Array.from(data.matchAll(/^URL:(.*)$/gm)).map(m => (m[1] || "").trim());

      // --- Rellenar texto si existen esos elementos en el DOM ---
      selText(".nombre",   nombre);
      selText(".empresa",  empresa);
      selText(".cargo",    cargo);
      selText(".ubicacion", ubicacion);

      // --- Asignar enlaces por dominio ---
      setHref(".whatsapp", urls.find(u => /wa\.me\//i.test(u)) || null);
      setHref(".linkedin", urls.find(u => /linkedin\.com\//i.test(u)) || null);
      setHref(".email",    email ? ("mailto:" + email) : (urls.find(u => /^mailto:/i.test(u)) || null));

      // ✅ Portafolio/Página: SOLO PortiFy (sin fallbacks que puedan coincidir con LinkedIn o GitHub Pages)
      const portifyRegex = /portify-[^/]+\.onrender\.com\/public\/index\.html/i;
      const portfolioUrl = urls.find(u => portifyRegex.test(u)) || null; // si no está, se oculta
      setHref(".portfolio", portfolioUrl);

      // GitHub: solo si está en el VCF (sin fallback)
      const githubUrl = urls.find(u => /github\.com/i.test(u)) || null;
      setHref(".github", githubUrl);

      // Mensaje (respetar \n del VCF)
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl) mensajeEl.innerHTML = (nota || "").replace(/\\n/g, "<br>");

      // Credencial (si existe)
      const credEl = document.getElementById("credencial");
      if (credEl) {
        const span = credEl.querySelector("span");
        if (cred && span) {
          span.textContent = cred;
          credEl.hidden = false;
        } else {
          credEl.hidden = true;
        }
      }

      // Guardar contacto (descargar el mismo VCF)
      const guardarBtn = document.getElementById("guardarContacto");
      if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
          e.preventDefault();
          const a = document.createElement("a");
          a.href = vcfUrl;
          a.download = `${(nombre || "contacto").replace(/ /g, "_")}.vcf`;
          document.body.appendChild(a);
          a.click();
          a.remove();
        });
      }
    })
    .catch(err => {
      console.error("Error cargando VCF:", err);
      // Oculta botones para evitar enlaces incorrectos
      [".whatsapp",".linkedin",".email",".portfolio",".github"].forEach(cls => setHref(cls, null));
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl) mensajeEl.textContent = 'No fue posible cargar la tarjeta de contacto.';
    });
});

// Helpers
function setHref(selector, href) {
  const el = document.querySelector(selector);
  if (!el) return;
  if (href && href.trim() && href !== "#") {
    el.href = href.trim();
    el.target = "_blank";
    el.rel = "noopener noreferrer";
    el.style.display = "";
    el.removeAttribute("hidden");
  } else {
    el.href = "#";
    el.style.display = "none";
    el.setAttribute("hidden", "hidden");
  }
}
function selText(selector, text) {
  const el = document.querySelector(selector);
  if (el) el.textContent = text || "";
}
