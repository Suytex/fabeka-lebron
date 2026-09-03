# Estado del proyecto

Última actualización: **3 de septiembre de 2026**

Documento para retomar el trabajo sin tener que releer todo el sitio. El README
explica cómo funciona el proyecto; este archivo explica en qué punto está.

---

## Dónde está todo

| | |
|---|---|
| **Publicado en** | https://suytex.github.io/fabeka-lebron |
| **Repositorio** | `Suytex/fabeka-lebron` |
| **Rama de producción** | `main` — GitHub Pages despliega desde ahí, en la raíz |
| **Despliegue** | Automático al fusionar en `main`. Tarda entre 30 y 60 segundos |
| **Páginas** | 9 · `index` · `pensamiento` · `ensayos` · `trayectoria` · `consejos` · `mentoria` · `plataformas` · `conferencias` · `prensa` |
| **Peso del código** | 263 líneas de CSS · 49 de JS · sin dependencias ni build |

---

## Hecho hasta hoy

| Fecha | Qué |
|---|---|
| 19 ago 2026 | Sitio inicial, 8 páginas. URL pública fijada. Imágenes temporales de relleno |
| 3 sep 2026 | Página **Ensayos** con los seis ensayos del documento v2.3 (PR #3) |

**Sobre la entrega del 3 de septiembre.** Los ensayos I–III ya estaban dentro de
`pensamiento.html`; se movieron a `ensayos.html` junto con los tres nuevos, para
que ningún texto quedara publicado en dos URLs. `pensamiento.html` pasó a ser la
entrada al Manuscrito Fundacional, con un índice enlazado a cada ensayo.

El texto se copió literalmente del `.docx` y se contrastó con un script:
34 de 34 párrafos idénticos. **Esa regla se mantiene: los ensayos no se reescriben.
Cualquier ajuste de redacción lo aprueba Fabeka Lebrón.**

---

## Pendiente de la clienta

**Fotografías oficiales.** Las cuatro imágenes de `assets/img/` son composiciones
abstractas de relleno, no fotografías. Los marcos ya están montados: basta con
sobrescribir cada archivo respetando nombre y proporción, sin tocar el HTML.
El detalle completo está en el README, apartado *⚠️ Imágenes temporales*.

Cuando lleguen, además de sustituir los archivos hay que borrar los comentarios
`<!-- IMAGEN TEMPORAL … -->` de los tres marcos, el apartado del README y, si ya
no hace falta, la carpeta `tools/`.

---

## Deuda técnica, por orden de ataque

### 1. El velo de entrada bloquea el sitio sin JavaScript · ~1 sesión

`#veil` (`index.html:56`) es `position:fixed; inset:0; z-index:1000` y su única
salida es el script de `index.html:292`. Sin JS, la portada queda tapada de forma
permanente. El respaldo de 6 segundos también depende de JS, así que no es
respaldo. Tres problemas en el mismo sitio:

- Sin JS, no hay forma de llegar al contenido.
- Con JS, cuesta hasta 6 segundos **en cada visita**: no hay `sessionStorage`, así
  que el visitante recurrente vuelve a pasar por la cortina. Castiga el LCP.
- El velo se antepone al `skip-link`, así que un lector de pantalla entra ahí.

Los tres se resuelven a la vez: inyectar el velo desde JS en lugar de servirlo en
el HTML, y recordar la visita.

### 2. Menú y pie duplicados a mano en 9 archivos · ~1 sesión

Cada página repite el `<nav>`, el `#mobile-menu` y el mapa del pie. Añadir una
página son 27 ediciones sincronizadas (ver el checklist del README). Es el mayor
riesgo de mantenimiento del repositorio. Se arregla inyectando los tres bloques
desde `site.js`, o con plantillas y un paso de compilación mínimo.

### 3. Sin validación automática · ~20 min

No hay `.github/workflows/`. Un enlace roto o una etiqueta mal cerrada llega a
producción sin aviso. Con una acción que valide HTML y compruebe enlaces en cada
push bastaría. Los scripts de verificación usados el 3 de septiembre están en el
historial del PR #3 y se pueden reutilizar.

### 4. Fuentes servidas desde el CDN de Google · ~20 min

Las 9 páginas cargan Cormorant Garamond y Jost desde `fonts.googleapis.com`.
Es una dependencia externa y, con la clienta operando desde Barcelona, el
argumento de RGPD sobre Google Fonts es real. Autoalojar las dos familias resuelve
rendimiento y privacidad de una vez.

### 5. Pulido menor

| Punto | Dónde |
|---|---|
| `<img>` sin `width`/`height` ni `loading` → salto de layout | `conferencias.html:52` |
| `alt` inconsistente: «Fabeka Lebrón» vs «Retrato de Fabeka Lebrón» | `conferencias.html:52` frente a `index.html:109` y `:134` |
| 49 estilos inline sueltos (`style="…"`) | Las 9 páginas |
| Correo en texto plano, sin ofuscar, y como único canal de contacto | Las 9 páginas |
| CV con `download` en Prensa pero sin él en el pie de la portada | `index.html` |
| Imágenes solo en JPEG, sin WebP ni AVIF | `assets/img/` |
| Sin `hreflang` ni versión en inglés, con el CV sí traducido | Todo el sitio |

---

## Cómo retomar

```bash
git clone https://github.com/Suytex/fabeka-lebron.git
cd fabeka-lebron
python3 -m http.server 8000     # abrir http://localhost:8000
```

No hay que instalar nada: el sitio es HTML, CSS y JS planos. Solo
`tools/gen-placeholders.py` necesita Pillow, y únicamente si hay que regenerar
las imágenes temporales.

Para publicar, fusionar en `main`. Pages se encarga del resto.
