import math, random
from cine import Video

DEFS = '''
<radialGradient id="thrg" cx="50%" cy="60%" r="60%"><stop offset="0" stop-color="#c81e3a"/><stop offset="1" stop-color="#7a0f1f"/></radialGradient>
<linearGradient id="awall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f2a36"/><stop offset="1" stop-color="#e07a86"/></linearGradient>
<linearGradient id="awall2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e07a86"/><stop offset="1" stop-color="#8f2a36"/></linearGradient>
<linearGradient id="alum" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0508"/><stop offset=".5" stop-color="#5c1019"/><stop offset="1" stop-color="#2a0508"/></linearGradient>
<radialGradient id="rbc2" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#ff6b6b"/><stop offset=".7" stop-color="#d11f2c"/><stop offset="1" stop-color="#8a0d16"/></radialGradient>
<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fde68a"/><stop offset="1" stop-color="#d97706"/></linearGradient>
<linearGradient id="myo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b23a46"/><stop offset="1" stop-color="#5e121b"/></linearGradient>
<linearGradient id="ischg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b2d4f" stop-opacity="0"/><stop offset=".25" stop-color="#3b2d4f" stop-opacity="1"/><stop offset="1" stop-color="#2a2238" stop-opacity="1"/></linearGradient>
<pattern id="fib" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><path d="M0 13 H26 M13 0 V26" stroke="#f5d0a9" stroke-width="2" opacity=".7"/></pattern>
<pattern id="ecgg" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0 H0 V40" fill="none" stroke="#ff6b6b" stroke-opacity=".12" stroke-width="2"/></pattern>
'''

rnd = random.Random(11)
RBC = [(rnd.uniform(0, 1500), rnd.uniform(-70, 70), rnd.uniform(0, 6.28)) for _ in range(26)]
PLT = [(rnd.uniform(-200, 300), rnd.uniform(-70, 70), rnd.uniform(500, 600), rnd.uniform(-30, 10)) for _ in range(18)]

def ecg():
    d = 'M 60 420'; st = []
    for i in range(4):
        x = 100 + i * 240
        d += f' L {x} 420 Q {x+20} 395 {x+40} 420 L {x+60} 420 L {x+70} 440 L {x+85} 300 L {x+100} 460 L {x+110} 382 L {x+150} 380 Q {x+175} 335 {x+205} 382 L {x+240} 420'
        st.append(f'M {x+110} 382 L {x+150} 380')
    return d, st

def stent():
    p = []
    for j in range(8):
        x0 = 400 + j * 40
        p.append(f'M {x0} -90 L {x0+20} 0 L {x0} 90 M {x0+40} -90 L {x0+20} 0 L {x0+40} 90')
    p.append('M 400 -90 H 720 M 400 90 H 720')
    return ' '.join(p)

def svg():
    s = ['<rect x="-200" y="1000" width="1500" height="600" fill="url(#myo)"/>']
    for i in range(16):
        y = 1020 + i * 34
        s.append(f'<path d="M -200 {y} C 100 {y-12} 400 {y+12} 700 {y} S 1100 {y-10} 1300 {y}" stroke="#7a1d26" stroke-width="5" fill="none" opacity=".7"/>')
    s.append('<rect id="isch" x="560" y="985" width="740" height="615" fill="url(#ischg)" opacity="0"/>')
    s.append('<rect x="-200" y="760" width="1500" height="180" fill="url(#alum)"/>')
    s.append('<g id="rbcs">' + ''.join(f'<g id="r{i}"><ellipse rx="34" ry="15" fill="url(#rbc2)"/><ellipse rx="16" ry="5.5" fill="#9b111e" opacity=".55"/></g>' for i in range(len(RBC))) + '</g>')
    s.append('<g filter="url(#glow)">' + ''.join(f'<circle id="pl{i}" r="8" fill="#f1f5f9" opacity="0"/>' for i in range(len(PLT))) + '</g>')
    s.append('<path id="plaq" fill="url(#lip)"/><path id="cap" fill="none" stroke="#f8e7d0" stroke-width="10" stroke-linecap="round"/>')
    s.append('<g id="thr" opacity="0"><path id="thrp" fill="url(#thrg)" stroke="#ff8a8a" stroke-opacity=".5" stroke-width="3"/><path id="thrf" fill="url(#fib)"/></g>')
    s.append('<path id="crack" data-len="auto" d="M 515 0 L 530 14 L 522 26 L 545 38 L 538 52 L 560 66" fill="none" stroke="#fff" stroke-width="5" filter="url(#glow)" opacity="0"/>')
    s.append(f'<g id="stent" opacity="0"><path d="{stent()}" fill="none" stroke="#e2e8f0" stroke-width="6" stroke-linejoin="round" filter="url(#glow)"/></g>')
    s.append('<rect x="-200" y="720" width="1500" height="40" fill="url(#awall)"/><rect x="-200" y="940" width="1500" height="40" fill="url(#awall2)"/>')
    s.append('<rect x="-200" y="756" width="1500" height="4" fill="#f9c1c8" opacity=".5"/><rect x="-200" y="940" width="1500" height="4" fill="#f9c1c8" opacity=".5"/>')
    d, st = ecg()
    s.append('<g id="ecgp" opacity="0"><rect x="40" y="270" width="1000" height="240" rx="26" fill="#0b0f15" opacity=".9"/><rect x="40" y="270" width="1000" height="240" rx="26" fill="url(#ecgg)"/>'
             f'<path id="ecgl" data-len="auto" d="{d}" fill="none" stroke="#a7f3d0" stroke-width="5" stroke-linejoin="round" filter="url(#glow)"/>'
             + ''.join(f'<path class="stseg" d="{x}" stroke="#fbbf24" stroke-width="12" stroke-linecap="round" filter="url(#glow)" opacity="0"/>' for x in st) + '</g>')
    return ''.join(s)

