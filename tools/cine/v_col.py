import math, random
from cine import Video

DEFS = '''
<linearGradient id="liver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9b3a32"/><stop offset="1" stop-color="#4a1312"/></linearGradient>
<radialGradient id="bile" cx="45%" cy="40%" r="70%"><stop offset="0" stop-color="#bef264"/><stop offset=".6" stop-color="#65a30d"/><stop offset="1" stop-color="#2f4f0a"/></radialGradient>
<linearGradient id="stone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fef3c7"/><stop offset=".5" stop-color="#d4a017"/><stop offset="1" stop-color="#7c4a03"/></linearGradient>
<linearGradient id="fan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0f2fe" stop-opacity=".35"/><stop offset="1" stop-color="#e0f2fe" stop-opacity=".05"/></linearGradient>
<pattern id="scan" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 6 H12" stroke="#fff" stroke-opacity=".08" stroke-width="2"/></pattern>
<clipPath id="gbclip"><path d="M 440 690 C 470 650 540 660 560 700 C 620 800 760 900 790 1050 C 815 1180 720 1260 620 1230 C 520 1200 500 1100 480 980 C 460 860 420 760 440 690 Z"/></clipPath>
'''
GB = 'M 440 690 C 470 650 540 660 560 700 C 620 800 760 900 790 1050 C 815 1180 720 1260 620 1230 C 520 1200 500 1100 480 980 C 460 860 420 760 440 690 Z'
rnd = random.Random(5)
STONES = [(640, 1140, 34), (705, 1085, 27), (585, 1175, 28), (695, 1175, 22), (612, 1065, 21), (560, 1105, 18)]

