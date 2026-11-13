from cine import Video

DEFS = '''
<radialGradient id="bone" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#f7efe0"/><stop offset=".6" stop-color="#d9cbb2"/><stop offset="1" stop-color="#9c8b70"/></radialGradient>
<radialGradient id="boneh" cx="38%" cy="32%" r="70%"><stop offset="0" stop-color="#fffaf0"/><stop offset=".65" stop-color="#e2d4bb"/><stop offset="1" stop-color="#a8977b"/></radialGradient>
<clipPath id="pclip"><path id="pelvclip"/></clipPath>
<clipPath id="fclip"><path d="M 40 -60 C 100 -30 150 0 178 26 C 218 14 250 46 240 108 C 234 150 224 186 220 236 L 176 900 L 64 900 L 104 262 C 96 206 70 168 -12 96 Z"/><circle r="92"/></clipPath>
<marker id="ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#fbbf24"/></marker>
'''

PT = ["M 640 640 C 560 520 400 420 200 380", "M 610 690 C 520 600 380 520 160 470", "M 585 725 C 480 660 340 620 130 560",
      "M 560 765 C 460 760 340 760 200 720", "M 600 905 C 560 960 500 1040 470 1100", "M 560 885 C 480 920 380 1000 340 1060",
      "M 520 820 C 430 850 330 880 250 860"]
FT = ["M -40 -60 C -10 20 60 120 120 260", "M 0 -80 C 30 0 80 100 140 240", "M 40 -70 C 60 0 100 80 160 200",
      "M -70 -20 C -20 -90 100 -40 200 80", "M -60 20 C 0 -50 110 0 190 130", "M 120 300 C 125 500 115 700 112 880",
      "M 160 300 C 162 500 150 700 145 880", "M -80 40 C -20 0 40 10 90 60"]

def svg():
    s = []
    s.append('<path id="pelv" fill="url(#bone)" stroke="#f5ecdc" stroke-opacity=".55" stroke-width="3" filter="url(#soft)"/>')
    s.append('<ellipse cx="400" cy="975" rx="62" ry="82" fill="#0b0f15" opacity=".85"/>')
    s.append('<g clip-path="url(#pclip)" filter="url(#glow)">' + ''.join(
        f'<path id="pt{i}" data-len="auto" d="{d}" fill="none" stroke="#ffcf5a" stroke-width="4" stroke-linecap="round" opacity=".9"/>' for i, d in enumerate(PT)) + '</g>')
    s.append('<path id="cart" fill="none" stroke="#7dd3fc" stroke-width="16" stroke-opacity=".45" stroke-linecap="round" filter="url(#glow)"/>')
    s.append('<g id="fem">'
             '<path d="M 40 -60 C 100 -30 150 0 178 26 C 218 14 250 46 240 108 C 234 150 224 186 220 236 L 176 900 L 64 900 L 104 262 C 96 206 70 168 -12 96 Z" fill="url(#bone)" stroke="#f5ecdc" stroke-opacity=".55" stroke-width="3"/>'
             '<ellipse cx="92" cy="250" rx="22" ry="34" fill="#cdbd9f"/>'
             '<circle r="92" fill="url(#boneh)" stroke="#fff6e6" stroke-opacity=".6" stroke-width="3"/>'
             '<g clip-path="url(#fclip)" filter="url(#glow)">' + ''.join(
                 f'<path id="ft{i}" data-len="auto" d="{d}" fill="none" stroke="#ffcf5a" stroke-width="4" stroke-linecap="round" opacity=".9"/>' for i, d in enumerate(FT)) + '</g>'
             '</g>')
    s.append('<circle id="warn" r="112" fill="none" stroke="#f87171" stroke-width="8" filter="url(#glow)" opacity="0"/>')
    s.append('<circle id="clunk" cx="610" cy="800" r="92" fill="none" stroke="#fff" stroke-width="10" filter="url(#glow)" opacity="0"/>')
    s.append('<circle id="ok" cx="610" cy="800" r="118" fill="none" stroke="#4ade80" stroke-width="8" filter="url(#glow)" opacity="0"/>')
    s.append('<path class="fx" data-a="10.2" data-b="13.4" d="M 820 1250 C 780 1300 720 1320 650 1320" fill="none" stroke="#fbbf24" stroke-width="10" stroke-linecap="round" marker-end="url(#ah)" filter="url(#glow)" style="opacity:0"/>')
    s.append('<path class="fx" data-a="14.2" data-b="16.6" d="M 600 1320 C 680 1320 760 1290 830 1230" fill="none" stroke="#fbbf24" stroke-width="10" stroke-linecap="round" marker-end="url(#ah)" filter="url(#glow)" style="opacity:0"/>')
    lab = 'font-family="Inter,sans-serif" font-size="30" font-weight="700" fill="#fff"'
    s.append(f'<g class="fx" data-a="1.3" data-b="4.4" style="opacity:0"><line x1="700" y1="740" x2="820" y2="640" stroke="#fff" stroke-width="2"/><circle cx="700" cy="740" r="6" fill="#fff"/><text x="830" y="630" {lab}>Cabeza femoral</text></g>')
    s.append(f'<g class="fx" data-a="1.8" data-b="4.4" style="opacity:0"><line x1="560" y1="680" x2="420" y2="560" stroke="#fff" stroke-width="2"/><circle cx="560" cy="680" r="6" fill="#fff"/><text x="250" y="545" {lab}>Acetábulo</text></g>')
    return ''.join(s)

