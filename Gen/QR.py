import qrcode
from PIL import Image

# Configuración
qr_data = "https://ramiju81.github.io/QR_WS/"
qr_logo_path = "logo.png"
qr_output_path = "qr_womo.png"
html_output_path = "index.html"

# 1. Generar el código QR
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# 2. Procesar el logo con fondo blanco moderado
logo_size = 80  # Tamaño del logo
logo = Image.open(qr_logo_path).convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Crear fondo blanco (solo 10px más grande en cada lado)
bg_size = (logo_size + 20, logo_size + 20)
background = Image.new("RGBA", bg_size, "white")

# Pegar el logo centrado en el fondo
logo_pos = (
    (bg_size[0] - logo_size) // 2,
    (bg_size[1] - logo_size) // 2
)
background.paste(logo, logo_pos, logo)

# 3. Pegar en el QR
qr_pos = (
    (qr_img.size[0] - bg_size[0]) // 2,
    (qr_img.size[1] - bg_size[1]) // 2
)
qr_img.paste(background, qr_pos, background)

# 4. Guardar QR
qr_img.save(qr_output_path)

# 5. HTML ORIGINAL COMPLETO (sin modificaciones)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WoMo Soluciónˢ | VCard Profesional</title>
  <link rel="stylesheet" href="statics/css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Libre+Baskerville:wght@700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <div class="vcard">
    <!-- Fondo degradado ámbar -->
    <div class="amber-fade"></div>
    
    <!-- Fondo de imagen -->
    <div class="bg-pattern"></div>
    
    <!-- Franja lateral izquierda -->
    <div class="edge-stripe"></div>

    <!-- Contenido principal -->
    <div class="content">
      <div class="logo">
        <img src="statics/img/Logo.png" alt="WoMo Logo">
      </div>

      <h2 class="empresa">WoMo Soluciónˢ</h2>      
      <h1 class="nombre">Julián Alberto Ramírez</h1>
      <p class="cargo">CTO & Full Stack Developer</p>
      <p class="ubicacion">Cali – Colombia</p>

      <div class="action-buttons">
        <a href="https://wa.me/573180401930" class="btn-icon whatsapp" title="WhatsApp">
          <i class="fab fa-whatsapp"></i>
        </a>
        <a href="https://www.linkedin.com/company/womo-solucions/" class="btn-icon linkedin" title="LinkedIn">
          <i class="fab fa-linkedin-in"></i>
        </a>
        <a href="mailto:womostd@gmail.com" class="btn-icon email" title="Email">
          <i class="fas fa-envelope"></i>
        </a>
        <a href="https://ramiju81.github.io/WoMo_Solucions/" class="btn-icon portfolio" title="Portafolio">
          <i class="fas fa-globe"></i>
        </a>
      </div>

      <div class="mensaje-box">
        <div class="mensaje">
          <p>Creamos soluciones digitales simples, útiles y profundamente humanas. <br>
            Transformamos lo manual en digital.</p>
            
          <strong>Es nuestra esencia.</strong>         
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 6. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")