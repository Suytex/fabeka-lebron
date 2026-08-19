#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabeka Lebrón — generador de imágenes temporales de relleno.

Produce cuatro archivos en assets/img/ mientras no llegan las fotografías
oficiales. Son composiciones abstractas y texturales (degradado suave en la
paleta de marca + grano fino + una geometría muy tenue en oro). Sin rostros,
sin figuras, sin material de terceros: todo se dibuja aquí.

    assets/img/fabeka-retrato-azul.jpg    680 x 880    hero de index.html
    assets/img/fabeka-retrato-negro.jpg   680 x 880    bio de index.html
    assets/img/fabeka-escenario.jpg       840 x 1080   conferencias.html
    assets/img/og-fabeka-lebron.jpg      1200 x 630    preview en redes

Las tres verticales son variaciones de una misma familia: mismo degradado
diagonal, misma luz, mismo arco; cambia solo la clave tonal (azul luminoso,
azul-negro, escenario con luz de oro).

Uso:
    pip install Pillow
    python3 tools/gen-placeholders.py

El resultado es determinista: la misma versión del script devuelve siempre
los mismos bytes. Cuando lleguen las fotografías reales basta con sobrescribir
los .jpg (mismos nombres) y borrar este script.
"""

import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"

# ---------------------------------------------------------------- paleta
# Los tokens del sistema de diseño (:root en styles.css) y las variantes
# tonales derivadas que usan las composiciones.
INK        = (0x1c, 0x2b, 0x4a)
INK_70     = (0x45, 0x52, 0x6d)
GOLD       = (0xa9, 0x88, 0x4b)
GOLD_PALE  = (0xcb, 0xb5, 0x86)
PAPER      = (0xfd, 0xfc, 0xfa)
PAPER_2    = (0xf7, 0xf5, 0xf0)
LINE       = (0xe7, 0xe2, 0xd8)
GRAY       = (0x8a, 0x85, 0x7a)

INK_LIGHT  = (0x3a, 0x4e, 0x76)   # ink aclarado, para el extremo alto del azul
INK_DEEP   = (0x12, 0x1c, 0x33)   # ink profundo, para las sombras
NEAR_BLACK = (0x0d, 0x11, 0x1a)   # azul-negro de la variante "negro"
SLATE      = (0x2b, 0x33, 0x40)   # gris azulado de la variante "negro"

# Familias serif preferidas para la OG, en orden. Se resuelve la primera que
# exista en el sistema; Georgia es la que usa el sitio como fallback serif.
SERIF_CANDIDATES = [
    "Cormorant Garamond", "EB Garamond", "Georgia", "Times New Roman",
    "Liberation Serif", "DejaVu Serif", "FreeSerif",
]
SANS_CANDIDATES = [
    "Jost", "Futura", "Avenir Next", "Helvetica Neue",
    "Liberation Sans", "DejaVu Sans", "FreeSans",
]


# ------------------------------------------------------------ utilidades

def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(size, stops, angle_deg):
    """Degradado lineal multiparada.

    Se calcula a baja resolución y se escala con bicúbica: sale más suave
    (y muchísimo más rápido) que resolver píxel a píxel.
    """
    import math

    w, h = size
    lw, lh = 128, max(2, int(round(128 * h / w)))
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    # Proyección normalizada 0..1 sobre el eje del degradado.
    span = abs(dx) + abs(dy)
    ox = 0.5 * (1 - dx / span) if span else 0.0
    oy = 0.5 * (1 - dy / span) if span else 0.0

    small = Image.new("RGB", (lw, lh))
    px = small.load()
    positions = [s[0] for s in stops]
    colors = [s[1] for s in stops]
    for y in range(lh):
        fy = y / (lh - 1)
        for x in range(lw):
            fx = x / (lw - 1)
            t = (fx * dx + fy * dy) / span + (ox * dx + oy * dy) / span
            t = min(1.0, max(0.0, t))
            # localizar el tramo
            i = 0
            while i < len(positions) - 2 and t > positions[i + 1]:
                i += 1
            p0, p1 = positions[i], positions[i + 1]
            local = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
            local = min(1.0, max(0.0, local))
            # suavizado de la interpolación (smoothstep)
            local = local * local * (3 - 2 * local)
            px[x, y] = lerp(colors[i], colors[i + 1], local)
    return small.resize(size, Image.Resampling.BICUBIC)


def radial_mask(size, cx, cy, radius, falloff=1.6):
    """Máscara L con un halo radial suave centrado en (cx, cy) relativos."""
    w, h = size
    lw, lh = 128, max(2, int(round(128 * h / w)))
    m = Image.new("L", (lw, lh), 0)
    px = m.load()
    for y in range(lh):
        fy = y / (lh - 1)
        for x in range(lw):
            fx = x / (lw - 1)
            # distancia en el espacio del lienzo (corrigiendo la proporción)
            ddx = (fx - cx)
            ddy = (fy - cy) * (h / w)
            d = (ddx * ddx + ddy * ddy) ** 0.5
            t = max(0.0, 1.0 - d / radius)
            px[x, y] = int(round(255 * (t ** falloff)))
    return m.resize(size, Image.Resampling.BICUBIC)



def band_mask(size, angle_deg, center=0.5, width=0.22):
    """Máscara L con una franja de luz suave, en diagonal (perfil gaussiano)."""
    import math

    w, h = size
    lw, lh = 128, max(2, int(round(128 * h / w)))
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    span = abs(dx) + abs(dy)
    m = Image.new("L", (lw, lh), 0)
    px = m.load()
    for y in range(lh):
        fy = y / (lh - 1)
        for x in range(lw):
            fx = x / (lw - 1)
            t = (fx * dx + fy * dy) / span
            t = t - math.floor(t) if False else t
            v = math.exp(-(((t - center) / width) ** 2))
            px[x, y] = int(round(255 * v))
    return m.resize(size, Image.Resampling.BICUBIC)


def glow(img, color, cx, cy, radius, strength, falloff=1.6):
    """Funde una luz de color sobre la imagen usando un halo radial."""
    mask = radial_mask(img.size, cx, cy, radius, falloff)
    if strength < 1.0:
        mask = mask.point(lambda v: int(v * strength))
    layer = Image.new("RGB", img.size, color)
    return Image.composite(layer, img, mask)



def sheen(img, color, mask, strength):
    """Funde un color sobre la imagen a través de una máscara dada."""
    if strength < 1.0:
        mask = mask.point(lambda v: int(v * strength))
    layer = Image.new("RGB", img.size, color)
    return Image.composite(layer, img, mask)


def vignette(img, strength=0.35, radius=1.15):
    """Oscurece los bordes muy ligeramente, como una lente."""
    mask = radial_mask(img.size, 0.5, 0.5, radius, 1.4)
    mask = mask.point(lambda v: int(255 - (255 - v) * strength))
    black = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(img, black, mask)


def grain(img, amount=0.055, seed=0, blur=0.4):
    """Grano fino determinista. También rompe el banding del degradado."""
    w, h = img.size
    rnd = random.Random(seed)
    noise = Image.frombytes("L", (w, h), bytes(rnd.getrandbits(8) for _ in range(w * h)))
    if blur:
        noise = noise.filter(ImageFilter.GaussianBlur(blur))
    noisy = ImageChops.add(img, noise.convert("RGB"), scale=1, offset=-128)
    return Image.blend(img, noisy, amount)


def overlay(size, draw_fn, scale=2):
    """Dibuja una capa RGBA en supermuestreo y la devuelve suavizada."""
    big = Image.new("RGBA", (size[0] * scale, size[1] * scale), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(big), scale)
    return big.resize(size, Image.Resampling.LANCZOS)


def load_font(candidates, size):
    """Primera familia disponible del sistema; None si no hay ninguna."""
    from PIL import features  # noqa: F401  (fuerza el import limpio de PIL)
    for name in candidates:
        for variant in (name, name.replace(" ", "")):
            try:
                return ImageFont.truetype(variant, size)
            except OSError:
                pass
    # búsqueda por fontconfig (Linux)
    try:
        import subprocess
        for name in candidates:
            out = subprocess.run(
                ["fc-match", "-f", "%{file}\n%{family}", name],
                capture_output=True, text=True, timeout=10,
            )
            path, _, family = out.stdout.partition("\n")
            if path and name.lower() in family.lower():
                return ImageFont.truetype(path, size)
    except Exception:
        pass
    try:
        import subprocess
        out = subprocess.run(["fc-match", "-f", "%{file}", "serif"],
                             capture_output=True, text=True, timeout=10)
        if out.stdout.strip():
            return ImageFont.truetype(out.stdout.strip(), size)
    except Exception:
        pass
    return None


def tracked_text(draw, xy, text, font, fill, tracking=0, anchor_center=True):
    """Texto con letter-spacing (Pillow no lo trae de serie)."""
    glyphs = list(text)
    widths = [draw.textlength(g, font=font) for g in glyphs]
    total = sum(widths) + tracking * (len(glyphs) - 1)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for g, gw in zip(glyphs, widths):
        draw.text((x, y), g, font=font, fill=fill, anchor="ls" if False else "la")
        x += gw + tracking
    return total


def save(img, name, quality=90):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True,
                            progressive=True, subsampling=1)
    kb = path.stat().st_size / 1024
    print(f"  {name:34s} {img.size[0]:>5} x {img.size[1]:<5}  {kb:6.1f} KB")


# ------------------------------------------------------- familia vertical

def vertical(size, stops, light, seed, shaft=None, arc_alpha=62, rule_alpha=34,
             vig=0.30, grain_amount=0.055, skip_grain=False):
    """Retrato abstracto: muro en degradado, luz diagonal y un arco tenue.

    Los tres verticales comparten esta construcción —muro, luz, arco, filete—
    y solo cambian la clave tonal y la temperatura de la luz. La geometría se
    mantiene centrada y lejos de los bordes para que `object-fit: cover` pueda
    recortar sin romper la composición.
    """
    w, h = size
    img = gradient(size, stops, angle_deg=58)

    # Franja de luz cayendo en diagonal sobre el muro.
    if shaft:
        scolor, scenter, swidth, sstrength = shaft
        img = sheen(img, scolor, band_mask(size, 118, scenter, swidth), sstrength)

    # Foco suave, la fuente de esa luz.
    lcolor, lcx, lcy, lrad, lstr = light
    img = glow(img, lcolor, lcx, lcy, lrad, lstr, falloff=1.9)

    def geometry(d, s):
        # Arco de medio punto: la única figura, apenas insinuada.
        aw = w * 0.62          # ancho del vano
        left = (w - aw) / 2
        top = h * 0.30         # arranque de la curva
        line_w = max(1, int(1.6 * s))
        col = GOLD_PALE + (arc_alpha,)
        d.arc([left * s, top * s, (left + aw) * s, (top + aw) * s],
              start=180, end=360, fill=col, width=line_w)
        # Jambas hasta el pie del encuadre.
        y0 = int((top + aw / 2) * s)
        d.line([(left * s, y0), (left * s, int(h * 0.94 * s))], fill=col, width=line_w)
        d.line([((left + aw) * s, y0), ((left + aw) * s, int(h * 0.94 * s))],
               fill=col, width=line_w)
        # Filete horizontal a la altura de la línea de tierra.
        y = int(h * 0.94 * s)
        d.line([(int(w * 0.08 * s), y), (int(w * 0.92 * s), y)],
               fill=GOLD_PALE + (rule_alpha,), width=max(1, int(1.2 * s)))

    img = Image.alpha_composite(img.convert("RGBA"), overlay(size, geometry)).convert("RGB")
    img = vignette(img, strength=vig, radius=1.05)
    if skip_grain:   # el grano se aplica al final, tras las luces añadidas
        return img
    return grain(img, amount=grain_amount, seed=seed)


def retrato_azul():
    """Clave alta de la familia: azul institucional luminoso."""
    return vertical(
        (680, 880),
        stops=[(0.0, INK_LIGHT), (0.55, INK), (1.0, INK_DEEP)],
        light=(PAPER_2, 0.70, 0.18, 0.95, 0.30),
        shaft=(PAPER_2, 0.42, 0.20, 0.16),
        seed=1001,
    )


def retrato_negro():
    """Clave baja: azul-negro, la misma luz apenas insinuada."""
    return vertical(
        (680, 880),
        stops=[(0.0, SLATE), (0.5, (0x1a, 0x1f, 0x29)), (1.0, NEAR_BLACK)],
        light=(GOLD_PALE, 0.72, 0.16, 0.82, 0.15),
        shaft=(GOLD_PALE, 0.40, 0.18, 0.09),
        seed=2002,
        arc_alpha=54, rule_alpha=28, vig=0.34, grain_amount=0.06,
    )


def escenario():
    """Clave cálida: el foco de sala abriendo un halo en el fondo del escenario."""
    img = vertical(
        (840, 1080),
        stops=[(0.0, INK), (0.5, (0x1a, 0x27, 0x42)), (1.0, INK_DEEP)],
        light=(GOLD_PALE, 0.50, 0.74, 0.90, 0.20),
        shaft=(GOLD_PALE, 0.46, 0.24, 0.11),
        seed=3003,
        arc_alpha=58, rule_alpha=30, vig=0.42,
        skip_grain=True,
    )
    # Halo alto y frío, muy abierto: profundidad de caja escénica.
    img = glow(img, PAPER_2, 0.50, 0.06, 1.05, 0.10, falloff=2.2)
    return grain(img, amount=0.055, seed=3003)


# -------------------------------------------------------------------- OG

def og_card():
    """Tarjeta social: papel, filete de oro, monograma FL y el nombre."""
    w, h = 1200, 630
    img = gradient((w, h), [(0.0, PAPER), (0.6, PAPER_2), (1.0, LINE)], angle_deg=118)
    img = glow(img, PAPER, 0.38, 0.30, 0.85, 0.55, falloff=1.8)

    f_mono = load_font(SERIF_CANDIDATES, 74)
    f_name = load_font(SERIF_CANDIDATES, 66)
    f_tag = load_font(SANS_CANDIDATES, 19)

    def marco(d, s):
        d.rectangle([28 * s, 28 * s, w * s - 28 * s - 1, h * s - 28 * s - 1],
                    outline=GOLD_PALE + (150,), width=max(1, int(1.5 * s)))

    img = Image.alpha_composite(img.convert("RGBA"), overlay((w, h), marco)).convert("RGB")

    d = ImageDraw.Draw(img)
    cx = w / 2

    if f_mono:
        # Monograma, igual que favicon.svg: FL en oro sobre papel.
        tracked_text(d, (cx, 150), "FL", f_mono, GOLD, tracking=6)
    if f_name:
        tracked_text(d, (cx, 288), "FABEKA LEBRÓN", f_name, INK, tracking=9)
    # Filete corto bajo el nombre.
    d.line([(cx - 90, 400), (cx + 90, 400)], fill=GOLD_PALE, width=1)
    if f_tag:
        tracked_text(d, (cx, 432), "FIRMA DE PENSAMIENTO E INFLUENCIA INTERNACIONAL",
                     f_tag, INK_70, tracking=4)
        tracked_text(d, (cx, 500), "BARCELONA · SÃO PAULO · SANTO DOMINGO",
                     f_tag, GRAY, tracking=4)

    return grain(img, amount=0.03, seed=4004, blur=0.5)


def main():
    print("Generando imágenes temporales en assets/img/ …")
    save(retrato_azul(), "fabeka-retrato-azul.jpg")
    save(retrato_negro(), "fabeka-retrato-negro.jpg")
    save(escenario(), "fabeka-escenario.jpg")
    save(og_card(), "og-fabeka-lebron.jpg", quality=92)
    print("Listo. Son placeholders: sustituir por las fotografías oficiales.")


if __name__ == "__main__":
    main()
