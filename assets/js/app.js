// Lección demo de Kronos: carga el contenido desde content/<leccion>.json
// Para otra lección: index.html?leccion=<id> con su JSON en content/.
// Cada sección se abre por su hash: index.html#flashcards, #examenes, etc.

const params = new URLSearchParams(location.search);
const LECCION = params.get('leccion') || 'ddc';
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

let DATA = null;

fetch(`content/${LECCION}.json`)
  .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(init)
  .catch(() => { $('titulo').textContent = 'No se pudo cargar la lección.'; });

function init(data) {
  DATA = data;
  document.title = `${data.titulo} | KronosMedicine`;
  $('titulo').textContent = `${data.especialidad} · ${data.titulo}`;
  $('especialidad').textContent = data.especialidad;
  $('drawerTitulo').textContent = data.titulo;
  $('palabras').innerHTML = data.palabrasClave.map((p) => `<li>${esc(p)}</li>`).join('');

  renderMenu(data.secciones);
  renderMapa(data.secciones);
  renderResumen(data.resumen);
  renderInfografias(data.infografias);
  renderMediaGrid('clasesGrabadas', data.videos.filter((v) => v.id !== 'intro').map((v) => ({ ...v, subtitulo: v.duracion })), 'Video pendiente');
  renderClasesVivo(data.clasesEnVivo);
  renderMediaGrid('cirugias', data.cirugias.map((c) => ({ ...c, subtitulo: c.tipo })), 'Cirugía pendiente');
  renderCursos(data.cursos);
  setupFlashcards(data.flashcards);
  setupExamen(data.examen);
  setupDrawer();

  window.addEventListener('hashchange', mostrarSeccion);
  mostrarSeccion();
}

/* ---------- Navegación ---------- */

function renderMenu(secciones) {
  $('menu').innerHTML = secciones.map((s, i) => `
    <li><a href="#${esc(s.id)}" data-id="${esc(s.id)}">
      <span class="num">${i + 1}</span><span class="ico">${esc(s.icono)}</span>${esc(s.titulo)}
    </a></li>`).join('');
  $('menu').addEventListener('click', (e) => { if (e.target.closest('a')) cerrarDrawer(); });
}

function setupDrawer() {
  $('burger').addEventListener('click', () => (document.body.classList.contains('menu-open') ? cerrarDrawer() : abrirDrawer()));
  $('scrim').addEventListener('click', cerrarDrawer);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') cerrarDrawer(); });
}
function abrirDrawer() {
  document.body.classList.add('menu-open');
  $('scrim').hidden = false;
  $('burger').setAttribute('aria-expanded', 'true');
}
function cerrarDrawer() {
  document.body.classList.remove('menu-open');
  $('scrim').hidden = true;
  $('burger').setAttribute('aria-expanded', 'false');
}

function mostrarSeccion() {
  const secs = DATA.secciones;
  const id = location.hash.slice(1);
  const idx = Math.max(0, secs.findIndex((s) => s.id === id));
  const s = secs[idx];

  document.querySelectorAll('.panel').forEach((p) => p.classList.toggle('active', p.dataset.panel === s.id));
  document.querySelectorAll('#menu a').forEach((a) => a.classList.toggle('active', a.dataset.id === s.id));

  $('seccionTitulo').textContent = s.titulo;
  $('seccionIntro').textContent = s.intro;
  $('seccionVideo').innerHTML = mediaHTML(s.video, `Video de la Dra. Torres: ${s.titulo}`, 'Video explicativo pendiente');

  $('anterior').disabled = idx === 0;
  $('siguiente').disabled = idx === secs.length - 1;
  $('anterior').onclick = () => { location.hash = secs[idx - 1].id; };
  $('siguiente').onclick = () => { location.hash = secs[idx + 1].id; };
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ---------- Medios ---------- */

// Acepta un archivo de video (assets/videos/x.mp4) o una URL de inserción (YouTube/Vimeo).
function mediaHTML(src, titulo, vacio) {
  if (!src) return `<div class="placeholder">${esc(vacio)}</div>`;
  if (/\.(mp4|webm|mov)$/i.test(src)) {
    return `<video src="${esc(src)}" controls preload="metadata" playsinline title="${esc(titulo)}"></video>`;
  }
  return `<iframe src="${esc(src)}" title="${esc(titulo)}" allowfullscreen loading="lazy"></iframe>`;
}

function renderMediaGrid(el, items, vacio) {
  $(el).innerHTML = `<div class="grid">${items.map((v) => `
    <div class="media">
      ${mediaHTML(v.embed || v.archivo, v.titulo, vacio)}
      <p>${esc(v.titulo)}${v.subtitulo ? ` · <span class="muted">${esc(v.subtitulo)}</span>` : ''}</p>
    </div>`).join('')}</div>`;
}

/* ---------- Secciones ---------- */

function renderMapa(secciones) {
  $('mapa').innerHTML = secciones.slice(1).map((s) => `
    <a class="block tile" href="#${esc(s.id)}"><span class="ico">${esc(s.icono)}</span><strong>${esc(s.titulo)}</strong></a>`).join('');
}

function renderResumen(bloques) {
  $('resumen').innerHTML = bloques
    .map((b) => `<article class="block"><h3>${esc(b.titulo)}</h3><p>${esc(b.texto)}</p></article>`)
    .join('');
}

function renderInfografias(items) {
  $('infografias').innerHTML = `<div class="grid">${items.map((i) => `
    <figure class="media">
      <img src="${esc(i.imagen)}" alt="${esc(i.alt)}" loading="lazy"
           onerror="this.outerHTML='<div class=&quot;placeholder&quot;>Infografía pendiente</div>'">
      <p>${esc(i.titulo)}</p>
    </figure>`).join('')}</div>`;
}

function renderClasesVivo(clases) {
  $('clasesVivo').innerHTML = clases.map((c) => `
    <article class="block live">
      <span class="badge">EN VIVO</span>
      <h3>${esc(c.titulo)}</h3>
      <p class="muted">${esc(c.ponente)} · ${esc(c.fecha)}</p>
      ${c.enlace ? `<a class="btn" href="${esc(c.enlace)}" target="_blank" rel="noopener">Unirme</a>` : '<button class="btn" disabled>Próximamente</button>'}
    </article>`).join('');
}

function renderCursos(cursos) {
  $('cursos').innerHTML = `<div class="grid">${cursos.map((c) => `
    <article class="block">
      <h3>${esc(c.titulo)}</h3>
      <p>${esc(c.descripcion)}</p>
      <p class="muted">Precio: ${esc(c.precio)}</p>
    </article>`).join('')}</div>`;
}

function setupFlashcards(cards) {
  let mazo = [...cards];
  let i = 0;
  let sabidas = 0;
  const card = $('card');

  const pintar = () => {
    card.classList.remove('flipped');
    $('progreso').textContent = `${sabidas}/${cards.length}`;
    if (!mazo.length) {
      $('cardFront').textContent = '¡Terminaste! Repasa de nuevo en unos días.';
      $('cardBack').textContent = '';
      return;
    }
    $('cardFront').textContent = mazo[i].frente;
    $('cardBack').textContent = mazo[i].reverso;
  };

  card.addEventListener('click', () => { if (mazo.length) card.classList.toggle('flipped'); });
  card.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); card.click(); } });
  $('lase').addEventListener('click', () => { if (!mazo.length) return; mazo.splice(i, 1); sabidas++; i = mazo.length ? i % mazo.length : 0; pintar(); });
  $('repasar').addEventListener('click', () => { if (!mazo.length) return; i = (i + 1) % mazo.length; pintar(); });
  pintar();
}

