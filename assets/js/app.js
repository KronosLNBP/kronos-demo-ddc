// Lección demo de Kronos: carga el contenido desde content/<leccion>.json
// Para otra lección: index.html?leccion=<id> con su JSON en content/.

const params = new URLSearchParams(location.search);
const LECCION = params.get('leccion') || 'ddc';
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

fetch(`content/${LECCION}.json`)
  .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(init)
  .catch(() => { $('titulo').textContent = 'No se pudo cargar la lección.'; });

function init(data) {
  document.title = `${data.titulo} | KronosMedicine`;
  $('titulo').textContent = data.titulo;
  $('especialidad').textContent = data.especialidad;
  $('palabras').innerHTML = data.palabrasClave.map((p) => `<li>${esc(p)}</li>`).join('');

  setupTabs();
  renderResumen(data.resumen);
  renderInfografias(data.infografias);
  renderVideos(data.videos);
  setupFlashcards(data.flashcards);
  setupExamen(data.examen);
}

function setupTabs() {
  document.querySelectorAll('.tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab, .panel').forEach((el) => el.classList.remove('active'));
      btn.classList.add('active');
      $(btn.dataset.tab).classList.add('active');
    });
  });
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

function renderVideos(items) {
  $('videos').innerHTML = `<div class="grid">${items.map((v) => `
    <div class="media">
      ${v.embed
        ? `<iframe src="${esc(v.embed)}" title="${esc(v.titulo)}" allowfullscreen loading="lazy"></iframe>`
        : '<div class="placeholder">Video pendiente</div>'}
      <p>${esc(v.titulo)} · ${esc(v.duracion)}</p>
    </div>`).join('')}</div>`;
}

function setupFlashcards(cards) {
  let mazo = [...cards];
  let i = 0;
  let sabidas = 0;
  const card = $('card');

  const pintar = () => {
    card.classList.remove('flipped');
    if (!mazo.length) {
      $('cardFront').textContent = '¡Terminaste! Repasa de nuevo en unos días.';
      $('cardBack').textContent = '';
      $('progreso').textContent = `${sabidas}/${cards.length}`;
      return;
    }
    $('cardFront').textContent = mazo[i].frente;
    $('cardBack').textContent = mazo[i].reverso;
    $('progreso').textContent = `${sabidas}/${cards.length}`;
  };

  card.addEventListener('click', () => card.classList.toggle('flipped'));
  card.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); card.click(); } });
  $('lase').addEventListener('click', () => { if (!mazo.length) return; mazo.splice(i, 1); sabidas++; i = mazo.length ? i % mazo.length : 0; pintar(); });
  $('repasar').addEventListener('click', () => { if (!mazo.length) return; i = (i + 1) % mazo.length; pintar(); });
  pintar();
}

function setupExamen(ex) {
  $('examInfo').textContent = `${ex.preguntas.length} preguntas en ${ex.minutos} minutos`;
  let restante = ex.minutos * 60;
  let reloj = null;

  $('empezar').addEventListener('click', () => {
    // DEMO: código fijo. En producción el código llega por mensaje tras el pago y se valida en el servidor.
    if ($('codigo').value.trim().toUpperCase() !== ex.codigoDemo) {
      $('codigoError').textContent = 'Código incorrecto.';
      return;
    }
    $('examGate').hidden = true;
    $('examBody').hidden = false;
    $('examForm').innerHTML = ex.preguntas.map((p, n) => `
      <div class="q" id="q${n}">
        <p class="caso">${esc(p.caso)}</p>
        <p><strong>${n + 1}. ${esc(p.pregunta)}</strong></p>
        ${p.opciones.map((o, k) => `<label><input type="radio" name="p${n}" value="${k}"> ${String.fromCharCode(65 + k)}) ${esc(o)}</label>`).join('')}
      </div>`).join('');
    tick();
    reloj = setInterval(tick, 1000);
  });

  function tick() {
    const m = String(Math.floor(restante / 60)).padStart(2, '0');
    const s = String(restante % 60).padStart(2, '0');
    $('timer').textContent = `${m}:${s}`;
    $('timer').classList.toggle('low', restante <= 60);
    if (restante-- <= 0) terminar();
  }

  function terminar() {
    clearInterval(reloj);
    let aciertos = 0;
    ex.preguntas.forEach((p, n) => {
      const marcada = document.querySelector(`input[name="p${n}"]:checked`);
      const ok = marcada && Number(marcada.value) === p.correcta;
      if (ok) aciertos++;
      const q = $(`q${n}`);
      q.classList.add(ok ? 'correct' : 'wrong');
      q.querySelectorAll('input').forEach((inp) => (inp.disabled = true));
      q.insertAdjacentHTML('beforeend', `<p class="exp"><strong>Respuesta: ${String.fromCharCode(65 + p.correcta)}.</strong> ${esc(p.explicacion)}</p>`);
    });
    $('terminar').hidden = true;
    $('examResult').hidden = false;
    $('examResult').innerHTML = `<p class="score">Calificación: ${aciertos}/${ex.preguntas.length}</p>`;
    $('examBody').prepend($('examResult'));
  }

  $('terminar').addEventListener('click', (e) => { e.preventDefault(); terminar(); });
}
