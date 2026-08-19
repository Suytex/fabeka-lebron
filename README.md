# Fabeka Lebrón — Sitio oficial

Sitio estático (HTML + CSS + JS, sin build) de la firma de pensamiento e influencia
internacional de **Fabeka Lebrón Pereyra**. Se publica con GitHub Pages.

---

## Estructura

```
.
├── index.html            Portada — narrativa en 7 capítulos
├── pensamiento.html      Ensayos y pensamiento
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
├── robots.txt
├── .nojekyll             Evita que GitHub Pages procese el sitio con Jekyll
└── assets/
    ├── cv/               CV_Fabeka_Lebron_2026_ES.pdf · _EN.pdf
    └── img/              Fotografías (pendientes de entrega)
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

## Pendientes antes del lanzamiento público

1. **Fotografías.** Hay tres marcos con marcador de posición. Para activarlos, colocar los
   archivos en `assets/img/` y sustituir el comentario HTML por la etiqueta `<img>` que ya
   está escrita justo encima de cada `<div class="note">`:

   | Página | Archivo esperado |
   |---|---|
   | `index.html` (hero) | `assets/img/fabeka-retrato-azul.jpg` |
   | `index.html` (bio) | `assets/img/fabeka-retrato-negro.jpg` |
   | `conferencias.html` | `assets/img/fabeka-escenario.jpg` |

2. **Imagen para redes.** Crear `assets/img/og-fabeka-lebron.jpg` (1200 × 630 px). Es la
   miniatura que aparece al compartir el sitio en WhatsApp, LinkedIn y X.

3. **URL pública.** El sitio aún no tiene dominio fijado: no hay `canonical`, `og:url`
   ni `sitemap.xml`. En cuanto se conozca la URL de GitHub Pages (o el dominio propio),
   ejecutar una sola vez:

   ```bash
   ./set-domain.sh https://<usuario>.github.io/<repo>
   ```

   El script inserta `canonical` y `og:url` en las 8 páginas, pasa las imágenes sociales
   a URL absoluta y genera `sitemap.xml` y `robots.txt`. Es idempotente: se vuelve a
   ejecutar tal cual cuando cambie el dominio.

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
