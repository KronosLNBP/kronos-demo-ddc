import math, random
from cine import Video

DEFS = '''
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e06a7c"/><stop offset="1" stop-color="#8f2236"/></linearGradient>
<linearGradient id="wall2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e06a7c"/><stop offset="1" stop-color="#8f2236"/></linearGradient>
<linearGradient id="lumen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0508"/><stop offset=".5" stop-color="#5c1019"/><stop offset="1" stop-color="#2a0508"/></linearGradient>
<radialGradient id="rbc" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#ff6b6b"/><stop offset=".7" stop-color="#d11f2c"/><stop offset="1" stop-color="#8a0d16"/></radialGradient>
<radialGradient id="mast" cx="42%" cy="38%" r="65%"><stop offset="0" stop-color="#e3a6c6"/><stop offset=".7" stop-color="#a3528a"/><stop offset="1" stop-color="#5e2152"/></radialGradient>
<radialGradient id="brong" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#f3b9bf"/><stop offset="1" stop-color="#a64e5c"/></radialGradient>
<linearGradient id="injg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e0f2fe"/><stop offset="1" stop-color="#7dd3fc"/></linearGradient>
'''

rnd = random.Random(3)
RBC = [(rnd.uniform(0, 1500), rnd.uniform(-105, 105), rnd.uniform(70, 120), rnd.uniform(0, 6.28)) for _ in range(34)]
GR = []
while len(GR) < 44:
    r = rnd.uniform(20, 148); a = rnd.uniform(0, 6.28); x, y = r * math.cos(a), r * math.sin(a)
    if (x + 30) ** 2 / 75 ** 2 + (y - 20) ** 2 / 60 ** 2 < 1: continue
    GR.append((x, y, rnd.uniform(8, 13)))
HIS = [(rnd.uniform(0, 6.28), rnd.uniform(60, 150), rnd.uniform(260, 680), rnd.uniform(0, .8)) for _ in range(70)]
REC = [(-160 + i * 17.5) for i in range(9)]
LEAK = [(rnd.uniform(-60, 1140), rnd.choice([-1, 1]), rnd.uniform(0, 1)) for _ in range(34)]

def star(cx, cy, r1, r2, n=9):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2; a = math.pi * i / n
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + 'Z'

