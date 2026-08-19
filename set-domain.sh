#!/usr/bin/env bash
# Fija la URL pública del sitio: inserta canonical + og:url en las 8 páginas
# y genera sitemap.xml y robots.txt.
#
#   ./set-domain.sh https://usuario.github.io/fabeka-lebron
#   ./set-domain.sh https://fabekalebron.com
#
# Es idempotente: se puede volver a ejecutar cuando cambie el dominio.

set -euo pipefail

[ $# -eq 1 ] || { echo "Uso: $0 <URL base, sin barra final>"; exit 1; }
BASE="${1%/}"
DATE=$(date +%F)

PAGES=(index.html pensamiento.html trayectoria.html consejos.html
       mentoria.html plataformas.html conferencias.html prensa.html)

for f in "${PAGES[@]}"; do
  [ -f "$f" ] || continue
  # limpiar valores previos
  perl -0pi -e 's{<link rel="canonical"[^>]*>\n}{}g; s{<meta property="og:url"[^>]*>\n}{}g' "$f"

  if [ "$f" = "index.html" ]; then URL="$BASE/"; else URL="$BASE/$f"; fi

  # canonical + og:url justo después del <title>
  perl -0pi -e "s{(</title>\n)}{\$1<link rel=\"canonical\" href=\"$URL\">\n<meta property=\"og:url\" content=\"$URL\">\n}" "$f"

  # imágenes sociales en absoluto (los scrapers no resuelven rutas relativas)
  perl -0pi -e "s{content=\"[^\"]*assets/img/og-fabeka-lebron\.jpg\"}{content=\"$BASE/assets/img/og-fabeka-lebron.jpg\"}g" "$f"
done

# JSON-LD: url de la persona
perl -0pi -e "s{(\"alternateName\": \"Fabeka Lebrón\",\n)(  \"url\":[^\n]*\n)?}{\$1  \"url\": \"$BASE/\",\n}" index.html

# sitemap.xml
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  for f in "${PAGES[@]}"; do
    if [ "$f" = "index.html" ]; then loc="$BASE/"; pr="1.0"; else loc="$BASE/$f"; pr="0.8"; fi
    echo "  <url><loc>$loc</loc><lastmod>$DATE</lastmod><priority>$pr</priority></url>"
  done
  echo '</urlset>'
} > sitemap.xml

# robots.txt
printf 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' "$BASE" > robots.txt

echo "✓ URL base fijada en: $BASE"
echo "  Actualizados: ${PAGES[*]} sitemap.xml robots.txt"
