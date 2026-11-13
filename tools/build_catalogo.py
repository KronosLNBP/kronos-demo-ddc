"""Genera content/catalogo.json (lo que admin.html publica en Firestore) a partir de los cursos construidos."""
import json, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDEN = sys.argv[1:] or ['alergologia', 'cardiologia', 'cirugia', 'dermatologia']
cursos = []
for cid in ORDEN:
    p = os.path.join(RAIZ, 'content', f'{cid}.json')
    if not os.path.exists(p): continue
    d = json.load(open(p, encoding='utf-8'))
    cursos.append({
        'id': cid, 'titulo': d['titulo'], 'descripcion': d['subtitulo'], 'especialidad': d['especialidad'],
        'nivel': 'CURSO ENARM', 'poster': f'assets/img/posters/curso-{cid}.jpg',
        'modulos': len(d['modulos']), 'horas': round(d['duracionMin'] / 60, 1),
        'preguntas': len(d['examen']['preguntas']), 'flashcards': len(d['flashcards']),
    })
json.dump({'cursos': cursos}, open(os.path.join(RAIZ, 'content', 'catalogo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('catálogo:', [c['id'] for c in cursos])
