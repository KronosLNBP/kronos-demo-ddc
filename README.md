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

## Estructura y quién es dueño de qué

| Carpeta / archivo | Qué contiene | Área responsable |
| --- | --- | --- |
| `content/ddc.json` | Resumen, flash cards, preguntas, lista de videos e infografías | Creador de producto |
| `assets/img/infografias/` | Infografías exportadas en `.webp` o `.svg` | Diseño |
| `assets/css/styles.css` | Colores, tipografía y componentes visuales | Diseño |
| `index.html`, `assets/js/app.js` | Estructura de la página y lógica (pestañas, flash cards, examen) | Programación |
| Campo `embed` de `videos` en el JSON | URL de inserción de YouTube o Vimeo (no listado) | Videos |
| `.github/workflows/deploy.yml`, `.htaccess` | Publicación en el hosting Apache | Programación |

Los videos **no se suben al repositorio**. Se suben como "no listados" a YouTube o Vimeo y en el JSON se pega la URL de inserción, por ejemplo `https://www.youtube.com/embed/ID_DEL_VIDEO`.

## Forma de trabajo

1. Cada área trabaja en su propia rama: `diseno`, `programacion`, `videos` o `contenido`.
2. Al terminar algo, abre un Pull Request hacia `main`.
3. El responsable de esa área lo revisa y lo aprueba. Si toca contenido médico, también lo revisa el Creador de producto.
4. Todo lo que entra a `main` se publica solo en el hosting (ver la sección siguiente).

## Publicación

Cada push a `main` ejecuta el workflow **Publicar demo**, que valida el JSON y sube los archivos por FTP al hosting Apache. Para activarlo, en GitHub entra a **Settings → Secrets and variables → Actions** y agrega:

- `FTP_SERVER`
- `FTP_USERNAME`
- `FTP_PASSWORD`
- `FTP_DIR`: carpeta destino, por ejemplo `/public_html/demo/`

Con eso el demo queda en `https://kronosmedicine.com.mx/demo/`.

## Contenido

El contenido actual de `content/ddc.json` es **de ejemplo** y solo sirve para probar los componentes. El Creador de producto lo reemplaza con la versión validada, escrita con redacción propia a partir de la GPC. No se copia texto ni imágenes de material de terceros.

Para agregar otra lección, crea `content/<id>.json` con la misma estructura y ábrela con `index.html?leccion=<id>`.