def svg():
    s = ['<g id="vessel">']
    s.append('<rect id="lum" x="-200" y="900" width="1500" height="280" fill="url(#lumen)"/>')
    s.append('<g id="rbcs">' + ''.join(
        f'<g id="r{i}"><ellipse rx="36" ry="16" fill="url(#rbc)"/><ellipse rx="17" ry="6" fill="#9b111e" opacity=".55"/></g>' for i in range(len(RBC))) + '</g>')
    s.append('<g id="leak">' + ''.join(f'<circle id="lk{i}" r="7" fill="#fde68a" opacity="0"/>' for i in range(len(LEAK))) + '</g>')
    s.append('<g id="wt">' + ''.join(f'<rect class="seg" data-x="{x}" x="{x}" y="860" width="124" height="40" rx="18" fill="url(#wall)"/>' for x in range(-180, 1240, 130)) + '</g>')
    s.append('<g id="wb">' + ''.join(f'<rect class="seg" data-x="{x}" x="{x}" y="1180" width="124" height="40" rx="18" fill="url(#wall2)"/>' for x in range(-180, 1240, 130)) + '</g>')
    s.append('</g>')
    # mastocito
    s.append('<g id="mastg" transform="translate(540 470)">')
    s.append('<circle id="memb" r="170" fill="url(#mast)" stroke="#f5c6dd" stroke-opacity=".6" stroke-width="4" filter="url(#soft)"/>')
    s.append('<ellipse cx="-30" cy="20" rx="72" ry="56" fill="#4c1d4f" opacity=".85"/>')
    for i, a in enumerate(REC):
        r = math.radians(a); x, y = 172 * math.cos(r), 172 * math.sin(r)
        s.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({a + 90:.1f})"><path d="M0 0 L0 -18 M0 -18 L-9 -32 M0 -18 L9 -32" stroke="#fde2f3" stroke-width="5" stroke-linecap="round" fill="none"/></g>')
    s.append('</g>')
    s.append('<g id="grans" filter="url(#glow)">' + ''.join(f'<circle id="g{i}" r="{r:.1f}" fill="#8b5cf6"/>' for i, (x, y, r) in enumerate(GR)) + '</g>')
    s.append('<g id="hist" filter="url(#glow)">' + ''.join(f'<circle id="h{i}" r="5" fill="#fbbf24" opacity="0"/>' for i in range(len(HIS))) + '</g>')
    s.append('<g id="alg" filter="url(#glow)">' + ''.join(f'<path id="al{i}" d="{star(0, 0, 22, 11)}" fill="#facc15"/>' for i in range(6)) + '</g>')
    # bronquio
    s.append('<g id="bron" transform="translate(540 470)" opacity="0">'
             '<circle r="236" fill="url(#brong)" filter="url(#soft)"/>'
             '<path d="M -150 -180 A 236 236 0 1 0 150 -180" fill="none" stroke="#f5ebe0" stroke-width="26" stroke-linecap="round" opacity=".9"/>'
             '<circle id="edema" r="200" fill="#ef4444" opacity="0" filter="url(#blur8)"/>'
             '<circle id="musc" r="190" fill="none" stroke="#9f2a3f" stroke-width="24" stroke-dasharray="26 10"/>'
             '<path id="muco" fill="#f6c3c8"/>'
             '<circle id="blum" r="150" fill="#12050a"/>'
             '</g>')
    s.append('<g id="inj" opacity="0"><g transform="rotate(-28)">'
             '<rect x="-150" y="-34" width="300" height="68" rx="30" fill="url(#injg)" filter="url(#glow)"/>'
             '<rect x="150" y="-18" width="60" height="36" rx="10" fill="#f97316"/>'
             '<text x="0" y="12" text-anchor="middle" font-family="Inter,sans-serif" font-size="30" font-weight="800" fill="#0c4a6e">ADRENALINA</text></g></g>')
    s.append('<g id="waves" fill="none" stroke="#38bdf8" stroke-width="6" filter="url(#glow)">' + ''.join(f'<circle id="wv{i}" r="10" opacity="0"/>' for i in range(4)) + '</g>')
    return ''.join(s)

