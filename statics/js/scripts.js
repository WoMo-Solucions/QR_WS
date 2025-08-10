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
            const urls = [...data.matchAll(/URL:(.+)/g)].map(m => m[1]);
            const ubicacion = (data.match(/ADR;TYPE=home:;;(.+?);;;;/) || [])[1] || "";
            const nota = (data.match(/NOTE:(.+)/) || [])[1] || "";

            // --- Rellenar HTML ---
            document.querySelector(".nombre").textContent = nombre;
            document.querySelector(".empresa").textContent = empresa;
            document.querySelector(".cargo").textContent = cargo;
            document.querySelector(".ubicacion").textContent = ubicacion;

            document.querySelector(".whatsapp").href = urls.find(u => u.includes("wa.me")) || "#";
            document.querySelector(".linkedin").href = urls.find(u => u.includes("linkedin")) || "#";
            document.querySelector(".email").href = "mailto:" + email;
            document.querySelector(".portfolio").href = urls.find(u => u.includes("github") || u.includes("womo")) || "#";

            document.querySelector(".mensaje").innerHTML = nota.replace(/\\n/g, "<br>");
        })
        .catch(err => console.error("Error cargando VCF:", err));

    // --- Botón Guardar Contacto ---
    const guardarBtn = document.getElementById("guardarContacto");
    if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
            e.preventDefault();

            // 🔹 Método para abrir directo el VCF
            window.location.href = vcfUrl;

            /* 🔸 Método anterior de descarga manual (comentado)
            const link = document.createElement("a");
            link.href = vcfUrl;
            link.download = "WoMo_Solucions.vcf";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            */
        });
    }
});