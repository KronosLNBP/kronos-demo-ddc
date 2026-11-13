"""Genera por curso: infografía (SVG), diagrama de flujo (SVG) y portada para el catálogo.
Uso: python3 tools/build_graficos.py alergologia cardiologia ...
"""
import json, os, sys, html, textwrap
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(str(s))
COLS = ['#4fd1c5', '#7c8cff', '#f6ad55', '#f687b3', '#63b3ed', '#b794f4', '#68d391']

# ---------- Diagramas de flujo (contenido clínico por curso) ----------
# Cada paso: (texto, tipo, rama_no) — tipo: 'box' | 'dec' | 'act' | 'end'; rama_no = texto del cuadro a la derecha si es decisión.
FLUJOS = {
    'alergologia': ("Anafilaxia: manejo inicial", [
        ("Sospecha: inicio súbito de piel o mucosas + compromiso respiratorio o cardiovascular", 'box', None),
        ("Adrenalina IM en el muslo: 0.01 mg/kg (máx. 0.5 mg adulto, 0.3 mg niño)", 'act', None),
        ("Retirar el alérgeno · posición supina con piernas elevadas · oxígeno · líquidos IV", 'box', None),
        ("¿Mejora en 5–15 minutos?", 'dec', "No: repetir adrenalina IM, más líquidos; si persiste, infusión IV en UCI"),
        ("Segunda línea: antihistamínico H1, salbutamol si hay sibilancias, esteroide", 'box', None),
        ("Observar 6–12 h (reacción bifásica) · triptasa sérica", 'box', None),
        ("Alta: autoinyector de adrenalina, plan escrito, brazalete y envío a Alergología", 'end', None),
    ]),
    'cardiologia': ("Dolor torácico y sospecha de SICA", [
        ("Dolor torácico sugestivo de isquemia", 'box', None),
        ("ECG de 12 derivaciones en menos de 10 minutos", 'act', None),
        ("¿Elevación del ST o BRIHH nuevo?", 'dec', "Sí: SICA CEST → angioplastia primaria si es posible en < 120 min; si no, trombólisis (< 12 h de síntomas)"),
        ("Troponina ultrasensible a las 0 y 1–3 h", 'box', None),
        ("¿Troponina elevada?", 'dec', "No: angina inestable (si la clínica es de isquemia)"),
        ("IAM sin elevación del ST", 'box', None),
        ("Aspirina + inhibidor P2Y12 + anticoagulante + estatina de alta intensidad", 'act', None),
        ("Estratificar (GRACE): coronariografía inmediata (< 2 h) si inestable; temprana (< 24 h) si alto riesgo", 'end', None),
    ]),
    'cirugia': ("Enfermedad litiásica biliar", [
        ("Dolor en hipocondrio derecho o epigastrio", 'box', None),
        ("Ultrasonido de hígado y vías biliares", 'act', None),
        ("¿Fiebre, Murphy positivo, pared > 4 mm?", 'dec', "No y dolor < 6 h: cólico biliar → colecistectomía laparoscópica electiva"),
        ("Colecistitis aguda: ayuno, líquidos, antibiótico", 'box', None),
        ("¿Ictericia o colédoco > 6 mm?", 'dec', "No: colecistectomía laparoscópica temprana (< 72 h)"),
        ("Coledocolitiasis: CPRE con extracción y después colecistectomía", 'box', None),
        ("¿Fiebre + ictericia + dolor (Charcot)?", 'dec', "No: completar CPRE y colecistectomía"),
        ("Colangitis: antibiótico y drenaje biliar; urgente si hay hipotensión o confusión (Reynolds)", 'end', None),
    ]),
    'dermatologia': ("Lesión pigmentada sospechosa", [
        ("Lesión pigmentada nueva o que cambia", 'box', None),
        ("ABCDE · signo del patito feo · dermatoscopia", 'act', None),
        ("¿Es sospechosa de melanoma?", 'dec', "No: vigilancia, fotografía y fotoprotección"),
        ("Biopsia escisional completa con márgenes de 1–3 mm", 'act', None),
        ("¿Melanoma confirmado?", 'dec', "No: seguimiento según el diagnóstico"),
        ("Medir el índice de Breslow (principal factor pronóstico)", 'box', None),
        ("Escisión amplia: in situ 0.5–1 cm · ≤ 1 mm 1 cm · 1–2 mm 1–2 cm · > 2 mm 2 cm", 'box', None),
        ("Ganglio centinela si Breslow > 0.8 mm o ulceración · seguimiento de por vida", 'end', None),
    ]),
}


def wrap(t, n):
    return textwrap.wrap(t, n) or ['']


