// statics/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  const vcfUrl = "./statics/womo.vcf";

  // --- Verificar CSS ---
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
      // Lecturas robustas (línea completa, multilínea)
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

      // --- Rellenar HTML ---
      selText(".nombre", nombre);
      selText(".empresa", empresa);
      selText(".cargo", cargo);
      selText(".ubicacion", ubicacion);

      // Enlaces
      setHref(".whatsapp",  urls.find(u => u.includes("wa.me")));
      setHref(".linkedin",  urls.find(u => u.includes("linkedin")));
      setHref(".email",     email ? ("mailto:" + email) : "");

      // Portafolio: **PRIORIDAD PORTIFY**, luego fallback (opcional)
      const portifyRegex = /portify-[^/]+\.onrender\.com\/public\/index\.html/i;
      const portfolioUrl = urls.find(u => portifyRegex.test(u))
                          || urls.find(u => u.includes("womo-solucions.github.io"))
                          || urls.find(u => u.toLowerCase().includes("womo"));
      setHref(".portfolio", portfolioUrl);

      // GitHub: si no viene en VCF, usa fallback oficial
      const githubUrl = urls.find(u => u.includes("github.com")) 
                     || "https://github.com/orgs/WoMo-Solucions";
      setHref(".github", githubUrl);

      // Mensaje (respetar \n del VCF)
      const mensajeEl = document.querySelector(".mensaje");
      if (mensajeEl) mensajeEl.innerHTML = (nota || "").replace(/\\n/g, "<br>");

      // Certificado profesional (sin texto quemado)
      const credEl = document.getElementById("credencial");
      if (credEl && cred) {
        credEl.querySelector("span").textContent = cred;
        credEl.hidden = false;
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
    .catch(err => console.error("Error cargando VCF:", err));
});

// Helpers
function setHref(selector, href) {
  const el = document.querySelector(selector);
  if (!el) return;
  el.href = (href && href.trim()) ? href : "#";
}
function selText(selector, text) {
  const el = document.querySelector(selector);
  if (el) el.textContent = text || "";
}
