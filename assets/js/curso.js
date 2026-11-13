// Página de curso de KronosMedicine.
// curso.html?id=<curso> carga content/<curso>.json. Secciones por hash: #inicio, #clases/m3, #resumenes/imagen, #flashcards/Clínica…

const params = new URLSearchParams(location.search);
const CURSO = (params.get('id') || 'ddc').replace(/[^a-z0-9-]/gi, '');
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const mmss = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

const TIPOS = {
  video: { ico: '🎥', nombre: 'Video', color: '#7c8cff' },
  podcast: { ico: '🎧', nombre: 'Podcast', color: '#b794f4' },
  lectura: { ico: '📄', nombre: 'Lectura', color: '#4fd1c5' },
  flashcards: { ico: '🃏', nombre: 'Flash cards', color: '#f6ad55' },
  infografia: { ico: '🧭', nombre: 'Infografía', color: '#63b3ed' },
  examen: { ico: '⏱️', nombre: 'Examen', color: '#f687b3' },
};

let DATA;

/* ---------- Avance guardado en este navegador ---------- */
const KEY = `kronos-${CURSO}-hecho`;
let hecho = new Set();
try { hecho = new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); } catch (e) { /* sin almacenamiento */ }
function guardar() { try { localStorage.setItem(KEY, JSON.stringify([...hecho])); } catch (e) { /* sin almacenamiento */ } }

fetch(`content/${CURSO}.json`)
  .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(init)
  .catch(() => { $('crumb').textContent = 'No se pudo cargar el curso.'; });

function init(data) {
  DATA = data;
  document.title = `${data.titulo} | KronosMedicine`;
  $('crumb').innerHTML = `<a href="./">Inicio</a> · ${esc(data.especialidad)} · ${esc(data.titulo)}`;
  $('drawerTitulo').textContent = data.titulo;

  renderMenu();
  renderInicio();
  renderRuta();
  renderPodcast();
  renderResumen();
  renderInfografias();
  renderDescargas();
  setupFlashcards();
  setupExamen();
  setupDrawer();
  actualizarAvance();

  window.addEventListener('hashchange', mostrarSeccion);
  mostrarSeccion();
}

/* ---------- Navegación ---------- */
function renderMenu() {
  $('menu').innerHTML = DATA.secciones.map((s, i) => `
    <li><a href="#${esc(s.id)}" data-id="${esc(s.id)}"><span class="num">${i + 1}</span><span class="ico">${esc(s.icono)}</span>${esc(s.titulo)}</a></li>`).join('');
  $('menu').addEventListener('click', (e) => { if (e.target.closest('a')) cerrarDrawer(); });
}
function setupDrawer() {
  $('burger').addEventListener('click', () => (document.body.classList.contains('menu-open') ? cerrarDrawer() : abrirDrawer()));
  $('scrim').addEventListener('click', cerrarDrawer);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') cerrarDrawer(); });
}
function abrirDrawer() { document.body.classList.add('menu-open'); $('scrim').hidden = false; $('burger').setAttribute('aria-expanded', 'true'); }
function cerrarDrawer() { document.body.classList.remove('menu-open'); $('scrim').hidden = true; $('burger').setAttribute('aria-expanded', 'false'); }