def flujo_svg(cid, titulo_curso):
    titulo, pasos = FLUJOS[cid]
    W = 1200; x0 = 120; bw = 560; y = 150; out = []; arrows = []
    for i, (txt, tipo, no) in enumerate(pasos):
        lines = wrap(txt, 46)
        h = 34 + 30 * len(lines)
        cx = x0 + bw / 2
        if tipo == 'dec':
            h = max(h, 120)
            pts = f"{cx},{y} {x0+bw},{y+h/2} {cx},{y+h} {x0},{y+h/2}"
            out.append(f'<polygon points="{pts}" fill="#1c2547" stroke="#7c8cff" stroke-width="2.5"/>')
            lines = wrap(txt, 30)
        else:
            fill = {'act': '#4fd1c5', 'end': '#141b33', 'box': '#141b33'}[tipo]
            stroke = {'act': 'none', 'end': '#48bb78', 'box': '#2a3563'}[tipo]
            out.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        col = '#0b1020' if tipo == 'act' else '#e8ecf8'
        ty = y + h / 2 - (len(lines) - 1) * 15 + 8
        for k, l in enumerate(lines):
            out.append(f'<text x="{cx}" y="{ty + k*30}" text-anchor="middle" font-size="21" font-weight="700" fill="{col}">{E(l)}</text>')
        if no:
            nl = wrap(no, 30); nh = 30 + 28 * len(nl); nx = x0 + bw + 90; ny = y + h / 2 - nh / 2
            out.append(f'<path d="M{x0+bw},{y+h/2} H{nx}" stroke="#9aa4c7" stroke-width="2.5" fill="none" marker-end="url(#ar)"/>')
            sid = 'No' if not no.startswith('Sí') else 'Sí'
            out.append(f'<text x="{x0+bw+22}" y="{y+h/2-10}" font-size="18" font-weight="700" fill="#9aa4c7">{"Sí" if sid=="Sí" else "No"}</text>')
            out.append(f'<rect x="{nx}" y="{ny}" width="420" height="{nh}" rx="14" fill="#141b33" stroke="#f6ad55" stroke-width="2"/>')
            for k, l in enumerate(nl):
                out.append(f'<text x="{nx+210}" y="{ny+38+k*28}" text-anchor="middle" font-size="19" fill="#e8ecf8">{E(l.split(": ",1)[1] if k==0 and ": " in l and l.split(":")[0] in ("No","Sí") else l)}</text>')
        if i < len(pasos) - 1:
            lab = ''
            if tipo == 'dec':
                lab = f'<text x="{cx+14}" y="{y+h+28}" font-size="18" font-weight="700" fill="#9aa4c7">{"No" if (no or "").startswith("Sí") else "Sí"}</text>'
            arrows.append(f'<path d="M{cx},{y+h} V{y+h+50}" stroke="#9aa4c7" stroke-width="2.5" fill="none" marker-end="url(#ar)"/>{lab}')
        y += h + 54
    H = int(y + 40)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, 'Segoe UI', Roboto, Arial, sans-serif">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4c7"/></marker></defs>
<rect width="{W}" height="{H}" fill="#0b1020"/>
<text x="{W/2}" y="64" text-anchor="middle" font-size="36" font-weight="800" fill="#e8ecf8">{E(titulo)}</text>
<text x="{W/2}" y="100" text-anchor="middle" font-size="18" fill="#9aa4c7">Diagrama de flujo · {E(titulo_curso)} · KronosMedicine</text>
{''.join(arrows)}{''.join(out)}
<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="14" fill="#5b648a">Material educativo · Revisar siempre la Guía de Práctica Clínica vigente</text>
</svg>'''


def infografia_svg(d):
    W = 1080; pad = 50; cols = 2; gap = 24; cw = (W - 2 * pad - gap) / cols
    cards = []; y0 = 260; colY = [y0, y0]
    for i, r in enumerate(d['resumen']):
        c = colY.index(min(colY)); x = pad + c * (cw + gap); y = colY[c]
        col = COLS[i % len(COLS)]
        tl = wrap(r['titulo'], 34); pl = wrap(r['perla'], 46)
        h = 70 + 30 * len(tl) + 26 * len(pl) + 18
        s = [f'<rect x="{x}" y="{y}" width="{cw}" height="{h}" rx="18" fill="#141b33"/>',
             f'<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{col}"/>',
             f'<circle cx="{x+44}" cy="{y+42}" r="20" fill="{col}"/><text x="{x+44}" y="{y+49}" text-anchor="middle" font-size="18" font-weight="800" fill="#0b1020">{i+1}</text>']
        for k, l in enumerate(tl):
            s.append(f'<text x="{x+78}" y="{y+50+k*30}" font-size="23" font-weight="800" fill="#e8ecf8">{E(l)}</text>')
        yy = y + 50 + 30 * len(tl) + 14
        for k, l in enumerate(pl):
            s.append(f'<text x="{x+28}" y="{yy+k*26}" font-size="18" fill="#b8c2e6">{E(l)}</text>')
        cards.append(''.join(s)); colY[c] = y + h + gap
    H = int(max(colY) + 60)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, 'Segoe UI', Roboto, Arial, sans-serif">
<defs><linearGradient id="hdr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c8cff"/><stop offset="1" stop-color="#4fd1c5"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="#0b1020"/>
<rect width="{W}" height="200" fill="url(#hdr)"/>
<text x="{pad}" y="62" font-size="20" font-weight="700" fill="#0b1020" letter-spacing="3">KRONOSMEDICINE · {E(d['especialidad'].upper())}</text>
<text x="{pad}" y="128" font-size="52" font-weight="800" fill="#0b1020">{E(d['titulo'])} de un vistazo</text>
<text x="{pad}" y="172" font-size="22" fill="#0b1020">{len(d['modulos'])} temas · la perla ENARM de cada uno</text>
{''.join(cards)}
<text x="{W/2}" y="{H-22}" text-anchor="middle" font-size="14" fill="#5b648a">Material educativo de KronosMedicine · Revisar siempre la Guía de Práctica Clínica vigente</text>
</svg>'''


