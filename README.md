# Kronos Medicine: lección demo

Lección demo de **Displasia del desarrollo de la cadera** para la app web de [kronosmedicine.com.mx](https://kronosmedicine.com.mx/). Incluye resumen, infografías, videos, flash cards y examen cronometrado.

**Entrega del avance: jueves 19 de noviembre de 2026.**

## Cómo verlo en tu computadora

```bash
git clone https://github.com/KronosLNBP/kronos-demo-ddc.git
cd kronos-demo-ddc
python3 -m http.server 8000
```

Abre http://localhost:8000. Tiene que ser con un servidor local, porque si abres `index.html` con doble clic el navegador bloquea la carga del JSON.

El código del examen demo es `KRONOS-DEMO`.

## Páginas

- **`index.html`: landing de la plataforma.** Presenta Kronos con el video "Modelo de estudio", las 8 secciones de la plataforma (cada una abre el video de la Dra. Torres que la explica) y el catálogo de cursos.
- **`curso.html?id=ddc`: página de un curso.** Tiene menú hamburguesa con 7 secciones:
  1. Inicio
  2. Ruta de estudio de 4 h
  3. Podcast
  4. Resúmenes
  5. Infografía y diagrama de flujo
  6. Flash cards
  7. Exámenes

  Cada sección tiene su enlace directo, por ejemplo `#flashcards/Clínica` o `#clases/m5`.

La ruta de estudio suma 240 min en 8 módulos que mezclan video (96 min), podcast (55), lectura (29), flash cards (22), examen (20) e infografía (18). El alumno marca cada actividad y su avance se guarda en el navegador.

Cada módulo abre con una **cápsula animada** de unos 2 minutos (`assets/videos/capsula-m1.mp4` … `m8`): motion graphics en español con música, sin voz. Los guiones de las clases completas y del podcast están en `docs/guiones-curso-ddc.md`.

**Descargables** (`assets/descargas/`): flash cards para imprimir a doble cara, infografía y diagrama de flujo en PDF y PNG, examen y hoja de respuestas. La clave de respuestas no se publica; se entrega aparte al docente.

Para agregar un curso nuevo, crea `content/<id>.json` con la misma estructura que `ddc.json` y agrégalo al catálogo en `content/plataforma.json`.

## Estructura y quién es dueño de qué

| Carpeta / archivo | Qué contiene | Área responsable |
| --- | --- | --- |
| `content/ddc.json` | Curso: módulos, resúmenes, flash cards, preguntas, podcast | Creador de producto |
| `content/plataforma.json` | Secciones de la landing y catálogo de cursos | Creador de producto |
| `docs/guiones-curso-ddc.md` | Guiones de clases y podcast | Videos + Creador de producto |
| `assets/img/infografias/` | Infografía y diagrama de flujo en SVG | Diseño |
| `assets/css/styles.css` | Colores, tipografía y componentes visuales | Diseño |
| `index.html`, `curso.html`, `assets/js/` | Landing, página de curso y su lógica | Programación |
| Campo `embed` de `videos` en el JSON | URL de inserción de YouTube o Vimeo (no listado) | Videos |
| `.github/workflows/deploy.yml`, `.htaccess` | Publicación en el hosting Apache | Programación |

Los videos **no se suben al repositorio**. Se suben como "no listados" a YouTube o Vimeo y en el JSON se pega la URL de inserción, por ejemplo `https://www.youtube.com/embed/ID_DEL_VIDEO`.

## Forma de trabajo

1. Cada área trabaja en su propia rama: `diseno`, `programacion`, `videos` o `contenido`.
2. Al terminar algo, abre un Pull Request hacia `main`.
3. El responsable de esa área lo revisa y lo aprueba. Si toca contenido médico, también lo revisa el Creador de producto.
4. Todo lo que entra a `main` se publica solo en GitHub Pages (ver la sección siguiente).

## Publicación

El demo se publica con **GitHub Pages** desde la rama `main`, carpeta raíz. Cada cambio que entra a `main` aparece en un par de minutos en:

**https://kronoslnbp.github.io/kronos-demo-ddc/**

Configuración (una sola vez): **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save**.

El archivo `.nojekyll` evita que GitHub procese el sitio con Jekyll; se publica tal cual.

Más adelante, para publicar en el hosting Apache de kronosmedicine.com.mx, está listo el workflow `.github/workflows/deploy.yml` (FTP). Solo se activa si se agregan los secretos `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` y `FTP_DIR`; mientras no existan, no hace nada.

## Contenido

El contenido de `content/ddc.json` está redactado con palabras propias a partir de los temas del PDF de referencia. Antes de considerarlo final, el Creador de producto lo valida contra la GPC vigente. No se copia texto ni imágenes de material de terceros.

Para agregar otra lección, crea `content/<id>.json` con la misma estructura y ábrela con `index.html?leccion=<id>`.
