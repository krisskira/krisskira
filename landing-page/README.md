# Portfolio de Crhistian Vergara

Generado con el template de landings (`template-kprrojects`). Se publica en
<https://krisskira.com/>.

```bash
npm install
npm run dev
npm run build
```

- Texto y secciones: `content/landing.json` (recorrido en `journey`, proyectos en `projects`)
- Nombre, SEO, JSON-LD y enlaces: `content/site.json`
- Traducción al inglés: `content/en.json` (la clave es el texto en español, exacto)
- Colores y fuentes: `content/theme.css`
- Imágenes y video: `public/media/`, generados con `python3 resources/build-media.py`
  (retrato, capturas de HotPlate y kLog, iconos y `og-cover.jpg` desde `resources/og-cover.html`)

## Publicar

El workflow `.github/workflows/pages.yml` construye y publica en GitHub Pages
cada push a `main` que toque `landing-page/`. En el repositorio:
**Settings → Pages → Source: GitHub Actions**.

## Código del template

`src/`, `scripts/vite-plugin-landing.js`, `index.html` y `eslint.config.js`
vienen del template. Para traer mejoras:

```bash
node ../../template-kprrojects/scripts/new-landing.mjs . --update
```
