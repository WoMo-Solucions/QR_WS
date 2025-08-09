from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np

# --- Configuración ---
input_path = "logo.png"  # tu logo original
output_path = "logo_.png"
bevel_depth = 3          # grosor del relieve
light_dir = (0, -1)      # luz desde arriba (dx, dy)
light_intensity = 1.2    # brillo de la luz
shadow_intensity = 0.8   # oscuridad de la sombra
background_color = (255, 255, 255, 255)  # fondo blanco

# --- Abrir imagen y extraer máscara ---
logo = Image.open(input_path).convert("RGBA")
alpha = logo.split()[3]  # canal alfa como máscara

# --- Crear mapa de relieve (bump map) ---
# Invertir máscara para que el borde sea detectado mejor
mask = ImageOps.invert(alpha)
# Desenfoque gaussiano para suavizar el borde del relieve
mask_blur = mask.filter(ImageFilter.GaussianBlur(bevel_depth))

# Convertir a array numpy
mask_array = np.array(mask_blur).astype(np.float32) / 255.0

# Calcular gradiente (normal map aproximado)
gy, gx = np.gradient(mask_array)
# Invertir eje Y para simular luz real
gy = -gy

# Normalizar vectores
norm = np.sqrt(gx**2 + gy**2 + 1)
nx, ny, nz = gx / norm, gy / norm, 1.0 / norm

# Luz direccional
lx, ly = light_dir
lz = 1.0
# Normalizar luz
len_l = np.sqrt(lx**2 + ly**2 + lz**2)
lx /= len_l
ly /= len_l
lz /= len_l

# Cálculo de luz (dot product entre normal y dirección de luz)
dot = nx * lx + ny * ly + nz * lz
# Normalizar a rango 0..1
dot = (dot - dot.min()) / (dot.max() - dot.min())

# Crear capa de luz/sombra en escala de grises
light_map = (dot * 255).astype(np.uint8)
# Evitar warning eliminando parámetro 'mode' en fromarray
light_img = Image.fromarray(light_map).convert("RGBA")

# Ajustar intensidad de luz
light_img = ImageEnhance.Brightness(light_img).enhance(light_intensity)

# Invertir solo canales RGB para sombra, conservar alfa intacto
arr = np.array(light_img)
arr[..., :3] = 255 - arr[..., :3]
shadow_img = Image.fromarray(arr, mode="RGBA")

# Ajustar intensidad de sombra
shadow_img = ImageEnhance.Brightness(shadow_img).enhance(shadow_intensity)

# --- Composición final ---
# Fondo blanco
final_img = Image.new("RGBA", logo.size, background_color)
# Sombra
final_img = Image.alpha_composite(final_img, shadow_img)
# Logo original
final_img = Image.alpha_composite(final_img, logo)
# Luz
final_img = Image.alpha_composite(final_img, light_img)

# Guardar resultado
final_img.save(output_path)
print(f"✅ Logo con bevel suave guardado en: {output_path}")
