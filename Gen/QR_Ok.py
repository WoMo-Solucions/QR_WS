import qrcode
from PIL import Image, ImageDraw

# ---------- CONFIG ----------
qr_data = "https://ramiju81.github.io/Vcard/"
logo_text_path = "circuito.png"  # imagen del circuito como molde
qr_logo_path = "logo.png"  # logo central en verde azulado
out_path = "QR_WSˢ.png"

box_size = 10     # tamaño en px de cada módulo
border = 4        # borde en módulos del QR

# Color verde vivo para el patrón del circuito
circuit_color = (0, 180, 70)  # Verde brillante

# Tamaño del logo central
logo_size = 80
blank_margin = 3  # espacio extra alrededor del logo

# 1) Generar QR base
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=box_size,
    border=border
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
w, h = qr_img.size

# 2) Crear máscara a partir de la imagen del circuito
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

# 3) Reservar espacio central para el logo
blank_size = logo_size + blank_margin * 2
blank_x = (w - blank_size) // 2
blank_y = (h - blank_size) // 2

mask_pixels = mask_full.load()
for yy in range(blank_y, blank_y + blank_size):
    for xx in range(blank_x, blank_x + blank_size):
        if 0 <= xx < w and 0 <= yy < h:
            mask_pixels[xx, yy] = 0

# 4) Pintar los módulos negros dentro de la máscara de color verde
colored = qr_img.copy()
px_col = colored.load()
px_mask = mask_full.load()

for y in range(h):
    for x in range(w):
        if px_mask[x, y] > 128 and px_col[x, y][0:3] == (0, 0, 0):
            px_col[x, y] = circuit_color + (255,)

# 5) Dibujar área blanca central
draw = ImageDraw.Draw(colored)
draw.rectangle([blank_x, blank_y, blank_x + blank_size - 1, blank_y + blank_size - 1],
               fill=(255, 255, 255, 255))

# 6) Pegar logo central
logo_center = Image.open(qr_logo_path).convert("RGBA")
logo_center = logo_center.resize((logo_size, logo_size), Image.LANCZOS)
logo_pos = ((w - logo_size) // 2, (h - logo_size) // 2)
colored.paste(logo_center, logo_pos, logo_center)

# 7) Guardar
colored.save(out_path)
print("✅ QR generado:", out_path)
