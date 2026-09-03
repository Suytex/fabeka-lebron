# Fabeka Lebrón — Sitio oficial

Sitio estático (HTML + CSS + JS, sin build) de la firma de pensamiento e influencia
internacional de **Fabeka Lebrón Pereyra**. Se publica con GitHub Pages.

---

## Estructura

```
.
├── index.html            Portada — narrativa en 7 capítulos
├── pensamiento.html      Entrada al pensamiento e índice de los ensayos
├── ensayos.html          Los seis ensayos completos
├── trayectoria.html      Trayectoria completa
├── consejos.html         Consejos & Advisory
├── mentoria.html         Mentoría
├── plataformas.html      Las cinco plataformas
├── conferencias.html     Conferencias y formatos
├── prensa.html           Bios oficiales, CV y contacto de prensa
├── styles.css            Hoja de estilo única de todo el sitio
├── site.js               Menú móvil + animaciones de entrada
├── favicon.svg           Monograma FL
├── set-domain.sh         Fija la URL pública y genera sitemap.xml
├── tools/
│   └── gen-placeholders.py   Genera las imágenes temporales de relleno
├── robots.txt
├── .nojekyll             Evita que GitHub Pages procese el sitio con Jekyll
└── assets/
    ├── cv/               CV_Fabeka_Lebron_2026_ES.pdf · _EN.pdf
    └── img/              Imágenes (temporales — ver más abajo)
```

---

## Sistema de diseño

Definido como variables CSS en `:root` (arriba de `styles.css`):

| Token | Valor | Uso |
|---|---|---|
| `--ink` | `#1c2b4a` | Texto principal, azul institucional |
| `--ink-70` | `#45526d` | Texto secundario |
| `--gold` | `#a9884b` | Acento, enlaces, numeración |
| `--gold-pale` | `#cbb586` | Filetes y marcos |
| `--paper` | `#fdfcfa` | Fondo base |
| `--paper-2` | `#f7f5f0` | Fondo de secciones alternas (`.warm`) |
| `--line` | `#e7e2d8` | Separadores |

**Tipografía:** Cormorant Garamond (display y editorial) + Jost (etiquetas y navegación),
cargadas desde Google Fonts. El cuerpo usa Georgia como serif de sistema.

---

## ⚠️ Imágenes temporales

Las cuatro imágenes de `assets/img/` son **provisionales**. No son fotografías:
son composiciones abstractas generadas con `tools/gen-placeholders.py` (Pillow),
en la paleta de marca, para que el sitio no se vea a medio hacer mientras llega
el material definitivo. No hay ninguna persona en ellas, ni real ni generada.

| Archivo | Tamaño | Dónde se usa |
|---|---|---|
| `assets/img/fabeka-retrato-azul.jpg` | 680 × 880 | Hero de `index.html` |
| `assets/img/fabeka-retrato-negro.jpg` | 680 × 880 | Bio de `index.html` |
| `assets/img/fabeka-escenario.jpg` | 840 × 1080 | `conferencias.html` |
| `assets/img/og-fabeka-lebron.jpg` | 1200 × 630 | Preview al compartir en redes |

**Para sustituirlas** basta con sobrescribir cada archivo respetando el nombre y
la proporción. No hay que tocar el HTML: las etiquetas `<img>` ya están puestas
y los marcos usan `aspect-ratio: 3.4/4.4` con `object-fit: cover` (las verticales
recortan por los lados si la foto es más ancha). Después, borrar en los tres
marcos el comentario `<!-- IMAGEN TEMPORAL … -->` y este apartado del README, y
—si ya no hace falta— la carpeta `tools/`.

El `alt` de las tres verticales ya está escrito pensando en la fotografía real
("Retrato de Fabeka Lebrón"), justamente para no tener que editarlo el día del
relevo.

**Regenerar las temporales** (opcional, el resultado es idéntico en cada
ejecución):

```bash
pip install Pillow
python3 tools/gen-placeholders.py
```

---

## Pendientes antes del lanzamiento público

1. **Fotografías oficiales.** Los tres marcos y la imagen social ya están activos, pero
   con imágenes temporales. Sustituirlas en cuanto llegue el material de la clienta:
   ver **⚠️ Imágenes temporales** arriba.

2. **URL pública.** Ya fijada en `https://suytex.github.io/fabeka-lebron`. Si cambia
   (dominio propio, otro repositorio), basta con volver a ejecutar:

   ```bash
   ./set-domain.sh https://<nueva-url>
   ```

   El script inserta `canonical` y `og:url` en las 9 páginas, pasa las imágenes sociales
   a URL absoluta y regenera `sitemap.xml` y `robots.txt`. Es idempotente. **Hay que
   volver a ejecutarlo cada vez que se añada una página nueva**, después de darla de alta
   en el array `PAGES` del propio script.

---

## Publicar en GitHub Pages

```bash
git add -A
git commit -m "Actualiza el sitio"
git push
```

En **Settings → Pages** del repositorio: *Source* = `Deploy from a branch`,
*Branch* = `main` / `(root)`. Con dominio propio, añadir un archivo `CNAME` en la raíz
con el dominio, volver a ejecutar `set-domain.sh` con la nueva URL y configurar en el
registrador:

```
ALIAS/ANAME  @      → <usuario>.github.io
CNAME        www    → <usuario>.github.io
```

## Ver el sitio en local

```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

---

© 2026 Fabeka Lebrón · Iberoamerican Bridges
