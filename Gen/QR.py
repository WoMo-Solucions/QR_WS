import qrcode
from PIL import Image, ImageDraw

# ---------- CONFIG ----------
qr_data = "https://ramiju81.github.io/QR_WS/"
logo_text_path = "circuito.png"  # imagen del circuito como molde
qr_logo_path = "logo.png"  # logo central en verde azulado
out_path = "QR_WSˢ.png"
html_output_path = "index.html"

box_size = 10     # tamaño en px de cada módulo
border = 4        # borde en módulos del QR

# Color verde vivo para el patrón del circuito
circuit_color = (0, 180, 70)  # Verde brillante

# Tamaño del logo central
logo_size = 80
blank_margin = 3  # espacio extra alrededor del logo

# 1. Generar QR base
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=box_size,
    border=border
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
w, h = qr_img.size

# 2. Crear máscara a partir de la imagen del circuito
logo_text = Image.open(logo_text_path).convert("RGBA")

# Usar alpha si lo hay, si no, usar luminancia
if "A" in logo_text.getbands():
    mask_src = logo_text.split()[3]
else:
    mask_src = logo_text.convert("L").point(lambda p: 255 if p < 240 else 0)

margin_px = box_size * 1
target_w = w - 1 * margin_px
target_h = h - 1 * margin_px
mask_src.thumbnail((target_w, target_h), Image.LANCZOS)


mask_src = mask_src.convert("L")
mask_src.thumbnail((target_w, target_h), Image.LANCZOS)
mask_w, mask_h = mask_src.size
mask_src = mask_src.point(lambda p: 255 if p > 128 else 0)

mask_full = Image.new("L", (w, h), 0)
pos_x = (w - mask_w) // 2
pos_y = (h - mask_h) // 2
mask_full.paste(mask_src, (pos_x, pos_y))

# 3. Reservar espacio central para el logo
blank_size = logo_size + blank_margin * 2
blank_x = (w - blank_size) // 2
blank_y = (h - blank_size) // 2

mask_pixels = mask_full.load()
for yy in range(blank_y, blank_y + blank_size):
    for xx in range(blank_x, blank_x + blank_size):
        if 0 <= xx < w and 0 <= yy < h:
            mask_pixels[xx, yy] = 0

# 4. Pintar los módulos negros dentro de la máscara de color verde
colored = qr_img.copy()
px_col = colored.load()
px_mask = mask_full.load()

for y in range(h):
    for x in range(w):
        if px_mask[x, y] > 128 and px_col[x, y][0:3] == (0, 0, 0):
            px_col[x, y] = circuit_color + (255,)

# 5. Dibujar área blanca central
draw = ImageDraw.Draw(colored)
draw.rectangle([blank_x, blank_y, blank_x + blank_size - 1, blank_y + blank_size - 1],
               fill=(255, 255, 255, 255))

# 6. Pegar logo central
logo_center = Image.open(qr_logo_path).convert("RGBA")
logo_center = logo_center.resize((logo_size, logo_size), Image.LANCZOS)
logo_pos = ((w - logo_size) // 2, (h - logo_size) // 2)
colored.paste(logo_center, logo_pos, logo_center)



# 7. HTML ORIGINAL COMPLETO (sin modificaciones)
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
    <div class="amber-fade"></div>
    <div class="bg-pattern"></div>
    <div class="edge-stripe"></div>

    <div class="content">
      <div class="logo">
        <img src="statics/img/Logo.png" alt="WoMo Logo">
      </div>

      <h2 class="empresa"></h2>      
      <h1 class="nombre"></h1>
      <p class="cargo"></p>
      <p class="ubicacion"></p>

      <div class="action-buttons">
        <a href="#" class="btn-icon whatsapp" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="#" class="btn-icon linkedin" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
        <a href="#" class="btn-icon email" title="Email"><i class="fas fa-envelope"></i></a>
        <a href="#" class="btn-icon portfolio" title="Portafolio"><i class="fas fa-globe"></i></a>
      </div>

      <!-- Mensaje -->
      <div class="mensaje-box">
        <div class="mensaje">
          <p></p>
        </div>
      </div>
        <!-- Guardar contacto -->
        <div class="guardar-contacto">
          <a href="#" id="guardarContacto" title="Guardar contacto">
            <i class="fas fa-address-book"></i>
          </a>
        </div>
    </div>
  </div>
  <script src="statics/js/scripts.js"></script>
</body>
</html>
"""

# 8. Guardar
colored.save(out_path)

# 9. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")