document.addEventListener("DOMContentLoaded", function () {
    const stylesheets = Array.from(document.styleSheets);
    const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));
    
    if (!cssLoaded) {
        console.error('El CSS no se cargó correctamente');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = './statics/css/styles.css';
        document.head.appendChild(link);
    }

    const guardarBtn = document.getElementById("guardarContacto");
    if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
            e.preventDefault();

            fetch("./statics/womo.vcf")
                .then(response => response.text())
                .then(vcfContent => {
                    const vcfDataUri = "data:text/vcard;charset=utf-8," + encodeURIComponent(vcfContent);
                    window.location.href = vcfDataUri;
                })
                .catch(error => console.error("Error cargando el VCF:", error));
        });
    }
});
