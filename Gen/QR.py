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
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>WoMo Soluciónˢ | Vcard</title>
  <link rel="stylesheet" href="statics/css/styles.css" />
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    body {
    margin: 0;
    padding: 0;
    background: #f2f2f2;
    font-family: 'Rubik', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    }

    .vcard {
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    max-width: 380px;
    width: 90%;
    padding: 30px 20px;
    text-align: center;
    }

    .logo-wrapper {
    margin-bottom: 10px;
    }

    .logo-circle {
    width: 120px;
    height: 120px;
    background: #f2f2f2;
    border-radius: 50%;
    border: 3px solid #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    }

    .logo-circle img {
    width: 90px;
    height: auto;
    object-fit: contain;
    }

    .empresa {
    font-size: 22px;
    color: #1a2a6c;
    font-weight: 800;
    margin-top: 20px;
    }

    .nombre {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    margin: 5px 0;
    }

    .cargo,
    .ubicacion {
    font-size: 14px;
    color: #666;
    margin: 2px 0;
    }

    .icon-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 30px 0;
    flex-wrap: wrap;
    }

    .icon-buttons a {
    font-size: 28px;
    text-decoration: none;
    color: #3a7bd5;
    padding: 10px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-radius: 50%;
    background: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    }

    .icon-buttons a:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }

    .mensaje {
    font-size: 15px;
    color: #333;
    text-align: justify;
    line-height: 1.6;
    padding: 0 10px;
    max-width: 280px;
    margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="vcard">
    <div class="logo-wrapper">
      <div class="logo-circle">
        <img src="statics/img/logo.png" alt="Logo WoMo" />
      </div>
    </div>

    <h1 class="empresa">WoMo Soluciónˢ</h1>
    <h2 class="nombre">Julián Alberto Ramírez</h2>
    <p class="cargo">CTO & Full Stack Developer</p>
    <p class="ubicacion">Cali - Colombia</p>

    <div class="icon-buttons">
      <a href="https://ramiju81.github.io/WoMo_Solucions/" title="Portafolio" target="_blank">🌐</a>
      <a href="https://www.linkedin.com/company/womo-solucions/" title="LinkedIn" target="_blank">🔗</a>
      <a href="mailto:womostd@gmail.com" title="Correo">✉️</a>
      <a href="https://wa.me/573180401930" title="WhatsApp" target="_blank">📱</a>
    </div>

    <p class="mensaje">
      Creamos soluciones digitales simples, útiles y profundamente humanas.<br>
      Transformamos procesos manuales en experiencias reales, vivas y automatizadas. Esa es nuestra esencia.
    </p>
  </div>
</body>
</html>"""

# 6. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")