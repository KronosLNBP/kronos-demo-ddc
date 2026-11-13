import math, random
from cine import Video

DEFS = '''
<linearGradient id="epi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1d3bd"/><stop offset="1" stop-color="#dcae8f"/></linearGradient>
<linearGradient id="der" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9a9a3"/><stop offset="1" stop-color="#c97b7c"/></linearGradient>
<linearGradient id="hyp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1d995"/><stop offset="1" stop-color="#c9a85c"/></linearGradient>
<linearGradient id="topf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a17c"/><stop offset="1" stop-color="#ecc3a3"/></linearGradient>
<radialGradient id="skin" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#eec4a4"/><stop offset=".8" stop-color="#d49e7c"/><stop offset="1" stop-color="#d49e7c" stop-opacity="0"/></radialGradient>
<radialGradient id="mcell" cx="40%" cy="35%" r="65%"><stop offset="0" stop-color="#6b4a3a"/><stop offset="1" stop-color="#22120c"/></radialGradient>
<clipPath id="slabclip"><rect x="60" y="560" width="960" height="860"/></clipPath>
'''
rnd = random.Random(21)
MAL = sorted([(580 + rnd.gauss(0, 120), rnd.uniform(600, 695), rnd.uniform(12, 19)) for _ in range(26)], key=lambda c: abs(c[0] - 580))
INV = sorted([(580 + rnd.gauss(0, 70), rnd.uniform(720, 990), rnd.uniform(12, 18)) for _ in range(20)], key=lambda c: c[1])
MEL = [(100 + i * 92 + rnd.uniform(-10, 10)) for i in range(10)]
GRN = [(rnd.choice(MEL) + rnd.uniform(-30, 30), rnd.uniform(0, 1)) for _ in range(36)]

