// statics/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  // ✅ Usar el VCF que está junto a index.html
  const vcfUrl = "./womo.vcf";

  // --- Verificar CSS (sin cambios) ---
  const stylesheets = Array.from(document.styleSheets || []);
  if (!stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'))) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = './statics/css/styles.css';
    document.head.appendChild(link);
  }

  // --- Leer y procesar VCF ---
  fetch(vcfUrl)
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
      selText(".nombre", nombre);
      selText(".empresa", empresa);
      selText(".cargo", cargo);
      selText(".ubicacion", ubicacion);

      // Enlaces 1:1
      setHref(".whatsapp", urls.find(u => u.includes("wa.me")));
      setHref(".linkedin", urls.find(u => u.includes("linkedin")));
      setHref(".email",    email ? ("mailto:" + email) : "");

      // ✅ Portafolio = SOLO PortiFy. Si no está, se oculta.
      const portifyRegex = /portify-[^/]+\.onrender\.com\/public\/index\.html/i;
      const portfolioUrl = urls.find(u => portifyRegex.test(u)) || null;
      setHref(".portfolio", portfolioUrl);

      // GitHub (si existe en el VCF). Sin fallback a nada.
      const githubUrl = urls.find(u => /github\.com/i.test(u)) || null;
      setHref(".github", githubUrl);

      // Mensaje (respeta \n del VCF)
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl) mensajeEl.innerHTML = (nota || "").replace(/\\n/g, "<br>");

      // Credencial
      const credEl = document.getElementById("credencial");
      if (credEl) {
        if (cred) {
          const span = credEl.querySelector("span");
          if (span) span.textContent = cred;
          credEl.hidden = false;
        } else {
          credEl.hidden = true;
        }
      }

      // Guardar contacto
      const guardarBtn = document.getElementById("guardarContacto");
      if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
          e.preventDefault();
          const link = document.createElement("a");
          link.href = vcfUrl;
          link.download = `${(nombre || "contacto").replace(/ /g, "_")}.vcf`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
      }
    })
    .catch(err => {
      console.error("Error cargando VCF:", err);
      // Si falla, ocultar botones para no abrir enlaces erróneos
      [".whatsapp",".linkedin",".email",".portfolio",".github"].forEach(cls => setHref(cls, null));
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl) mensajeEl.textContent = 'No fue posible cargar la tarjeta de contacto.';
    });
});

// Helpers
function setHref(selector, href) {
  const el = document.querySelector(selector);
  if (!el) return;
  if (href && href.trim()) {
    el.href = href;
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