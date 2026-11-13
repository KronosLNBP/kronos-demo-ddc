import json, html, asyncio, base64
from playwright.async_api import async_playwright
import os, sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CID=sys.argv[1]
OUT=f'/tmp/pdf-{CID}'; os.makedirs(OUT, exist_ok=True)
d=json.load(open(f'{R}/content/{CID}.json',encoding='utf-8'))
TEMA=d['titulo']
e=lambda s: html.escape(str(s))
logo='data:image/png;base64,'+base64.b64encode(open(f'{R}/tools/logo_small.png','rb').read()).decode()
BASE='''<style>@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter,Poppins,sans-serif;color:#0b1020}
.pg{width:8.5in;height:11in;position:relative;page-break-after:always;overflow:hidden}
.hdr{display:flex;align-items:center;gap:10px;font-weight:800;font-size:13pt}.hdr img{height:30px}.hdr b span{color:#0f9e94}
.ft{position:absolute;bottom:.35in;left:.5in;right:.5in;font-size:8pt;color:#7a839e;display:flex;justify-content:space-between}
</style>'''
# ---------- Flash cards ----------
cards=d['flashcards']; per=8
pages=[cards[i:i+per] for i in range(0,len(cards),per)]
W,H=3.6,2.35
def grid(items, back=False):
    cells=[]
    for r in range(4):
        row=items[r*2:r*2+2]
        row=row+[None]*(2-len(row))
        if back: row=row[::-1]  # espejo para impresión a doble cara (borde largo)
        cells+=row
    out=''
    for c in cells:
        if c is None: out+='<div class="fc empty"></div>'; continue
        if not back:
            out+=f'<div class="fc"><span class="tema">{e(c["tema"])}</span><p>{e(c["frente"])}</p><img src="{logo}"></div>'
        else:
            out+=f'<div class="fc b"><span class="tema">Respuesta · {e(c["tema"])}</span><p>{e(c["reverso"])}</p></div>'
    return out
fc_css='''<style>.sheet{position:absolute;top:.75in;left:.5in;display:grid;grid-template-columns:repeat(2,3.6in);grid-auto-rows:2.35in;gap:0 .3in}
.fc{border:1px dashed #b8bfd6;padding:.22in .25in;display:flex;flex-direction:column;justify-content:center;position:relative;margin-bottom:.12in}
.fc .tema{position:absolute;top:.14in;left:.25in;font-size:7.5pt;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#0f9e94}
.fc p{margin:0;font-size:13pt;font-weight:700;line-height:1.3}
.fc img{position:absolute;right:.16in;bottom:.12in;height:22px;opacity:.85}
.fc.b{background:#eef9f8}.fc.b p{font-weight:500;font-size:12pt}.fc.empty{border-color:transparent}
.top{position:absolute;top:.3in;left:.5in;right:.5in;display:flex;justify-content:space-between;align-items:center}
.top small{color:#7a839e;font-size:8pt}</style>'''
body=''
for n,pgc in enumerate(pages,1):
    body+=f'<div class="pg"><div class="top"><div class="hdr"><img src="{logo}"><b>Kronos<span>Medicine</span></b></div><small>{e(TEMA)} · Flash cards · Hoja {n} (frente)</small></div><div class="sheet">{grid(pgc)}</div><div class="ft"><span>Recorta por la línea punteada.</span><span>kronosmedicine.com.mx</span></div></div>'
    body+=f'<div class="pg"><div class="top"><div class="hdr"><img src="{logo}"><b>Kronos<span>Medicine</span></b></div><small>Hoja {n} (reverso) · imprime a doble cara, giro por el borde largo</small></div><div class="sheet">{grid(pgc,True)}</div><div class="ft"><span>Repasa unas cuantas cada día durante la semana.</span><span>kronosmedicine.com.mx</span></div></div>'
open(f'{OUT}/flash.html','w',encoding='utf-8').write(f'<html><head><meta charset="utf-8">{BASE}{fc_css}</head><body>{body}</body></html>')

# ---------- Examen ----------
ex=d['examen']
# Examen impreso: 20 preguntas repartidas entre los temas
import random
_r=random.Random(CID); _por={}
for q in ex['preguntas']: _por.setdefault(q['tema'],[]).append(q)
_g=list(_por.values()); qs=[]
while len(qs)<min(20,len(ex['preguntas'])):
    for g in _g:
        if g and len(qs)<20: qs.append(g.pop(0))
