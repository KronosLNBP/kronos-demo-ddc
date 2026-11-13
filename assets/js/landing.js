// Landing de KronosMedicine: lee content/plataforma.json
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Secciones de la plataforma que tienen su equivalente dentro del curso demo.
const EN_CURSO = { resumenes: 'resumenes', diagramas: 'diagramas', flashcards: 'flashcards', examenes: 'examenes', 'clases-grabadas': 'clases' };

fetch('content/plataforma.json')
  .then((r) => r.json())
  .then(init)
  .catch(() => {});

function init(data) {
  const p = data.presentacion;
  $('heroVideo').innerHTML = `<video src="${esc(p.video)}" poster="${esc(p.poster)}" controls preload="metadata" playsinline title="${esc(p.titulo)}"></video>
    <p class="caption">▶ ${esc(p.titulo)}</p>`;

  $('features').innerHTML = data.secciones.map((s, i) => `
    <button class="feature" data-i="${i}">
      <span class="thumb" style="background-image:url('${esc(s.poster)}')"><span class="play">▶</span></span>
      <span class="feature-body">
        <span class="feature-ico">${esc(s.icono)}</span>
        <strong>${esc(s.titulo)}</strong>
        <span class="muted">${esc(s.texto)}</span>
      </span>
    </button>`).join('');
  $('features').addEventListener('click', (e) => {
    const b = e.target.closest('.feature');
    if (b) abrirModal(data.secciones[Number(b.dataset.i)]);
  });

  const v3d = data.videos3d || [];
  $('v3d').innerHTML = v3d.map((v, i) => `
    <button class="v3d" data-i="${i}" style="background-image:url('${esc(v.poster)}')" aria-label="Ver video: ${esc(v.titulo)}">
      <span class="play">▶</span>
      <span class="v3d-txt"><small>${esc(v.especialidad)}</small><strong>${esc(v.titulo)}</strong></span>
    </button>`).join('');
  $('v3d').addEventListener('click', (e) => {
    const b = e.target.closest('.v3d');
    if (!b) return;
    const v = v3d[Number(b.dataset.i)];
    abrirModal({ video: v.video, poster: v.poster, icono: v.especialidad, titulo: v.titulo,
      texto: v.curso === 'ddc' ? 'Forma parte del curso demo gratuito.' : 'Forma parte del curso completo para miembros Premium.', curso: v.curso });
  });

  $('catalogo').innerHTML = data.cursos.map((c) => c.disponible ? `
    <a class="course-card" href="curso.html?id=${esc(c.id)}">
      <span class="badge ${c.premium ? '' : 'ok'}">${c.premium ? 'Premium' : 'Demo gratis'}</span>
      <h3>${esc(c.titulo)}</h3>
      <p class="muted">${esc(c.especialidad)} · ${esc(c.horas)} horas</p>
      <ul class="chips">${c.recursos.map((r) => `<li>${esc(r)}</li>`).join('')}</ul>
      <span class="btn">Entrar al curso</span>
    </a>` : `
    <div class="course-card disabled">
      <span class="badge">Próximamente</span>
      <h3>${esc(c.titulo)}</h3>
      <p class="muted">${esc(c.especialidad)} · ${esc(c.horas)} horas</p>
    </div>`).join('');

  // Menú móvil
  $('burger').addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    $('burger').setAttribute('aria-expanded', String(open));
  });
  $('toplinks').addEventListener('click', (e) => { if (e.target.closest('a')) document.body.classList.remove('nav-open'); });

  $('modalClose').addEventListener('click', cerrarModal);
  $('modal').addEventListener('click', (e) => { if (e.target.id === 'modal') cerrarModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') cerrarModal(); });
}

function abrirModal(s) {
  $('modalVideo').innerHTML = `<video src="${esc(s.video)}" poster="${esc(s.poster)}" controls autoplay playsinline></video>`;
  $('modalIcono').textContent = s.icono;
  $('modalTitulo').textContent = s.titulo;
  $('modalTexto').textContent = s.texto;
  const destino = EN_CURSO[s.id];
  if (s.curso) {
    $('modalCta').hidden = false;
    $('modalCta').textContent = 'Ver el curso';
    $('modalCta').href = `curso.html?id=${encodeURIComponent(s.curso)}`;
  } else {
    $('modalCta').textContent = 'Verlo en el curso demo';
    $('modalCta').hidden = !destino;
    if (destino) $('modalCta').href = `curso.html?id=ddc#${destino}`;
  }
  $('modal').hidden = false;
  document.body.classList.add('no-scroll');
}

function cerrarModal() {
  if ($('modal').hidden) return;
  $('modalVideo').innerHTML = '';
  $('modal').hidden = true;
  document.body.classList.remove('no-scroll');
}