def poly(cx, cy, r, seed):
    rr = random.Random(seed); n = rr.randint(6, 8); pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rr.uniform(-.2, .2); k = r * rr.uniform(.8, 1.1)
        pts.append(f'{k * math.cos(a):.1f},{k * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + 'Z'

APEX = (950, 600)
def fan():
    a0 = math.atan2(1100 - APEX[1], 650 - APEX[0]); R = 760; sp = math.radians(24)
    p1 = (APEX[0] + R * math.cos(a0 - sp), APEX[1] + R * math.sin(a0 - sp)); p2 = (APEX[0] + R * math.cos(a0 + sp), APEX[1] + R * math.sin(a0 + sp))
    return f'M {APEX[0]} {APEX[1]} L {p1[0]:.0f} {p1[1]:.0f} A {R} {R} 0 0 1 {p2[0]:.0f} {p2[1]:.0f} Z', math.degrees(a0)

def svg():
    LIV = ['<path d="M -100 180 C 200 120 700 140 1180 260 L 1180 640 C 900 700 640 640 460 610 C 300 580 120 610 -100 650 Z" fill="url(#liver)" filter="url(#soft)"/>',
         '<path d="M 0 230 C 300 180 700 200 1100 300" stroke="#e07a6a" stroke-opacity=".25" stroke-width="18" fill="none" filter="url(#blur8)"/>']
    s = [
         '<path d="M -50 1390 C 200 1310 450 1340 700 1470" stroke="#d6907f" stroke-width="110" stroke-linecap="round" fill="none" opacity=".85"/>',
         '<path d="M -50 1390 C 200 1310 450 1340 700 1470" stroke="#f1b4a4" stroke-width="20" stroke-linecap="round" fill="none" opacity=".35"/>']
    duct = 'stroke-width="30" stroke-linecap="round" fill="none"'
    for d in ['M 300 240 L 300 575', 'M 452 690 C 420 640 360 600 300 578', 'M 300 570 C 300 800 280 1000 250 1330']:
        s.append(f'<path d="{d}" stroke="#4d7c0f" {duct}/><path d="{d}" stroke="#a3e635" stroke-opacity=".35" stroke-width="8" stroke-linecap="round" fill="none"/>')
    s.append('<path id="flow" d="M 300 240 L 300 572 C 360 600 420 640 452 690 L 540 820" fill="none" stroke="none"/>')
    s.append('<g filter="url(#glow)">' + ''.join(f'<circle id="fd{i}" r="8" fill="#d9f99d" opacity="0"/>' for i in range(16)) + '</g>')
    s.extend(LIV)
    s.append(f'<path id="halo" d="{GB}" fill="none" stroke="#ef4444" stroke-width="80" filter="url(#blur8)" opacity="0"/>')
    s.append(f'<path id="gbf" d="{GB}" fill="url(#bile)" opacity=".9" filter="url(#soft)"/>')
    s.append('<g clip-path="url(#gbclip)"><ellipse cx="580" cy="860" rx="90" ry="200" fill="#ecfccb" opacity=".18" filter="url(#blur8)"/></g>')
    fp, ang = fan()
    s.append('<g id="shadows" opacity="0">' + ''.join(
        f'<g transform="translate({x} {y}) rotate({ang - 90:.1f})"><rect x="{-r*0.8:.0f}" y="0" width="{r*1.6:.0f}" height="260" fill="#000" opacity=".55" filter="url(#blur8)"/></g>' for x, y, r in STONES) + '</g>')
    s.append('<g id="stones">' + ''.join(
        f'<g id="s{i}" transform="translate({x} {y}) scale(0)"><path d="{poly(0,0,r,i)}" fill="url(#stone)" stroke="#78350f" stroke-width="3"/><path d="{poly(0,0,r*.45,i+9)}" fill="#fff" opacity=".25"/></g>' for i, (x, y, r) in enumerate(STONES)) + '</g>')
    s.append(f'<g id="sx" transform="scale(0)"><path d="{poly(0,0,24,42)}" fill="url(#stone)" stroke="#78350f" stroke-width="3"/></g>')
    s.append('<path id="route" d="M 600 1010 C 540 900 480 790 452 712" fill="none" stroke="none"/>')
    s.append(f'<path id="gbw" d="{GB}" fill="none" stroke="#3f7d4a" stroke-width="10"/>')
    s.append('<circle id="block" cx="452" cy="706" r="44" fill="none" stroke="#f87171" stroke-width="8" filter="url(#glow)" opacity="0"/>')
    s.append(f'<g id="fang" opacity="0"><path d="{fp}" fill="url(#fan)"/><path d="{fp}" fill="url(#scan)"/>'
             f'<g transform="translate({APEX[0]} {APEX[1]}) rotate({ang - 90:.1f})"><rect x="-70" y="-120" width="140" height="130" rx="30" fill="#cbd5e1"/><rect x="-60" y="-10" width="120" height="22" rx="8" fill="#334155"/></g>'
             '<line id="sweep" x1="0" y1="0" x2="0" y2="0" stroke="#e0f2fe" stroke-width="6" filter="url(#glow)"/></g>')
    return ''.join(s), ang

SVG, ANG = svg()
JS = (r'''
const ST=__ST__;
const flow = document.getElementById('flow'), FL = flow.getTotalLength();
const bf = S(t,.4,1.2)*(1-S(t,10.6,11.4));
for(let i=0;i<16;i++){ const u=(t*.14+i/16)%1; const p=flow.getPointAtLength(u*FL); A('fd'+i,'cx',p.x); A('fd'+i,'cy',p.y); O('fd'+i, bf*Math.sin(u*Math.PI)) }
ST.forEach((s,i)=>{ const q=out(P(t,5.0+i*.28,6.2+i*.28)); TT('s'+i,`translate(${s[0]} ${s[1]}) scale(${q}) rotate(${t*4+i*20})`);
  const e=$('s'+i).firstChild; e.setAttribute('stroke', t>18.6 ? '#fff' : '#78350f'); e.setAttribute('stroke-width', 3+4*S(t,19.2,19.8)) });
const route=$('route'), RL=route.getTotalLength(); const m=S(t,9.4,11.2); const pt=route.getPointAtLength(m*RL);
TT('sx',`translate(${pt.x} ${pt.y}) scale(${out(P(t,6.0,7.2))}) rotate(${t*10})`);
O('block', S(t,11.1,11.5)*(.6+.4*Math.sin(t*6)));
const inf = S(t,13.9,15.6);
A('gbw','stroke-width', 10+18*inf);
const c1=[63,125,74], c2=[234,88,12]; A('gbw','stroke',`rgb(${c1.map((v,i)=>Math.round(L(v,c2[i],inf))).join(',')})`);
O('halo', .5*inf*(.75+.25*Math.sin(t*4)));
const fg=S(t,18.8,19.6); O('fang', fg); O('shadows', fg*.9);
const sw = Math.sin(t*1.6)*22*Math.PI/180, base=(__ANG__)*Math.PI/180;
A('sweep','x1',__AX__); A('sweep','y1',__AY__); A('sweep','x2',__AX__+760*Math.cos(base+sw)); A('sweep','y2',__AY__+760*Math.sin(base+sw));
''').replace('__ST__', str([list(s) for s in STONES])).replace('__ANG__', f'{ANG:.2f}').replace('__AX__', str(APEX[0])).replace('__AY__', str(APEX[1]))

def make():
    return Video('colecistitis', 'Cirugía', 'Colecistitis aguda', 'De la litiasis a la colecistectomía',
                 '#a3e635', '#84cc16', SVG, JS,
                 '[[0,1.0,540,760],[4.6,1.22,620,1060],[9.2,1.3,520,840],[13.8,1.08,600,960],[18.4,0.98,660,930],[23,1.03,660,940]]',
                 [(0.6, 4.5, 'La vesícula <b>almacena y concentra</b> la bilis.'),
                  (4.8, 9.1, 'Si la bilis se sobresatura, se forman <b>cálculos</b>.'),
                  (9.4, 13.7, 'Un cálculo <b>obstruye el conducto cístico</b>…'),
                  (14.0, 18.3, '…y la vesícula se <b>inflama</b>: colecistitis aguda.'),
                  (18.6, 22.7, 'Ultrasonido para confirmar y <b>colecistectomía temprana</b>.')],
                 [(14.4, 18.2, 'Dolor > 6 h · fiebre · Murphy positivo'),
                  (19.0, 22.8, 'Ultrasonido: estudio de elección'),
                  (19.6, 22.8, 'Colecistectomía laparoscópica temprana (< 72 h)')],
                 [(4.6, 'whoosh')] + [(5.0 + i * .28, 'tick') for i in range(6)] + [(9.2, 'whoosh'), (11.2, 'boom'), (13.8, 'whoosh'), (18.4, 'whoosh'), (19.4, 'chime')],
                 DEFS)