JS = r'''
const h = 140 - 70*S(t,5,7) + 55*S(t,19,22);
const PA=[708.7,764], PB=[574,898.7], k=h*1.333*0.7071;
const cup = `${PA[0]} ${PA[1]} C ${PA[0]-k} ${PA[1]-k} ${PB[0]-k} ${PB[1]-k} ${PB[0]} ${PB[1]}`;
const d = `M 90 360 C 260 280 560 330 700 600 L ${cup} L 540 1060 C 500 1150 380 1160 330 1080 L 240 880 C 190 790 110 730 90 650 Z`;
A('pelv','d',d); A('pelvclip','d',d); A('cart','d','M '+cup);
const dx = 48*S(t,5.5,7.5) - 48*S(t,9.2,10) + 95*S(t,11.2,12.4) - 95*S(t,15.6,16.2);
const dy = -14*S(t,5.5,7.5) + 14*S(t,9.2,10) - 25*S(t,11.2,12.4) + 25*S(t,15.6,16.2);
const ang = 14*S(t,10,11.2) - 36*S(t,14.2,15.6) - 6*S(t,19,22);
TT('fem',`translate(${610+dx} ${800+dy}) rotate(${ang})`);
for(let i=0;i<7;i++) draw('pt'+i, S(t,.3+i*.18,2.4+i*.18));
for(let i=0;i<8;i++) draw('ft'+i, S(t,.6+i*.15,2.6+i*.15));
const w = (S(t,6.5,7.2)*(1-S(t,9.0,9.6)) + S(t,12.0,12.5)*(1-S(t,15.6,16.1)));
A('warn','cx',610+dx); A('warn','cy',800+dy); O('warn', w*(.6+.4*Math.sin(t*6)));
const c = P(t,16.2,17.0); A('clunk','r',92+130*c); O('clunk', t>16.2 ? (1-c) : 0);
O('ok', S(t,16.4,17.2)*(.7+.3*Math.sin(t*3)));
const g = .8+.2*Math.sin(t*2.2);
document.querySelectorAll('[id^=pt],[id^=ft]').forEach(e=>e.setAttribute('opacity', g));
'''

def make():
    return Video('ddc', 'Ortopedia pediátrica', 'Displasia del desarrollo de cadera', 'Barlow, Ortolani y tratamiento temprano',
                 '#fbbf24', '#f59e0b', svg(), JS,
                 '[[0,1.0,560,730],[4.6,1.13,600,800],[9.2,1.08,620,880],[13.8,1.1,630,880],[18.4,1.0,560,860],[23,1.07,580,850]]',
                 [(0.6, 4.5, 'En el recién nacido, la cadera <b>aún se está formando</b>.'),
                  (4.8, 9.1, 'Si la cabeza femoral no queda centrada, el <b>acetábulo no se desarrolla</b>.'),
                  (9.4, 13.7, '<b>Barlow</b>: aducción y presión posterior. La cadera inestable <b>se luxa</b>.'),
                  (14.0, 18.3, '<b>Ortolani</b>: abducción. La cadera luxada <b>se reduce</b>.'),
                  (18.6, 22.7, 'Detectarla a tiempo cambia todo: <b>ultrasonido</b> y <b>arnés de Pavlik</b>.')],
                 [(10.0, 13.6, 'Barlow · aducción + presión posterior → luxa'),
                  (14.4, 18.2, 'Ortolani · abducción → reduce'),
                  (19.0, 22.8, 'Ultrasonido antes de los 4–6 meses'),
                  (19.6, 22.8, 'Arnés de Pavlik: flexión y abducción')],
                 [(4.6, 'whoosh'), (9.2, 'whoosh'), (12.2, 'boom'), (13.8, 'whoosh'), (16.2, 'boom'), (18.4, 'whoosh'), (19.4, 'chime')],
                 DEFS)