function setupExamen(ex) {
  const muestra = (ex.muestra || []).map((n) => ex.preguntas[n]).filter(Boolean);
  $('muestraInfo').textContent = `${muestra.length} preguntas`;
  $('examInfo').textContent = `${ex.preguntas.length} preguntas en ${ex.minutos} minutos`;
  let reloj = null;
  let actuales = [];

  $('empezarMuestra').addEventListener('click', () => iniciar(muestra, null));
  $('empezar').addEventListener('click', () => {
    // DEMO: código fijo. En producción el código llega por mensaje tras el pago y se valida en el servidor.
    if ($('codigo').value.trim().toUpperCase() !== ex.codigoDemo) {
      $('codigoError').textContent = 'Código incorrecto.';
      return;
    }
    $('codigoError').textContent = '';
    iniciar(ex.preguntas, ex.minutos * 60);
  });

  function iniciar(preguntas, segundos) {
    actuales = preguntas;
    $('examGate').hidden = true;
    $('examBody').hidden = false;
    $('examResult').hidden = true;
    $('terminar').hidden = false;
    $('otraVez').hidden = true;
    $('examForm').innerHTML = preguntas.map((p, n) => `
      <div class="q" id="q${n}">
        <p class="caso">${esc(p.caso)}</p>
        <p><strong>${n + 1}. ${esc(p.pregunta)}</strong></p>
        ${p.opciones.map((o, k) => `<label><input type="radio" name="p${n}" value="${k}"> ${String.fromCharCode(65 + k)}) ${esc(o)}</label>`).join('')}
      </div>`).join('');

    $('timer').hidden = segundos == null;
    if (segundos != null) {
      let restante = segundos;
      const tick = () => {
        const m = String(Math.floor(restante / 60)).padStart(2, '0');
        const s = String(restante % 60).padStart(2, '0');
        $('timer').textContent = `${m}:${s}`;
        $('timer').classList.toggle('low', restante <= 60);
        if (restante-- <= 0) terminar();
      };
      tick();
      reloj = setInterval(tick, 1000);
    }
  }

  function terminar() {
    clearInterval(reloj);
    let aciertos = 0;
    actuales.forEach((p, n) => {
      const marcada = document.querySelector(`input[name="p${n}"]:checked`);
      const ok = marcada && Number(marcada.value) === p.correcta;
      if (ok) aciertos++;
      const q = $(`q${n}`);
      q.classList.add(ok ? 'correct' : 'wrong');
      q.querySelectorAll('input').forEach((inp) => (inp.disabled = true));
      q.insertAdjacentHTML('beforeend', `<p class="exp"><strong>Respuesta: ${String.fromCharCode(65 + p.correcta)}.</strong> ${esc(p.explicacion)}</p>`);
    });
    $('terminar').hidden = true;
    $('otraVez').hidden = false;
    $('examResult').hidden = false;
    $('examResult').innerHTML = `<p class="score">Calificación: ${aciertos}/${actuales.length}</p>`;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  $('terminar').addEventListener('click', (e) => { e.preventDefault(); terminar(); });
  $('otraVez').addEventListener('click', () => {
    $('examBody').hidden = true;
    $('examGate').hidden = false;
    $('codigo').value = '';
  });
}