L='ABCD'
ex_css='''<style>.pad{padding:.5in .6in .7in}.title{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #0f9e94;padding-bottom:8px;margin-bottom:12px}
h1{font-size:20pt;margin:6px 0 0}.meta{font-size:9pt;color:#4a5272}.datos{display:grid;grid-template-columns:2fr 1fr 1fr;gap:14px;font-size:9.5pt;margin:8px 0 14px}.datos span{border-bottom:1px solid #9aa3bf;padding-bottom:3px}
.inst{background:#eef9f8;border-left:4px solid #0f9e94;padding:8px 12px;font-size:9pt;margin-bottom:12px}
.q{break-inside:avoid;margin-bottom:11px;font-size:9.6pt}.q .caso{margin:0 0 2px}.q .p{font-weight:700;margin:0 0 4px}.q ol{margin:0;padding-left:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:2px 16px}
.q li b{display:inline-block;width:16px}.cols{column-count:1}
.hoja{display:grid;grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(10,auto);grid-auto-flow:column;gap:6px 40px;margin-top:10px}.fila{display:flex;align-items:center;gap:12px;font-size:11pt}.fila .n{width:26px;text-align:right;font-weight:700}
.bub{width:24px;height:24px;border:1.5px solid #4a5272;border-radius:50%;display:grid;place-items:center;font-size:8.5pt;color:#4a5272}
.k{break-inside:avoid;font-size:9.4pt;margin-bottom:9px;padding:6px 10px;border-left:3px solid #0f9e94;background:#f6f8fc}
.k b.r{color:#0f9e94}.tag{font-size:7.5pt;font-weight:800;color:#7a839e;text-transform:uppercase;letter-spacing:.08em}
.tabla{width:100%;border-collapse:collapse;font-size:9.5pt;margin-top:8px}.tabla td,.tabla th{border:1px solid #d6dbea;padding:5px 8px;text-align:left}
</style>'''
def header(t, sub):
    return f'<div class="title"><div><div class="hdr"><img src="{logo}"><b>Kronos<span>Medicine</span></b></div><h1>{t}</h1></div><div class="meta">{sub}</div></div>'
