document.addEventListener("DOMContentLoaded", function () {
    const vcfUrl = "./statics/womo.vcf";

    // --- Verificar CSS ---
    const stylesheets = Array.from(document.styleSheets);
    if (!stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'))) {
        console.warn('El CSS no se cargó correctamente, cargando de respaldo...');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = './statics/css/styles.css';
        document.head.appendChild(link);
    }

    // --- Leer y procesar VCF ---
    fetch(vcfUrl)
        .then(response => response.text())
        .then(data => {
            const nombre = (data.match(/FN:(.+)/) || [])[1] || "";
            const empresa = (data.match(/ORG:(.+)/) || [])[1] || "";
            const cargo = (data.match(/TITLE:(.+)/) || [])[1] || "";
            const telefono = (data.match(/TEL:(.+)/) || [])[1] || "";
            const email = (data.match(/EMAIL:(.+)/) || [])[1] || "";
            const urlsRaw = [...data.matchAll(/URL:(.+)/g)].map(m => m[1]);
            const ubicacion = (data.match(/ADR;TYPE=home:;;(.+?);;;;/) || [])[1] || "";
            const nota = (data.match(/NOTE:(.+)/) || [])[1] || "";

            // Filtrar URLs para quitar mails y WhatsApp
            const urls = urlsRaw.filter(u => !u.includes("mailto:") && !u.includes("wa.me"));

            // --- Rellenar HTML ---
            document.querySelector(".nombre").textContent = nombre;
            document.querySelector(".empresa").textContent = empresa;
            document.querySelector(".cargo").textContent = cargo;
            document.querySelector(".ubicacion").textContent = ubicacion;

            document.querySelector(".whatsapp").href = urlsRaw.find(u => u.includes("wa.me")) || "#";
            document.querySelector(".email").href = "mailto:" + email;

            document.querySelector(".linkedin").href = urls.find(u => u.includes("linkedin")) || "#";
            document.querySelector(".portfolio").href = urls.find(u => u.includes("github") || u.includes("womo")) || "#";

            document.querySelector(".mensaje").innerHTML = nota.replace(/\\n/g, "<br>");
        })
        .catch(err => console.error("Error cargando VCF:", err));

    // --- Botón Guardar Contacto ---
    const guardarBtn = document.getElementById("guardarContacto");
    if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
            e.preventDefault();

            const partesNombre = nombre.trim().split(" ");
            const nombreSolo = partesNombre.slice(0, -1).join(" ");
            const apellido = partesNombre.slice(-1).join(" ");
            const nombreCompleto = `${nombreSolo} ${apellido}`.trim();

            const urlGoogleContacts = `https://contacts.google.com/new?name=${encodeURIComponent(nombreCompleto)}&email=${encodeURIComponent(email)}`;
            window.open(urlGoogleContacts, "_blank");
        });
    }
});