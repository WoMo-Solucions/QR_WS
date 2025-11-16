// statics/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  // Ruta real del VCF
  const vcfUrl = "./statics/womo.vcf";

  // --- Cargar CSS si no está (no interfiere con tu HTML) ---
  try {
    const stylesheets = Array.from(document.styleSheets || []);
    if (!stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'))) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = './statics/css/styles.css';
      document.head.appendChild(link);
    }
  } catch (e) {
    // Algunos navegadores bloquean acceso a document.styleSheets; no pasa nada
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

      // --- Rellenar texto (si existen esos elementos) ---
      safeSetText(".nombre",   nombre);
      safeSetText(".empresa",  empresa);
      safeSetText(".cargo",    cargo);
      safeSetText(".ubicacion", ubicacion);

      // --- Detectar enlaces por dominio (sin ocultar nada si falta) ---
      const urlWhats   = urls.find(u => /wa\.me\//i.test(u)) || null;          // https://wa.me/573...
      const urlLinked  = urls.find(u => /linkedin\.com\//i.test(u)) || null;   // LinkedIn empresa
      const urlMail    = email ? ("mailto:" + email) 
                               : (urls.find(u => /^mailto:/i.test(u)) || null);

      // Portafolio = URL de PortiFy exacta del VCF
      const portifyRegex = /portify-[^/]+\.onrender\.com\/public\/index\.html/i;
      const urlPagina    = urls.find(u => portifyRegex.test(u)) || null;

      // GitHub empresa
      const urlGithub   = urls.find(u => /github\.com\/womo-solucions/i.test(u)) 
                       || urls.find(u => /github\.com\//i.test(u)) 
                       || null;

      // ✅ Instagram (cualquier URL con instagram.com)
      const urlInstagram = urls.find(u => /instagram\.com\/womo_solucions/i.test(u)) 
                        || urls.find(u => /instagram\.com\//i.test(u)) 
                        || null;

      // --- Asignar enlaces solo si existen (no esconder botones) ---
      safeSetHref(".whatsapp",   urlWhats);
      safeSetHref(".linkedin",   urlLinked);
      safeSetHref(".email",      urlMail);
      safeSetHref(".portfolio",  urlPagina);    // 🌐 Portafolio = PortiFy
      safeSetHref(".github",     urlGithub);
      safeSetHref(".instagram",  urlInstagram); // 📷 Instagram separado

      // --- Mensaje: respeta \n del VCF ---
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl && nota) mensajeEl.innerHTML = nota.replace(/\\n/g, "<br>");

      // --- Credencial ---
      const credEl = document.getElementById("credencial");
      if (credEl) {
        const span = credEl.querySelector("span");
        if (span && cred) {
          span.textContent = cred;
          credEl.hidden = false;
        }
      }

      // --- Guardar contacto (descargar VCF en un clic) ---
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
      // Si falla, no tocamos nada: los href quedan como en el HTML
    });
});

/* ================= Helpers ================= */

// No ocultar; si existe href nuevo lo pone, si no, deja el que ya tenías
function safeSetHref(selector, href) {
  const el = document.querySelector(selector);
  if (!el || !href || !href.trim()) return;
  el.href = href.trim();
  el.target = "_blank";
  el.rel = "noopener noreferrer";
}

// No borrar contenido si falta el dato
function safeSetText(selector, text) {
  const el = document.querySelector(selector);
  if (el && text) el.textContent = text;
}