qhtml=''.join(f'<div class="q"><p class="caso">{i+1}. {e(q["caso"])}</p><p class="p">{e(q["pregunta"])}</p><ol>{"".join(f"<li><b>{L[k]})</b> {e(o)}</li>" for k,o in enumerate(q["opciones"]))}</ol></div>' for i,q in enumerate(qs))
exam=f'''<div class="pad">{header(f"Examen cronometrado: {e(TEMA)}", f"{len(qs)} preguntas · {ex['minutos']} minutos<br>Aprobatorio: {ex['aprobatorio']}%")}
<div class="datos"><span>Nombre:</span><span>Fecha:</span><span>Calificación:</span></div>
<div class="inst"><b>Instrucciones:</b> lee cada caso y elige una sola respuesta. Anota tus respuestas en la hoja de respuestas. Tienes {ex['minutos']} minutos; empieza cuando te lo indiquen.</div>
{qhtml}</div>'''
filas=''.join(f'<div class="fila"><span class="n">{i+1}</span>'+''.join(f'<span class="bub">{l}</span>' for l in L)+'</div>' for i in range(len(qs)))
hoja=f'''<div class="pg"><div class="pad">{header("Hoja de respuestas", f"{e(TEMA)}<br>Rellena un solo círculo por pregunta")}
<div class="datos"><span>Nombre:</span><span>Fecha:</span><span>Hora de inicio / fin:</span></div>
<div class="hoja">{filas}</div>
<table class="tabla" style="margin-top:28px"><tr><th>Correctas</th><th>Incorrectas</th><th>Sin responder</th><th>Calificación (%)</th></tr><tr><td style="height:30px"></td><td></td><td></td><td></td></tr></table>
</div><div class="ft"><span>Calificación = correctas ÷ {len(qs)} × 100</span><span>kronosmedicine.com.mx</span></div></div>'''
temas={}
for i,q in enumerate(qs): temas.setdefault(q['tema'],[]).append(i+1)
clave_rows=''.join(f'<div class="k"><span class="tag">{e(q["tema"])}</span><br><b>{i+1}.</b> <b class="r">{L[q["correcta"]]}) {e(q["opciones"][q["correcta"]])}</b><br>{e(q["explicacion"])}</div>' for i,q in enumerate(qs))
mods={m['id']:(n+1,m['titulo']) for n,m in enumerate(d['modulos'])}
tabla=''.join(f'<tr><td>{e(t)}</td><td>{", ".join(map(str,v))}</td><td>Módulo {mods[qs[v[0]-1]["modulo"]][0]}: {e(mods[qs[v[0]-1]["modulo"]][1])}</td></tr>' for t,v in temas.items())
clave=f'''<div class="pad">{header("Clave de respuestas y explicaciones", "Solo para el docente o<br>para revisar al terminar")}
{clave_rows}
<h3 style="font-size:12pt;margin:16px 0 4px">Resultado por tema</h3><p style="font-size:9pt;margin:0">Si en un tema aciertas menos del 70%, repasa el módulo indicado de la ruta de estudio.</p>
<table class="tabla"><tr><th>Tema</th><th>Preguntas</th><th>Qué repasar</th></tr>{tabla}</table></div>'''
open(f'{OUT}/examen.html','w',encoding='utf-8').write(f'<html><head><meta charset="utf-8">{BASE}{ex_css}<style>@page{{margin:0}}</style></head><body>{exam}</body></html>')
open(f'{OUT}/hoja.html','w',encoding='utf-8').write(f'<html><head><meta charset="utf-8">{BASE}{ex_css}</head><body>{hoja}</body></html>')
open(f'{OUT}/clave.html','w',encoding='utf-8').write(f'<html><head><meta charset="utf-8">{BASE}{ex_css}</head><body>{clave}</body></html>')

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg=await b.new_page()
        for name in ['flash','hoja']:
            await pg.goto(f'file://{OUT}/{name}.html'); await pg.wait_for_timeout(300)
            await pg.pdf(path=f'{OUT}/{name}.pdf', width='8.5in', height='11in', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
        for name in ['examen','clave']:
            await pg.goto(f'file://{OUT}/{name}.html'); await pg.wait_for_timeout(300)
            await pg.pdf(path=f'{OUT}/{name}.pdf', width='8.5in', height='11in', print_background=True, margin={'top':'0.3in','bottom':'0.5in','left':'0','right':'0'},
                display_header_footer=True, header_template='<span></span>',
                footer_template=('<div style="font-size:7pt;color:#7a839e;width:100%;padding:0 .6in;display:flex;justify-content:space-between;font-family:Inter,sans-serif"><span>KronosMedicine · '+TEMA+'</span><span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span></div>').replace("'+TEMA+'",TEMA))
        # Infografías: PNG 2x y PDF
        import re
        for svg in [f'{CID}-infografia', f'{CID}-algoritmo']:
            _t=open(f'{R}/assets/img/infografias/{svg}.svg',encoding='utf-8').read(); w=int(re.search(r'width="(\d+)"',_t).group(1)); h=int(re.search(r'height="(\d+)"',_t).group(1))
            p2=await b.new_page(viewport={'width':w,'height':h})
            svgtxt=open(f'{R}/assets/img/infografias/{svg}.svg',encoding='utf-8').read()
            await p2.goto('about:blank')
            await p2.set_content(f'<html><head><style>body{{margin:0;background:#0b1020}} svg{{width:100%;height:auto;display:block}}</style></head><body>{svgtxt}</body></html>')
            await p2.wait_for_timeout(300)
            await p2.pdf(path=f'{OUT}/{svg}.pdf', width=f'{w/96}in', height=f'{h/96}in', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
            await p2.close()
        await b.close()
asyncio.run(main())
print('ok')

import shutil
D=f'{R}/assets/descargas'
for src,dst in [('flash.pdf','flash-cards'),('examen.pdf','examen'),('hoja.pdf','hoja')]:
    shutil.copy(f'{OUT}/{src}', f'{D}/{CID}_{dst}.pdf')
shutil.copy(f'{OUT}/{CID}-infografia.pdf', f'{D}/{CID}_infografia.pdf')
shutil.copy(f'{OUT}/{CID}-algoritmo.pdf', f'{D}/{CID}_diagrama.pdf')
os.makedirs('/home/claude/entrega/cursos', exist_ok=True)
shutil.copy(f'{OUT}/clave.pdf', f'/home/claude/entrega/cursos/{CID}_clave-de-respuestas.pdf')
print('PDFs', CID)
