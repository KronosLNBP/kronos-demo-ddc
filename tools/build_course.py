"""Genera content/<id>.json para un curso de KronosMedicine a partir de una definición compacta.

Uso: python3 tools/build_course.py alergologia
Cada definición vive en tools/cursos/<id>.py y expone CURSO (dict) y MODULOS (lista).
"""
import importlib.util, json, random, sys, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECCIONES = [
    ("inicio", "Inicio del curso", "⏳", None, ""),
    ("clases", "Ruta de estudio", "🗺️", "clases-grabadas", "Sigue los módulos en orden: video, lectura, podcast y flash cards. Marca cada actividad al terminarla."),
    ("podcast", "Podcast", "🎧", None, "Escucha cada tema mientras te arreglas, vas en el transporte o estás en el gym."),
    ("resumenes", "Resúmenes", "📄", "resumenes", "Resúmenes cortos para comprender, reforzar y recordar. Cada tema cierra con su perla ENARM."),
    ("diagramas", "Infografía y diagrama de flujo", "🧭", "diagramas", "Lo esencial del curso en una imagen y el algoritmo clave. Léelos después del resumen."),
    ("flashcards", "Flash cards", "🃏", "flashcards", "Repaso rápido por tema. Después de leer el resumen, repasa las tarjetas poco a poco durante la semana."),
    ("examenes", "Exámenes", "⏱️", "examenes", "Cada intento saca preguntas distintas del banco del curso. Al final tienes tu resultado completo por tema."),
]


def cargar(cid):
    ruta = os.path.join(RAIZ, 'tools', 'cursos', f'{cid}.py')
    spec = importlib.util.spec_from_file_location(cid, ruta)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.CURSO, mod.MODULOS


def construir(cid):
    C, M = cargar(cid)
    rnd = random.Random(cid)
    secciones = []
    for sid, tit, ico, vid, intro in SECCIONES:
        s = {"id": sid, "titulo": tit, "icono": ico, "video": "", "intro": intro}
        if vid:
            s["video"] = f"assets/videos/{vid}.mp4"; s["poster"] = f"assets/img/posters/{vid}.jpg"
        secciones.append(s)

    modulos, resumen, flash, preguntas, podcast = [], [], [], [], []
    for i, m in enumerate(M, 1):
        mid = f"m{i}"
        corto = m.get("corto", m["titulo"])
        acts = [
            {"tipo": "video", "titulo": f"Clase: {m['titulo']}", "minutos": m.get("video", 8), "destino": ""},
            {"tipo": "lectura", "titulo": f"Resumen: {corto}", "minutos": m.get("lectura", 5), "destino": mid},
        ]
        if m.get("infografia"):
            acts.append({"tipo": "infografia", "titulo": m["infografia"][0], "minutos": 3, "destino": m["infografia"][1]})
        acts += [
            {"tipo": "podcast", "titulo": f"Episodio {i}: {m.get('podcast', corto)}", "minutos": m.get("pod", 6), "destino": f"p{i}"},
            {"tipo": "flashcards", "titulo": f"Flash cards: {corto}", "minutos": 3, "destino": corto},
        ]
        modulos.append({"id": mid, "titulo": m["titulo"], "minutos": sum(a["minutos"] for a in acts), "video": "",
                        "objetivos": m["objetivos"], "temas": m["temas"], "actividades": acts})
        resumen.append({"id": mid, "titulo": m["titulo"], "puntos": m["puntos"], "perla": m["perla"]})
        podcast.append({"id": f"p{i}", "titulo": m.get("podcast", corto), "minutos": m.get("pod", 6), "audio": ""})
        for f, r in m["flash"]:
            flash.append({"tema": corto, "frente": f, "reverso": r})
        for caso, preg, ops, ok, exp in m["preguntas"]:
            correcta = ops[ok]
            otras = [o for k, o in enumerate(ops) if k != ok]
            pos = rnd.randrange(len(ops))
            otras.insert(pos, correcta)
            preguntas.append({"tema": corto, "modulo": mid, "caso": caso, "pregunta": preg, "opciones": otras, "correcta": pos, "explicacion": exp})

    examen_min = C.get("examenMin", 20)
    modulos[-1]["actividades"].append({"tipo": "examen", "titulo": f"Examen cronometrado: {C.get('examenCantidad', 20)} preguntas", "minutos": examen_min, "destino": ""})
    modulos[-1]["minutos"] += examen_min
    total = sum(m["minutos"] for m in modulos)

    data = {
        "_nota": "Contenido redactado por Kronos a partir de los temas de los resúmenes de referencia y las GPC. Debe validarlo el Creador de producto.",
        "id": cid, "titulo": C["titulo"], "subtitulo": C["subtitulo"], "especialidad": C["especialidad"],
        "duracionMin": total, "nivel": C.get("nivel", "Pregrado, internado y preparación ENARM"),
        "palabrasClave": C["palabrasClave"], "secciones": secciones, "modulos": modulos,
        "resumen": resumen, "infografias": C.get("infografias", []), "flashcards": flash, "podcast": podcast,
        "examen": {"minutos": C.get("examenMin", 20), "cantidad": C.get("examenCantidad", 20), "muestraCantidad": 5,
                   "aprobatorio": 70, "codigoDemo": "KRONOS-DEMO", "preguntas": preguntas},
        "descargas": C.get("descargas", {}),
    }
    out = os.path.join(RAIZ, 'content', f'{cid}.json')
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{cid}: {len(modulos)} módulos · {total} min · {len(flash)} flash cards · {len(preguntas)} preguntas")
    return data


if __name__ == '__main__':
    for cid in sys.argv[1:]:
        construir(cid)
