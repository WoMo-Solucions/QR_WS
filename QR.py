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
    <meta charset="UTF-8">
    <title>WoMo Soluciónˢ</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 30px 10px;
            background: #ffffff;
            color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        img.logo {
            width: 80px;
            max-width: 40%;
            margin-bottom: 20px;
        }
        .contenido {
            text-align: center;
            max-width: 480px;
        }
        .datos {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        table {
            border-collapse: collapse;
            line-height: 1.3;
        }
        td {
            padding: 4px 10px;
            vertical-align: top;
            text-align: left;
        }
        td.icono {
            font-size: 18px;
            padding-right: 10px;
            text-align: right;
        }
        .nota {
            text-align: justify;
            font-size: 14px;
            padding: 0 10px;
        }
        @media screen and (max-width: 600px) {
            td {
                font-size: 15px;
            }
            .nota {
                font-size: 13px;
            }
        }
    </style>
</head>
<body>
    <div class="contenido">
        <img src="logo.png" alt="Logotipo WoMo" class="logo">
        <div class="datos">
            <table style="border-spacing: 0; line-height: 1.2;">
                <tr><td class="icono">🏢</td><td><strong style="font-size: 18px;">WoMo Soluciónˢ</strong></td></tr>
                <tr><td class="icono">🌐</td><td><a href="https://ramiju81.github.io/WoMo_Solucions/" target="_blank">Portafolio</a></td></tr>
 <tr><td class="icono">🔗</td><td><a href="https://www.linkedin.com/company/womo-solucions/" target="_blank" rel="noopener noreferrer">LinkedIn</a></td></tr>               <tr><td class="icono">📧</td><td><a href="mailto:womostd@gmail.com">e-mail</a></td></tr>
                <tr><td class="icono">📱</td><td><a href="https://wa.me/573180401930" target="_blank" rel="noopener noreferrer">WhatsApp</a></td></tr>
                <tr><td class="icono">🧑‍💻</td><td><strong>Julian Alberto Ramirez</strong></td></tr>
                <tr><td class="icono">💼</td><td>CTO & Desarrollador Full Stack</td></tr>
                <tr><td class="icono">📍</td><td>Cali - Colombia</td></tr>
            </table>
        </div>
        <div style="margin: 25px 0;">
            <div class="icono" style="text-align: center; font-size: 20px;">🛠️</div>
        </div>
        <div class="nota" style="font-size: 17px;">
        Soluciones digitales simples, útiles y profundamente humanas.<br> En <strong>WoMo Soluciónˢ</strong> transformamos procesos manuales en experiencias digitales reales, ágiles y automatizadas.
        </div>
    </div>
</body>
</html>"""

# 6. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")