let seccionActual = null;
function mostrarSeccion() {
  const [id, param] = decodeURIComponent(location.hash.slice(1)).split('/');
  const secs = DATA.secciones;
  const idx = Math.max(0, secs.findIndex((s) => s.id === id));
  const s = secs[idx];

  document.querySelectorAll('.panel').forEach((p) => p.classList.toggle('active', p.dataset.panel === s.id));
  document.querySelectorAll('#menu a').forEach((a) => a.classList.toggle('active', a.dataset.id === s.id));

  $('seccionTitulo').textContent = s.id === 'inicio' ? DATA.titulo : s.titulo;
  if (seccionActual !== s.id) {
    $('seccionIntro').textContent = s.intro || '';
    $('seccionVideo').innerHTML = s.video
      ? `<video src="${esc(s.video)}" poster="${esc(s.poster || '')}" controls preload="metadata" playsinline title="Dra. Torres: ${esc(s.titulo)}"></video>` : '';
    $('explainer').hidden = !s.intro;
    $('explainer').classList.toggle('no-video', !s.video);
  }
  seccionActual = s.id;

  $('anterior').disabled = idx === 0;
  $('siguiente').disabled = idx === secs.length - 1;
  $('anterior').onclick = () => { location.hash = secs[idx - 1].id; };
  $('siguiente').onclick = () => { location.hash = secs[idx + 1].id; };

  if (s.id === 'flashcards' && param !== undefined) filtrarFlashcards(param);
  const destino = param && document.getElementById(`${s.id}-${param}`);
  if (destino) {
    if (destino.tagName === 'DETAILS') destino.open = true;
    destino.classList.add('flash');
    setTimeout(() => destino.classList.remove('flash'), 1600);
    setTimeout(() => destino.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
  } else {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

/* ---------- Inicio ---------- */
function renderInicio() {
  const acts = DATA.modulos.flatMap((m) => m.actividades);
  $('subtitulo').textContent = DATA.subtitulo;
  $('meta').innerHTML = [
    ['⏳', `${DATA.duracionMin / 60} horas`],
    ['🗂️', `${DATA.modulos.length} módulos`],
    ['✅', `${acts.length} actividades`],
    ['🎯', DATA.nivel],
  ].map(([i, t]) => `<li><span>${i}</span>${esc(t)}</li>`).join('');
  $('palabras').innerHTML = DATA.palabrasClave.map((p) => `<li>${esc(p)}</li>`).join('');

  const porTipo = {};
  acts.forEach((a) => { porTipo[a.tipo] = (porTipo[a.tipo] || 0) + a.minutos; });
  const orden = Object.entries(porTipo).sort((a, b) => b[1] - a[1]);
  const total = DATA.duracionMin;
  $('mix').innerHTML = `
    <div class="mix-bar">${orden.map(([t, m]) => `<span style="width:${(m / total) * 100}%;background:${TIPOS[t].color}" title="${esc(TIPOS[t].nombre)}: ${m} min"></span>`).join('')}</div>
    <ul class="mix-legend">${orden.map(([t, m]) => `
      <li><span class="dot" style="background:${TIPOS[t].color}"></span>${TIPOS[t].ico} ${esc(TIPOS[t].nombre)}<strong>${m} min</strong></li>`).join('')}
    </ul>`;
}

/* ---------- Ruta de estudio ---------- */
function enlaceActividad(a) {
  switch (a.tipo) {
    case 'lectura': return `#resumenes/${a.destino}`;
    case 'infografia': return `#diagramas/${a.destino}`;
    case 'podcast': return `#podcast/${a.destino}`;
    case 'flashcards': return `#flashcards/${a.destino}`;
    case 'examen': return '#examenes';
    default: return '';
  }
}

function renderRuta() {
  $('ruta').innerHTML = DATA.modulos.map((m, mi) => `
    <details class="module" id="clases-${esc(m.id)}" ${mi === 0 ? 'open' : ''}>
      <summary>
        <span class="mod-num">${mi + 1}</span>
        <span class="mod-title"><strong>${esc(m.titulo)}</strong><span class="muted">${m.minutos} min · ${m.actividades.length} actividades</span></span>
        <span class="mod-done" id="done-${esc(m.id)}"></span>
      </summary>
      <div class="mod-body">
        ${m.capsula ? `<div class="capsula"><video src="${esc(m.capsula)}" poster="${esc(m.capsulaPoster || '')}" controls preload="none" playsinline></video><p class="muted">🎬 Cápsula animada del módulo ${mi + 1}</p></div>` : ''}
        <div class="mod-cols">
          <div><h4>Objetivos</h4><ul>${m.objetivos.map((o) => `<li>${esc(o)}</li>`).join('')}</ul></div>
          <div><h4>Temas</h4><ul>${m.temas.map((t) => `<li>${esc(t)}</li>`).join('')}</ul></div>
        </div>
        <ol class="acts">${m.actividades.map((a, ai) => {
          const id = `${m.id}-${ai}`;
          const link = enlaceActividad(a);
          return `
          <li class="act ${hecho.has(id) ? 'is-done' : ''}" data-id="${id}">
            <label class="check"><input type="checkbox" ${hecho.has(id) ? 'checked' : ''} aria-label="Marcar como hecha"><span></span></label>
            <span class="act-ico" style="background:${TIPOS[a.tipo].color}">${TIPOS[a.tipo].ico}</span>
            <span class="act-title">${esc(a.titulo)}<span class="muted">${esc(TIPOS[a.tipo].nombre)} · ${a.minutos} min</span></span>
            ${link ? `<a class="btn sm ghost" href="${link}">Abrir</a>` : `<button class="btn sm ghost" type="button" data-video="${esc(m.id)}">Ver</button>`}
          </li>`;
        }).join('')}</ol>
        <div class="mod-video" id="video-${esc(m.id)}" hidden>
          ${m.video ? `<video src="${esc(m.video)}" controls preload="none" playsinline></video>`
            : `<div class="placeholder wide">🎬 La clase completa está en producción por el área de Videos.<br><span class="muted">${m.capsula ? 'Mientras tanto, mira la cápsula animada al inicio del módulo.' : 'El guion de este módulo ya está listo.'}</span></div>`}
        </div>
      </div>
    </details>`).join('');

  $('ruta').addEventListener('change', (e) => {
    const li = e.target.closest('.act');
    if (!li) return;
    marcar(li.dataset.id, e.target.checked);
  });
  $('ruta').addEventListener('click', (e) => {
    const b = e.target.closest('[data-video]');
    if (b) { const v = $(`video-${b.dataset.video}`); v.hidden = !v.hidden; }
  });
}

function marcar(id, si) {
  if (si) hecho.add(id); else hecho.delete(id);
  guardar();
  const li = document.querySelector(`.act[data-id="${id}"]`);
  if (li) { li.classList.toggle('is-done', si); li.querySelector('input').checked = si; }
  actualizarAvance();
}

function actualizarAvance() {
  let total = 0; let listos = 0;
  DATA.modulos.forEach((m) => {
    let mt = 0; let ml = 0;
    m.actividades.forEach((a, ai) => { mt += a.minutos; if (hecho.has(`${m.id}-${ai}`)) ml += a.minutos; });
    total += mt; listos += ml;
    const el = $(`done-${m.id}`);
    if (el) el.innerHTML = ml === mt ? '<span class="badge ok">Completo</span>' : `<span class="ring" style="--p:${(ml / mt) * 100}"></span>`;
  });
  const pct = Math.round((listos / total) * 100);
  $('avanceTxt').textContent = `${pct}%`;
  $('avanceBar').style.width = `${pct}%`;
}

/* ---------- Podcast ---------- */
function renderPodcast() {
  const moduloDe = {};
  DATA.modulos.forEach((m, i) => m.actividades.forEach((a) => { if (a.tipo === 'podcast') moduloDe[a.destino] = i + 1; }));
  $('podcast').innerHTML = `<ol class="episodes">${DATA.podcast.map((p, i) => `
    <li class="episode" id="podcast-${esc(p.id)}">
      <span class="ep-num">${i + 1}</span>
      <span class="ep-title"><strong>${esc(p.titulo)}</strong><span class="muted">Módulo ${moduloDe[p.id] || '–'} · ${p.minutos} min</span></span>
      ${p.audio ? `<audio src="${esc(p.audio)}" controls preload="none"></audio>` : '<span class="badge">En producción</span>'}
    </li>`).join('')}</ol>`;
}

/* ---------- Resúmenes ---------- */
function renderResumen() {
  $('resumen').innerHTML = `
    <nav class="toc">${DATA.resumen.map((b) => `<a href="#resumenes/${esc(b.id)}">${esc(b.titulo)}</a>`).join('')}</nav>
    ${DATA.resumen.map((b) => `
    <article class="block" id="resumenes-${esc(b.id)}">
      <h3>${esc(b.titulo)}</h3>
      <ul class="points">${b.puntos.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>
      ${b.perla ? `<p class="perla"><strong>Perla ENARM:</strong> ${esc(b.perla)}</p>` : ''}
    </article>`).join('')}`;
}

/* ---------- Infografías ---------- */
function renderInfografias() {
  $('infografias').innerHTML = DATA.infografias.map((i) => `
    <figure class="infografia" id="diagramas-${esc(i.id)}">
      <figcaption><strong>${esc(i.titulo)}</strong> <a href="${esc(i.imagen)}" target="_blank" rel="noopener">Abrir en tamaño completo ↗</a></figcaption>
      <img src="${esc(i.imagen)}" alt="${esc(i.alt)}" loading="lazy">
    </figure>`).join('');
}

/* ---------- Descargas ---------- */
function renderDescargas() {
  const d = DATA.descargas || {};
  Object.entries(d).forEach(([sec, items]) => {
    const panel = document.querySelector(`[data-panel="${sec}"]`);
    if (!panel || !items.length) return;
    panel.insertAdjacentHTML('beforeend', `<div class="downloads"><span class="muted">Descargar:</span>${items.map((i) => `<a class="btn sm ghost" href="${esc(i.archivo)}" download>⬇ ${esc(i.titulo)}</a>`).join('')}</div>`);
  });
}

/* ---------- Flash cards ---------- */
let fc = { mazo: [], i: 0, sabidas: 0, total: 0, tema: '' };
function setupFlashcards() {
  const temas = [...new Set(DATA.flashcards.map((c) => c.tema))];
  $('filtros').innerHTML = ['', ...temas].map((t) => `<button class="chip-btn" data-tema="${esc(t)}">${t ? esc(t) : 'Todas'}</button>`).join('');
  $('filtros').addEventListener('click', (e) => { const b = e.target.closest('[data-tema]'); if (b) location.hash = `flashcards/${b.dataset.tema}`; });
  const card = $('card');
  card.addEventListener('click', () => { if (fc.mazo.length) card.classList.toggle('flipped'); });
  card.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); card.click(); } });
  $('lase').addEventListener('click', () => { if (!fc.mazo.length) return; fc.mazo.splice(fc.i, 1); fc.sabidas++; fc.i = fc.mazo.length ? fc.i % fc.mazo.length : 0; pintarCard(); });
  $('repasar').addEventListener('click', () => { if (!fc.mazo.length) return; fc.i = (fc.i + 1) % fc.mazo.length; pintarCard(); });
  $('reiniciar').addEventListener('click', () => filtrarFlashcards(fc.tema));
  filtrarFlashcards('');
}
function filtrarFlashcards(tema) {
  fc = { mazo: DATA.flashcards.filter((c) => !tema || c.tema === tema), i: 0, sabidas: 0, tema };
  fc.total = fc.mazo.length;
  document.querySelectorAll('.chip-btn').forEach((b) => b.classList.toggle('active', b.dataset.tema === tema));
  pintarCard();
}
function pintarCard() {
  $('card').classList.remove('flipped');
  $('progreso').textContent = `${fc.sabidas}/${fc.total} dominadas`;
  if (!fc.mazo.length) {
    $('cardTema').textContent = '';
    $('cardFront').textContent = '¡Mazo terminado! Repásalo de nuevo en unos días.';
    $('cardBack').textContent = '';
    return;
  }
  const c = fc.mazo[fc.i];
  $('cardTema').textContent = c.tema;
  $('cardFront').textContent = c.frente;
  $('cardBack').textContent = c.reverso;
}