def blob(cx, cy, r, amp, seed, n=80):
    rr = random.Random(seed); ph = [rr.uniform(0, 6.28) for _ in range(4)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = r * (1 + amp * (.5 * math.sin(3 * a + ph[0]) + .3 * math.sin(5 * a + ph[1]) + .2 * math.sin(9 * a + ph[2])))
        pts.append(f'{cx + k * math.cos(a):.1f},{cy + k * math.sin(a) * .92:.1f}')
    return 'M' + ' L'.join(pts) + 'Z'

def svg():
    s = ['<g id="slab">']
    s.append('<path d="M 60 560 L 1020 560 L 1080 470 L 120 470 Z" fill="url(#topf)"/>')
    s.append('<g id="mole" transform="translate(600 515) scale(1 .28)"><path id="mole0" d="' + blob(0, 0, 70, .12, 1) + '" fill="#4a2a1c"/>'
             '<path id="mole1" d="' + blob(10, 0, 120, .35, 2) + '" fill="#2a160e" opacity="0"/><path id="mole2" d="' + blob(-30, 10, 70, .4, 3) + '" fill="#6d2a1e" opacity="0"/></g>')
    s.append('<path d="M 1020 560 L 1080 470 L 1080 1330 L 1020 1420 Z" fill="#8a5a4a"/>')
    s.append('<rect x="60" y="1150" width="960" height="270" fill="url(#hyp)"/>')
    rr = random.Random(4)
    for i in range(16):
        x = 90 + (i % 8) * 120 + rr.uniform(-15, 15); y = 1205 + (i // 8) * 115 + rr.uniform(-10, 10)
        s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr.uniform(48,62):.0f}" ry="{rr.uniform(40,52):.0f}" fill="#f8e7b0" stroke="#e0c070" stroke-width="3"/>')
    s.append('<rect x="60" y="700" width="960" height="450" fill="url(#der)"/>')
    for i in range(12):
        y = 760 + i * 32
        s.append(f'<path d="M 60 {y} C 250 {y-14} 450 {y+14} 650 {y} S 900 {y-12} 1020 {y}" stroke="#f6cdc6" stroke-width="4" fill="none" opacity=".55"/>')
    for x in range(110, 1000, 120):
        s.append(f'<path d="M {x} 1000 C {x} 800 {x+10} 730 {x+30} 725 C {x+50} 730 {x+60} 800 {x+60} 1000" stroke="#c0262d" stroke-width="6" fill="none" opacity=".75"/>')
    s.append('<rect x="60" y="560" width="960" height="140" fill="url(#epi)"/>')
    s.append('<rect x="60" y="560" width="960" height="20" fill="#f6e3d3"/>')
    for row in range(3):
        for i in range(21):
            x = 72 + i * 46 + (23 if row % 2 else 0); y = 600 + row * 34
            if x > 1010: continue
            s.append(f'<rect x="{x}" y="{y}" width="40" height="28" rx="12" fill="none" stroke="#cf9d7d" stroke-width="2" opacity=".7"/>')
    s.append('<g id="grn">' + ''.join(f'<circle id="gn{i}" r="4" fill="#5b3a29" opacity="0"/>' for i in range(len(GRN))) + '</g>')
    s.append('<g id="mels" filter="url(#glow)">' + ''.join(
        f'<g><path d="M {x} 700 L {x-26} 650 M {x} 700 L {x+4} 640 M {x} 700 L {x+28} 655" stroke="#5b3a29" stroke-width="5" stroke-linecap="round"/><circle cx="{x}" cy="702" r="16" fill="url(#mcell)"/></g>' for x in MEL) + '</g>')
    s.append('<g id="mal">' + ''.join(
        f'<g id="m{i}" transform="translate({x:.0f} {y:.0f}) scale(0)"><circle r="{r:.0f}" fill="#24130d" stroke="#a855f7" stroke-opacity=".6" stroke-width="3"/><circle r="{r*.45:.0f}" fill="#6b21a8" opacity=".7"/></g>' for i, (x, y, r) in enumerate(MAL)) + '</g>')
    s.append('<g id="inv">' + ''.join(
        f'<g id="v{i}" transform="translate({x:.0f} {y:.0f}) scale(0)"><circle r="{r:.0f}" fill="#24130d" stroke="#c084fc" stroke-opacity=".7" stroke-width="3"/><circle r="{r*.45:.0f}" fill="#7e22ce" opacity=".75"/></g>' for i, (x, y, r) in enumerate(INV)) + '</g>')
    deep = max(c[1] for c in INV) + 16
    tick = ''.join(f'<line x1="840" x2="{860 if k % 2 == 0 else 852}" y1="{580 + k*40}" y2="{580 + k*40}" stroke="#fff" stroke-width="3"/>' for k in range(int((deep - 580) / 40) + 1))
    s.append(f'<g id="ruler" opacity="0"><line id="rl" data-len="auto" x1="840" y1="580" x2="840" y2="{deep:.0f}" stroke="#fff" stroke-width="5" filter="url(#glow)"/>{tick}'
             f'<line x1="600" x2="840" y1="{deep:.0f}" y2="{deep:.0f}" stroke="#fff" stroke-dasharray="10 8" stroke-width="3"/>'
             f'<line x1="200" x2="840" y1="580" y2="580" stroke="#fff" stroke-dasharray="10 8" stroke-width="3" opacity=".6"/>'
             f'<text x="870" y="{(580+deep)/2:.0f}" font-family="Inter,sans-serif" font-size="34" font-weight="800" fill="#fff">Breslow</text>'
             f'<text x="870" y="{(580+deep)/2+40:.0f}" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#e9d5ff">mm de profundidad</text></g>')
    s.append('</g>')
    # vista superior para el ABCDE
    s.append('<g id="topv" opacity="0">')
    s.append('<circle cx="540" cy="800" r="470" fill="url(#skin)"/>')
    s.append(f'<path d="{blob(540, 800, 210, .28, 7)}" fill="#5b3a29" filter="url(#soft)"/>')
    s.append(f'<path d="{blob(500, 770, 130, .4, 8)}" fill="#1f120c"/>')
    s.append(f'<path d="{blob(620, 860, 70, .5, 9)}" fill="#8b2a22" opacity=".75"/>')
    s.append(f'<path d="{blob(460, 880, 55, .5, 10)}" fill="#64748b" opacity=".65"/>')
    s.append(f'<path d="{blob(600, 720, 40, .5, 11)}" fill="#a16207" opacity=".7"/>')
    s.append('<g class="fx" data-a="14.5" data-b="18.4" style="opacity:0"><line x1="540" y1="540" x2="540" y2="1060" stroke="#fff" stroke-width="4" stroke-dasharray="14 10"/><line x1="280" y1="800" x2="800" y2="800" stroke="#fff" stroke-width="4" stroke-dasharray="14 10"/></g>')
    s.append('<g class="fx" data-a="16.3" data-b="18.4" style="opacity:0"><line x1="300" y1="500" x2="790" y2="500" stroke="#c084fc" stroke-width="6"/><line x1="300" y1="480" x2="300" y2="520" stroke="#c084fc" stroke-width="6"/><line x1="790" y1="480" x2="790" y2="520" stroke="#c084fc" stroke-width="6"/><text x="545" y="465" text-anchor="middle" font-family="Inter,sans-serif" font-size="36" font-weight="800" fill="#fff">&gt; 6 mm</text></g>')
    s.append('<ellipse id="exc" data-len="auto" cx="540" cy="800" rx="380" ry="270" fill="none" stroke="#c084fc" stroke-width="7" stroke-dasharray="1" filter="url(#glow)" opacity="0"/>')
    s.append('</g>')
    return ''.join(s)

JS = (r'''
const MAL=__MAL__, INV=__INV__, GRN=__GRN__;
const gl=.6+.4*Math.sin(t*3); $('mels').style.opacity = .75+.25*gl*S(t,.6,1.4);
GRN.forEach((g,i)=>{ const f=(t*.35+g[1])%1; A('gn'+i,'cx',g[0]+Math.sin(f*6+i)*6); A('gn'+i,'cy',696-f*105); O('gn'+i, S(t,.8,1.6)*(1-S(t,13.6,14.2))*Math.sin(f*Math.PI)) });
MAL.forEach((c,i)=>{ const q=out(P(t,5.0+i*.13,5.6+i*.13)); TT('m'+i,`translate(${c[0]} ${c[1]}) scale(${q*(1+.06*Math.sin(t*4+i))})`) });
INV.forEach((c,i)=>{ const q=out(P(t,9.4+i*.12,10.0+i*.12)); TT('v'+i,`translate(${c[0]} ${c[1]-30*(1-q)}) scale(${q})`) });
const g=S(t,5.2,8.5); TT('mole',`translate(600 515) scale(${1+.5*g} ${.28*(1+.5*g)})`); O('mole1', g); O('mole2', g*.9);
O('ruler', S(t,11.3,11.7)); draw('rl', S(t,11.4,12.8));
O('slab', 1-S(t,13.8,14.6)); O('topv', S(t,14.0,14.8));
const ep=S(t,19.0,20.6); O('exc', S(t,18.9,19.2)); const ex=$('exc'); const LEN=+ex.dataset.len; ex.style.strokeDasharray=`${LEN*ep} ${LEN}`;
''').replace('__MAL__', str([[round(a, 1) for a in c] for c in MAL])).replace('__INV__', str([[round(a, 1) for a in c] for c in INV])).replace('__GRN__', str([[round(a, 2) for a in c] for c in GRN]))

def make():
    return Video('melanoma', 'Dermatología', 'Melanoma', 'Del melanocito al índice de Breslow',
                 '#c084fc', '#a855f7', svg(), JS,
                 '[[0,1.0,560,860],[4.6,1.25,590,690],[9.2,1.0,680,830],[13.8,1.0,680,830],[14.6,0.95,540,1130],[18.4,0.95,540,1130],[23,1.0,540,1100]]',
                 [(0.6, 4.5, 'Los <b>melanocitos</b> producen el pigmento de la piel.'),
                  (4.8, 9.1, 'En el melanoma crecen <b>sin control</b>…'),
                  (9.4, 13.7, '…e <b>invaden la dermis</b>. Esa profundidad es el <b>índice de Breslow</b>.'),
                  (14.0, 18.3, 'Sospecha con el <b>ABCDE</b>.'),
                  (18.6, 22.7, 'Lesión sospechosa: <b>biopsia escisional</b>.')],
                 [(14.5, 18.2, 'A · Asimetría'), (15.1, 18.2, 'B · Bordes irregulares'), (15.7, 18.2, 'C · Color heterogéneo'),
                  (16.3, 18.2, 'D · Diámetro > 6 mm'), (16.9, 18.2, 'E · Evolución'),
                  (19.0, 22.8, 'Biopsia escisional con márgenes estrechos'),
                  (19.6, 22.8, 'Breslow: factor pronóstico más importante')],
                 [(4.6, 'whoosh'), (9.2, 'whoosh'), (13.8, 'whoosh')] + [(14.5 + k * .6, 'tick') for k in range(5)] + [(18.4, 'whoosh'), (19.2, 'chime')],
                 DEFS)