JS = (r'''
const RBC=__RBC__, GR=__GR__, HIS=__HIS__, REC=__REC__, LEAK=__LEAK__;
let F=0; for(let x=0;x<t;x+=.05){ F+= .05*(1-.55*S(x,9.4,11)+.55*S(x,18.8,20.5)) }
const dd = 70*S(t,9.6,11.5) - 70*S(t,19.5,21.5);
const leak = S(t,10,11.5) - S(t,19.4,21);
A('lum','y',900-dd); A('lum','height',280+2*dd);
TT('wt',`translate(0 ${-dd})`); TT('wb',`translate(0 ${dd})`);
document.querySelectorAll('.seg').forEach(e=>{const x=+e.dataset.x, w=124-34*leak; e.setAttribute('x', x+(124-w)/2); e.setAttribute('width', w)});
RBC.forEach((c,i)=>{ const x=((c[0]+c[2]*F*1.6)%1500)-200; const y=1040+c[1]*(1+dd/140)+Math.sin(t*1.5+c[3])*6;
  TT('r'+i,`translate(${x} ${y}) rotate(${Math.sin(t+c[3])*18})`) });
LEAK.forEach((p,i)=>{ const f=(t*.5+p[2])%1; const y0 = p[1]<0 ? 860-dd : 1220+dd; const y=y0+p[1]*f*170;
  A('lk'+i,'cx',p[0]); A('lk'+i,'cy',y); O('lk'+i, leak*(1-f)*.9) });
const mo = 1 - S(t,13.8,14.6);
O('mastg', mo); A('mastg','transform',`translate(540 470) scale(${1+.05*S(t,5,6)})`);
GR.forEach((g,i)=>{ const p=S(t,5.2+i*.02,7.6+i*.02); const k=1+2.6*p; const e=$('g'+i);
  e.setAttribute('cx',540+g[0]*k); e.setAttribute('cy',470+g[1]*k);
  e.setAttribute('fill', p>.25 ? '#fbbf24' : '#8b5cf6'); e.style.opacity = mo*(1-S(t,8.2,9.4)) });
HIS.forEach((h,i)=>{ const p=out(P(t,5.3+h[3],8.2+h[3])); const r=L(h[1],h[2],p);
  const a=h[0]+t*.05; A('h'+i,'cx',540+r*Math.cos(a)); A('h'+i,'cy',470+r*Math.sin(a)*.8);
  O('h'+i, S(t,5.3+h[3],5.8+h[3])*(1-S(t,19.2,21))*(.55+.45*Math.sin(t*3+i))) });
for(let i=0;i<6;i++){ const a=REC[i+1]*Math.PI/180; const tx=540+212*Math.cos(a), ty=470+212*Math.sin(a);
  const sx=540+(i-2.5)*190, sy=-60-i*25; const p=S(t,.4+i*.25,3.0+i*.25);
  TT('al'+i,`translate(${L(sx,tx,p)} ${L(sy,ty,p)}) rotate(${t*40+i*30})`); O('al'+i, mo*(1-S(t,5.4,6.4))) }
const bo=S(t,13.9,14.8); O('bron',bo);
const con = S(t,14.6,16.8) - S(t,19.6,21.6);
const lum = 150-95*con; A('blum','r',lum); A('musc','r',lum+40);
let dp=''; for(let j=0;j<=72;j++){ const a=j/72*Math.PI*2; const r=lum+16+Math.sin(a*10)*(4+8*con); dp+=(j?'L':'M')+(Math.cos(a)*r).toFixed(1)+' '+(Math.sin(a)*r).toFixed(1) } A('muco','d',dp+'Z');
O('edema', .55*con*(.7+.3*Math.sin(t*5)));
const ip=S(t,18.5,19.4); O('inj', ip); TT('inj',`translate(${L(1300,820,ip)} ${L(560,820,ip)})`);
for(let i=0;i<4;i++){ const q=P(t,19.4+i*.45,20.9+i*.45); A('wv'+i,'cx',820); A('wv'+i,'cy',820); A('wv'+i,'r',20+380*q); O('wv'+i, q>0&&q<1 ? (1-q)*.8 : 0) }
''').replace('__RBC__', str([list(map(lambda v: round(v, 1), c)) for c in RBC])).replace('__GR__', str([[round(a, 1) for a in g] for g in GR])) \
   .replace('__HIS__', str([[round(a, 2) for a in h] for h in HIS])).replace('__REC__', str(REC)).replace('__LEAK__', str([[round(a, 2) for a in p] for p in LEAK]))

def make():
    return Video('anafilaxia', 'Alergología', 'Anafilaxia', 'Del mastocito a la adrenalina en minutos',
                 '#38bdf8', '#f472b6', svg(), JS,
                 '[[0,1.0,540,690],[4.6,1.12,540,560],[9.2,1.0,540,830],[13.8,1.05,540,700],[18.4,1.02,600,760],[23,1.0,600,780]]',
                 [(0.6, 4.5, 'Un <b>alérgeno</b> se une a la IgE del <b>mastocito</b>.'),
                  (4.8, 9.1, 'En segundos libera <b>histamina</b> y otros mediadores.'),
                  (9.4, 13.7, 'Los vasos se <b>dilatan</b> y fugan líquido: la presión <b>cae</b>.'),
                  (14.0, 18.3, 'La vía aérea <b>se cierra</b>. Es una <b>emergencia</b>.'),
                  (18.6, 22.7, 'Primer paso, sin demora: <b>adrenalina IM</b> en el muslo.')],
                 [(10.6, 13.6, 'Vasodilatación y fuga capilar → choque'),
                  (14.6, 18.2, 'Broncoespasmo y edema de la vía aérea'),
                  (19.2, 22.8, 'Adrenalina IM · cara anterolateral del muslo'),
                  (19.8, 22.8, '0.01 mg/kg · máx. 0.5 mg en adulto')],
                 [(4.6, 'whoosh'), (5.3, 'burst'), (9.2, 'whoosh'), (13.8, 'whoosh'), (15.2, 'boom'), (18.4, 'whoosh'), (19.4, 'chime')],
                 DEFS)