/* ---------- Exámenes ---------- */
function setupExamen() {
  const ex = DATA.examen;
  const muestra = ex.muestra.map((n) => ex.preguntas[n]);
  $('muestraInfo').textContent = `${muestra.length} preguntas · sin límite de tiempo · resultado al final`;
  $('examInfo').textContent = `${ex.preguntas.length} preguntas en ${ex.minutos} minutos · aprobatorio ${ex.aprobatorio}%`;

  let reloj = null; let actuales = []; let segundosTotal = null; let restante = 0; let inicio = 0; let modo = '';

  $('empezarMuestra').addEventListener('click', () => iniciar(muestra, null, 'muestra'));
  $('empezar').addEventListener('click', () => {
    // DEMO: código fijo. En producción el código llega por mensaje tras el pago y se valida en el servidor.
    if ($('codigo').value.trim().toUpperCase() !== ex.codigoDemo) { $('codigoError').textContent = 'Código incorrecto.'; return; }
    $('codigoError').textContent = '';
    iniciar(ex.preguntas, ex.minutos * 60, 'cronometrado');
  });

  function iniciar(preguntas, segundos, m) {
    actuales = preguntas; segundosTotal = segundos; modo = m; inicio = Date.now();
    $('examGate').hidden = true; $('examResult').hidden = true; $('examBody').hidden = false;
    $('examForm').innerHTML = preguntas.map((p, n) => `
      <div class="q" id="q${n}">
        <p class="q-meta">Pregunta ${n + 1} de ${preguntas.length} · ${esc(p.tema)}</p>
        <p class="caso">${esc(p.caso)}</p>
        <p class="q-preg">${esc(p.pregunta)}</p>
        ${p.opciones.map((o, k) => `<label class="opt"><input type="radio" name="p${n}" value="${k}"><span class="letra">${String.fromCharCode(65 + k)}</span>${esc(o)}</label>`).join('')}
      </div>`).join('');
    contar();
    $('timer').hidden = segundos == null;
    clearInterval(reloj);
    if (segundos != null) {
      restante = segundos;
      const tick = () => {
        $('timer').textContent = `⏱ ${mmss(Math.max(restante, 0))}`;
        $('timer').classList.toggle('low', restante <= 60);
        if (restante-- <= 0) terminar(true);
      };
      tick(); reloj = setInterval(tick, 1000);
    }
    window.scrollTo({ top: $('examBody').offsetTop - 80, behavior: 'smooth' });
  }

  function contar() {
    const n = actuales.filter((_, i) => document.querySelector(`input[name="p${i}"]:checked`)).length;
    $('contestadas').textContent = `Contestadas: ${n}/${actuales.length}`;
  }
  $('examForm').addEventListener('change', contar);

  function terminar(porTiempo = false) {
    clearInterval(reloj);
    const usados = Math.round((Date.now() - inicio) / 1000);
    const res = actuales.map((p, i) => {
      const m = document.querySelector(`input[name="p${i}"]:checked`);
      const r = m ? Number(m.value) : null;
      return { p, r, ok: r === p.correcta };
    });
    const ok = res.filter((x) => x.ok).length;
    const sin = res.filter((x) => x.r === null).length;
    const mal = res.length - ok - sin;
    const pct = Math.round((ok / res.length) * 100);
    const aprobado = pct >= ex.aprobatorio;

    const temas = {};
    res.forEach((x) => {
      const t = temas[x.p.tema] || (temas[x.p.tema] = { ok: 0, n: 0, modulo: x.p.modulo });
      t.n++; if (x.ok) t.ok++;
    });
    const repasar = Object.entries(temas).filter(([, t]) => t.ok / t.n < 0.7);
    const modIdx = (id) => DATA.modulos.findIndex((m) => m.id === id) + 1;

    if (modo === 'cronometrado') {
      DATA.modulos.forEach((m) => m.actividades.forEach((a, ai) => { if (a.tipo === 'examen') marcar(`${m.id}-${ai}`, true); }));
    }

    $('examBody').hidden = true;
    $('examResult').hidden = false;
    $('examResult').innerHTML = `
      <div class="result-head ${aprobado ? 'pass' : 'fail'}">
        <div class="score-ring" style="--p:${pct}"><span>${pct}%</span></div>
        <div>
          <p class="eyebrow">${modo === 'muestra' ? 'Examen muestra' : 'Examen cronometrado'}${porTiempo ? ' · se acabó el tiempo' : ''}</p>
          <h2>${aprobado ? '¡Aprobado!' : 'Aún no apruebas'}</h2>
          <p class="muted">${ok} de ${res.length} correctas · aprobatorio ${ex.aprobatorio}%</p>
        </div>
      </div>
      <ul class="result-stats">
        <li><strong class="c-ok">${ok}</strong>Correctas</li>
        <li><strong class="c-bad">${mal}</strong>Incorrectas</li>
        <li><strong>${sin}</strong>Sin responder</li>
        <li><strong>${mmss(Math.min(usados, segundosTotal ?? usados))}</strong>${segundosTotal ? `de ${mmss(segundosTotal)}` : 'Tiempo'}</li>
      </ul>

      <h3 class="h3">Resultado por tema</h3>
      <table class="by-topic">
        <thead><tr><th>Tema</th><th>Aciertos</th><th>Dominio</th></tr></thead>
        <tbody>${Object.entries(temas).map(([nombre, t]) => {
          const p = Math.round((t.ok / t.n) * 100);
          return `<tr><td>${esc(nombre)}</td><td>${t.ok}/${t.n}</td><td><span class="tbar"><span style="width:${p}%;background:${p >= 70 ? 'var(--ok)' : p >= 50 ? '#f6ad55' : 'var(--bad)'}"></span></span> ${p}%</td></tr>`;
        }).join('')}</tbody>
      </table>

      ${repasar.length ? `<div class="recos"><h3 class="h3">Te recomendamos repasar</h3><ul>${repasar.map(([nombre, t]) => `
        <li><strong>${esc(nombre)}</strong> → <a href="#clases/${esc(t.modulo)}">Módulo ${modIdx(t.modulo)} de la ruta</a> · <a href="#flashcards/${esc(nombre)}">flash cards</a></li>`).join('')}</ul></div>`
        : '<div class="recos ok"><h3 class="h3">Dominas todos los temas evaluados</h3><p>Repasa las flash cards durante la semana para no olvidarlo.</p></div>'}

      <h3 class="h3">Revisión pregunta por pregunta</h3>
      <ol class="review">${res.map((x, i) => `
        <li class="${x.ok ? 'r-ok' : x.r === null ? 'r-none' : 'r-bad'}">
          <p class="q-meta">${x.ok ? '✔ Correcta' : x.r === null ? '— Sin responder' : '✘ Incorrecta'} · ${esc(x.p.tema)}</p>
          <p class="caso">${esc(x.p.caso)}</p>
          <p class="q-preg">${i + 1}. ${esc(x.p.pregunta)}</p>
          ${x.r !== null && !x.ok ? `<p class="tu">Tu respuesta: ${String.fromCharCode(65 + x.r)}) ${esc(x.p.opciones[x.r])}</p>` : ''}
          <p class="correcta">Respuesta correcta: ${String.fromCharCode(65 + x.p.correcta)}) ${esc(x.p.opciones[x.p.correcta])}</p>
          <p class="exp">${esc(x.p.explicacion)}</p>
        </li>`).join('')}</ol>

      <div class="cta">
        <button class="btn" id="repetir">Volver a los exámenes</button>
        <a class="btn ghost" href="#clases">Ir a la ruta de estudio</a>
      </div>`;
    $('repetir').addEventListener('click', () => { $('examResult').hidden = true; $('examGate').hidden = false; $('codigo').value = ''; window.scrollTo({ top: 0, behavior: 'smooth' }); });
    window.scrollTo({ top: $('examResult').offsetTop - 80, behavior: 'smooth' });
  }

  $('terminar').addEventListener('click', (e) => {
    e.preventDefault();
    const faltan = actuales.filter((_, i) => !document.querySelector(`input[name="p${i}"]:checked`)).length;
    if (faltan && !$('terminar').dataset.confirm) {
      $('terminar').dataset.confirm = '1';
      $('terminar').textContent = `Te faltan ${faltan}. Toca otra vez para calificar`;
      setTimeout(() => { delete $('terminar').dataset.confirm; $('terminar').textContent = 'Terminar y calificar'; }, 4000);
      return;
    }
    delete $('terminar').dataset.confirm; $('terminar').textContent = 'Terminar y calificar';
    terminar(false);
  });
}