def portada_html(d):
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}body{{width:1280px;height:720px;overflow:hidden;font-family:Inter,Poppins,sans-serif;color:#eef2ff;
background:radial-gradient(700px 500px at 15% 20%,rgba(37,99,235,.45),transparent 60%),radial-gradient(700px 500px at 90% 90%,rgba(79,209,197,.3),transparent 60%),#070b1a;position:relative}}
.logo{{position:absolute;right:-40px;top:60px;height:640px;opacity:.22}}.c{{position:absolute;left:90px;top:120px;width:900px}}
.e{{color:#4fd1c5;font-weight:800;letter-spacing:6px;font-size:24px;text-transform:uppercase}}h1{{font-size:104px;line-height:1;margin:22px 0 26px;font-weight:800}}
.s{{font-size:30px;color:#b8c2e6;line-height:1.35;max-width:820px}}.chips{{display:flex;gap:14px;margin-top:44px}}.chips span{{background:rgba(79,209,197,.15);border:1px solid rgba(79,209,197,.4);color:#4fd1c5;font-weight:800;font-size:24px;padding:12px 22px;border-radius:999px}}
.b{{position:absolute;left:90px;top:50px;display:flex;align-items:center;gap:12px;font-weight:800;font-size:26px}}.b img{{height:48px}}.b span{{color:#4fd1c5}}
</style></head><body><img class="logo" src="file://{RAIZ}/assets/img/logo.png"><div class="b"><img src="file://{RAIZ}/assets/img/logo.png">Kronos<span>Medicine</span></div>
<div class="c"><p class="e">Curso ENARM · {E(d['especialidad'])}</p><h1>{E(d['titulo'])}</h1><p class="s">{E(d['subtitulo'])}</p>
<div class="chips"><span>{len(d['modulos'])} módulos</span><span>{len(d['flashcards'])} flash cards</span><span>{len(d['examen']['preguntas'])} preguntas</span></div></div></body></html>'''


if __name__ == '__main__':
    import asyncio
    from playwright.async_api import async_playwright
    ids = sys.argv[1:]
    async def main():
        async with async_playwright() as p:
            b = await p.chromium.launch(args=['--allow-file-access-from-files'])
            for cid in ids:
                d = json.load(open(f'{RAIZ}/content/{cid}.json', encoding='utf-8'))
                open(f'{RAIZ}/assets/img/infografias/{cid}-infografia.svg', 'w', encoding='utf-8').write(infografia_svg(d))
                open(f'{RAIZ}/assets/img/infografias/{cid}-algoritmo.svg', 'w', encoding='utf-8').write(flujo_svg(cid, d['titulo']))
                tmp = f'/tmp/portada-{cid}.html'; open(tmp, 'w', encoding='utf-8').write(portada_html(d))
                pg = await b.new_page(viewport={'width': 1280, 'height': 720})
                await pg.goto(f'file://{tmp}'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=f'{RAIZ}/assets/img/posters/curso-{cid}.jpg', type='jpeg', quality=88)
                await pg.close()
                print('gráficos', cid)
            await b.close()
    asyncio.run(main())