JS = (r'''
const RBC=__RBC__, PLT=__PLT__;
let F=0; for(let x=0;x<t;x+=.05){ F+=.05*(1-S(x,8.0,9.6)+S(x,19.6,21.0)) }
const ph = 40 + 70*S(t,.6,4.0) - 85*S(t,19.0,20.4);
const top = 940-ph;
A('plaq','d',`M 380 940 C 450 940 470 ${top} 550 ${top} C 630 ${top} 650 940 720 940 Z`);
A('cap','d',`M 400 938 C 460 936 475 ${top} 550 ${top} C 625 ${top} 640 936 700 938`);
TT('crack',`translate(0 ${top-10})`); draw('crack', S(t,5.0,5.6)); O('crack', S(t,4.9,5.1)*(1-S(t,19,19.8)));
const base = top+12, ttop = L(base-6, 757, S(t,6.0,8.6));
const tp = `M 420 ${base+8} C 440 ${ttop+10} 470 ${ttop} 552 ${ttop} C 635 ${ttop} 665 ${ttop+10} 685 ${base+8} Z`;
A('thrp','d',tp); A('thrf','d',tp); O('thr', S(t,5.8,6.4)*(1-S(t,19.4,21)));
const isch = S(t,9.6,12.0)*(1-.55*S(t,20,22.5));
O('isch', .8*isch*(.85+.15*Math.sin(t*4)));
RBC.forEach((c,i)=>{ const x=((c[0]+190*F)%1500)-200; const y=850+c[1]+Math.sin(t*1.4+c[2])*5;
  TT('r'+i,`translate(${x} ${y}) rotate(${Math.sin(t+c[2])*15})`);
  O('r'+i, x>640 ? 1-.9*S(t,9.0,10.5)*(1-S(t,19.8,21)) : 1) });
PLT.forEach((p,i)=>{ const q=S(t,5.6+i*.05,7.2+i*.05); A('pl'+i,'cx',L(p[0],p[2],q)); A('pl'+i,'cy',L(850+p[1],top+p[3],q)); O('pl'+i, S(t,5.4,5.8)*(1-S(t,8.4,9.2))) });
O('ecgp', S(t,13.9,14.6)*(1-S(t,18.2,18.8))); draw('ecgl', S(t,14.2,16.6));
document.querySelectorAll('.stseg').forEach((e,i)=>e.style.opacity=S(t,16.3+i*.2,16.7+i*.2)*(.7+.3*Math.sin(t*6)));
const sh = .15+.85*S(t,19.0,20.2); O('stent', S(t,18.6,19.0)); TT('stent',`translate(0 850) scale(1 ${sh})`);
''').replace('__RBC__', str([[round(a, 1) for a in c] for c in RBC])).replace('__PLT__', str([[round(a, 1) for a in c] for c in PLT]))

def make():
    beats = [(0.4 + k * 0.85, 'beat') for k in range(11)] + [(20.3 + k * 0.8, 'beat') for k in range(3)]
    return Video('iam', 'Cardiología', 'Infarto agudo de miocardio', 'De la placa al tiempo de reperfusión',
                 '#ff6b6b', '#ef4444', svg(), JS,
                 '[[0,1.1,540,860],[4.6,1.3,560,860],[9.2,1.0,640,960],[13.8,1.0,540,640],[18.4,1.2,560,860],[23,1.06,560,880]]',
                 [(0.6, 4.5, 'En la pared de la coronaria crece una <b>placa de ateroma</b>.'),
                  (4.8, 9.1, 'Si su capa fibrosa <b>se rompe</b>, se forma un <b>trombo</b>.'),
                  (9.4, 13.7, 'El flujo se detiene y el miocardio entra en <b>isquemia</b>.'),
                  (14.0, 18.3, '<b>Tiempo es miocardio</b>: ECG en menos de <b>10 minutos</b>.'),
                  (18.6, 22.7, 'Con elevación del ST: <b>reperfundir</b> cuanto antes.')],
                 [(14.6, 18.2, 'ECG en menos de 10 minutos'),
                  (16.4, 18.2, 'Elevación del ST = IAM CEST'),
                  (19.0, 22.8, 'Angioplastia primaria si se logra en < 120 min'),
                  (19.6, 22.8, 'Si no es posible: trombólisis')],
                 beats + [(4.6, 'whoosh'), (5.0, 'tick'), (8.6, 'boom'), (9.2, 'whoosh'), (13.8, 'whoosh'), (18.4, 'whoosh'), (20.2, 'chime')],
                 DEFS)
