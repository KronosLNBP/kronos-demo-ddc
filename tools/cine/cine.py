"""Videos verticales estilo "anatomía cinematográfica" de Kronos.
Cada video es un HTML 1080x1920 con una función render(t) determinista,
se graba cuadro por cuadro con Playwright y se le une el cierre KRONOS.
"""
import asyncio, base64, html, math, os, random, subprocess, wave
import numpy as np

W, H, FPS = 1080, 1920, 30
ROOT = '/home/claude/cine'
LOGO = base64.b64encode(open('/home/claude/video/logo.png', 'rb').read()).decode()
E = lambda s: html.escape(str(s))

CSS = r'''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#05070a;font-family:Inter,Poppins,"Segoe UI",sans-serif;color:#fff}
#stage{position:absolute;inset:0}
svg{position:absolute;inset:0}
.vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 75% 60% at 50% 42%,transparent 45%,rgba(0,0,0,.55) 80%,rgba(0,0,0,.85) 100%)}
.shade{position:absolute;left:0;right:0;bottom:0;height:720px;background:linear-gradient(transparent,rgba(3,5,8,.82) 55%,rgba(3,5,8,.95))}
.top{position:absolute;left:70px;top:90px;display:flex;align-items:center;gap:16px;font-weight:800;letter-spacing:5px;font-size:24px;color:rgba(255,255,255,.75);text-transform:uppercase}
.top i{width:34px;height:3px;background:var(--acc)}
.title{position:absolute;left:70px;right:70px;top:150px}
.title h1{font-size:84px;line-height:1.02;font-weight:800;letter-spacing:-1.5px;text-shadow:0 6px 40px rgba(0,0,0,.7)}
.title p{margin-top:18px;font-size:32px;color:rgba(255,255,255,.7);font-weight:600}
.cap{position:absolute;left:80px;right:80px;bottom:300px;font-size:60px;line-height:1.16;font-weight:800;letter-spacing:-.5px;text-shadow:0 4px 30px rgba(0,0,0,.8);opacity:0}
.cap b{color:var(--acc);font-weight:800}
.chips{position:absolute;left:80px;right:80px;bottom:560px;display:flex;flex-direction:column;align-items:flex-start;gap:16px}
.chip{display:inline-flex;align-items:center;gap:14px;padding:16px 26px;border-radius:18px;background:rgba(10,16,26,.78);border:1.5px solid var(--accl);font-size:34px;font-weight:700;backdrop-filter:blur(6px);box-shadow:0 10px 40px rgba(0,0,0,.4);opacity:0}
.chip i{width:14px;height:14px;border-radius:50%;background:var(--acc);box-shadow:0 0 18px var(--acc)}
.badge{position:absolute;right:56px;bottom:70px;width:84px;height:84px;border-radius:20px;background:rgba(37,99,235,.9);display:grid;place-items:center;box-shadow:0 0 30px rgba(59,130,246,.6)}
.badge img{width:62px}
.bar{position:absolute;left:80px;right:80px;bottom:200px;height:5px;border-radius:5px;background:rgba(255,255,255,.12)}
.bar span{display:block;height:100%;border-radius:5px;background:var(--acc)}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
'''

JS_BASE = r'''
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const io=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const out=p=>1-Math.pow(1-p,3);
const P=(t,a,b)=>clamp((t-a)/(b-a));
const S=(t,a,b)=>io(P(t,a,b));
const L=(a,b,p)=>a+(b-a)*p;
const $=id=>document.getElementById(id);
const A=(id,k,v)=>{const e=typeof id==='string'?$(id):id; if(e) e.setAttribute(k,v)};
const O=(id,v)=>{const e=typeof id==='string'?$(id):id; if(e) e.style.opacity=v};
const TT=(id,v)=>{const e=typeof id==='string'?$(id):id; if(e) e.setAttribute('transform',v)};
const TOTAL=+document.body.dataset.total;
function camera(t){
  const k=CAM; let a=k[0],b=k[k.length-1];
  for(let i=0;i<k.length-1;i++){ if(t>=k[i][0]&&t<=k[i+1][0]){a=k[i];b=k[i+1];break} }
  if(t<k[0][0]) b=a; if(t>k[k.length-1][0]) a=b;
  const p=a===b?0:io(P(t,a[0],b[0]));
  const s=L(a[1],b[1],p), x=L(a[2],b[2],p), y=L(a[3],b[3],p);
  TT('cam',`translate(540 820) scale(${s}) translate(${-x} ${-y})`);
}
function draw(id,p){const e=$(id); if(!e) return; const len=+e.dataset.len; e.style.strokeDasharray=len; e.style.strokeDashoffset=len*(1-p)}
window.render=function(t){
  camera(t);
  // partículas de polvo
  document.querySelectorAll('.dust').forEach((d,i)=>{
    const x=+d.dataset.x, y=+d.dataset.y, sp=+d.dataset.s;
    const yy=((y - t*sp*14) % 2000 + 2000) % 2000 - 40;
    d.setAttribute('cx', x + Math.sin(t*.4+i)*18); d.setAttribute('cy', yy);
    d.style.opacity = (.25+.25*Math.sin(t*1.3+i*2.1)) * clamp(t/1.2);
  });
  document.querySelectorAll('.bok').forEach((d,i)=>{ d.setAttribute('transform',`translate(${Math.sin(t*.12+i)*30} ${Math.cos(t*.1+i)*20})`) });
  // título
  const ti=S(t,.2,1.0)*(1-S(t,4.0,4.6));
  O('title',ti); $('title').style.transform=`translateY(${(1-S(t,.2,1.0))*30}px)`;
  O('top',S(t,4.2,4.9));
  // subtítulos
  document.querySelectorAll('.cap').forEach(c=>{
    const a=+c.dataset.a,b=+c.dataset.b;
    const o=S(t,a,a+.45)*(1-S(t,b-.35,b));
    c.style.opacity=o; c.style.transform=`translateY(${(1-out(P(t,a,a+.5)))*40}px)`;
  });
  document.querySelectorAll('.fx').forEach(c=>{
    const a=+c.dataset.a,b=+(c.dataset.b||1e9);
    const o=S(t,a,a+.4)*(1-S(t,b-.3,b));
    c.style.opacity=o;
    if(c.classList.contains('chip')) c.style.transform=`translateX(${(1-out(P(t,a,a+.5)))*-50}px)`;
  });
  $('barfill').style.width=(clamp(t/TOTAL)*100)+'%';
  O('flash',S(t,TOTAL-.6,TOTAL));
  anim(t);
};
'''


def bokeh(acc2):
    """Fondo: luces difusas tipo monitores de laboratorio."""
    rnd = random.Random(7)
    out = ['<g filter="url(#blur40)">']
    for i in range(7):
        x = rnd.choice([rnd.randint(-80, 260), rnd.randint(780, 1100)]); y = rnd.randint(120, 1500)
        w = rnd.randint(160, 320); h = rnd.randint(100, 220)
        col = rnd.choice([acc2, '#5b7cff', '#2dd4bf', '#94a3b8'])
        out.append(f'<rect class="bok" x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{col}" opacity="{rnd.uniform(.05,.12):.2f}"/>')
    out.append('</g>')
    for i in range(46):
        out.append(f'<circle class="dust" data-x="{rnd.randint(0,1080)}" data-y="{rnd.randint(0,1960)}" data-s="{rnd.uniform(.4,1.6):.2f}" r="{rnd.uniform(1.2,3.6):.1f}" fill="#fff" opacity="0"/>')
    return '\n'.join(out)


DEFS = '''
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="18"/><feOffset dy="20"/><feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="bgr" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#1b222c"/><stop offset=".55" stop-color="#0c1016"/><stop offset="1" stop-color="#040508"/></radialGradient>
'''


class Video:
    def __init__(self, vid, curso, titulo, sub, acc, acc2, svg, js, cam, caps, chips, cues, defs=''):
        self.id, self.curso, self.titulo, self.sub = vid, curso, titulo, sub
        self.acc, self.acc2, self.svg, self.js, self.cam = acc, acc2, svg, js, cam
        self.caps, self.chips, self.cues, self.defs = caps, chips, cues, defs
        self.t = 23.0

    def html(self):
        caps = ''.join(f'<div class="cap" data-a="{a}" data-b="{b}">{txt}</div>' for a, b, txt in self.caps)
        chips = ''.join(f'<div class="chip fx" data-a="{a}" data-b="{b}"><i></i>{E(txt)}</div>' for a, b, txt in self.chips)
        return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
:root{{--acc:{self.acc};--accl:{self.acc}88}}</style></head>
<body data-total="{self.t}"><div id="stage">
<svg viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{DEFS}{self.defs}</defs>
<rect width="1080" height="1920" fill="url(#bgr)"/>{bokeh(self.acc2)}
<g id="cam">{self.svg}</g></svg>
<div class="vig"></div><div class="shade"></div>
<div class="top" id="top" style="opacity:0"><i></i>Kronos · {E(self.curso)}</div>
<div class="title" id="title" style="opacity:0"><div class="top" style="position:static;margin-bottom:26px"><i></i>{E(self.curso)}</div><h1>{E(self.titulo)}</h1><p>{E(self.sub)}</p></div>
<div class="chips">{chips}</div>{caps}
<div class="bar"><span id="barfill"></span></div>
<div class="badge"><img src="data:image/png;base64,{LOGO}"></div>
<div id="flash"></div></div>
<script>const CAM={self.cam};{JS_BASE}
function anim(t){{ {self.js} }}
document.querySelectorAll('[data-len]').forEach(e=>{{ if(e.dataset.len==='auto') e.dataset.len=Math.ceil(e.getTotalLength()) }});
render(0);</script></body></html>'''


async def record(v, out_mp4, times=None, still=None):
    from playwright.async_api import async_playwright
    path = f'{ROOT}/{v.id}.html'
    open(path, 'w', encoding='utf-8').write(v.html())
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': W, 'height': H})
        await pg.goto(f'file://{path}'); await pg.wait_for_timeout(400)
        if times is not None:
            for i, t in enumerate(times):
                await pg.evaluate(f'render({t})')
                await pg.screenshot(path=still.format(i=i), type='jpeg', quality=85)
            await b.close(); return
        tmp = out_mp4.replace('.mp4', '.tmp.mp4')
        ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        n = int(round(v.t * FPS))
        for i in range(n):
            await pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
        await b.close()
    ff.stdin.close(); ff.wait()
    if ff.returncode == 0: os.replace(tmp, out_mp4)


def audio(v, out_wav, seed=0):
    sr = 48000; T = v.t; n = int(sr * T); t = np.arange(n) / sr
    rng = np.random.default_rng(seed)
    base = [55.0, 61.74, 49.0, 58.27, 51.91][seed % 5]
    out = np.zeros(n)
    # colchón grave con lento vaivén
    for i, (mul, amp) in enumerate([(1, .5), (1.5, .3), (2, .32), (3, .12), (4.0, .08)]):
        lfo = .6 + .4 * np.sin(2 * np.pi * (.05 + .02 * i) * t + i)
        for d in (-.4, .4):
            out += amp * lfo * np.sin(2 * np.pi * (base * mul + d) * t + i)
    # brillo agudo
    for fr in (base * 8, base * 12):
        out += .03 * (np.sin(2 * np.pi * .23 * t) * .5 + .5) * np.sin(2 * np.pi * fr * t)
    out /= np.max(np.abs(out)); out *= 10 ** (-17 / 20)

    def put(t0, sig):
        s = int(t0 * sr); e = min(n, s + len(sig))
        if 0 <= s < n: out[s:e] += sig[:e - s]
    def env(L, a, d):
        x = np.arange(L) / sr; return np.minimum(x / a, 1) * np.exp(-np.maximum(x - a, 0) * d)
    Lw = int(.9 * sr); tw = np.arange(Lw) / sr
    noise = rng.standard_normal(Lw); k = np.ones(60) / 60
    whoosh = np.convolve(noise, k, 'same') * np.sin(np.pi * tw / .9) ** 2 * .22
    Lb = int(.5 * sr); tb = np.arange(Lb) / sr
    boom = np.sin(2 * np.pi * (60 - 25 * tb) * tb) * np.exp(-tb * 7) * .55
    lub = lambda: (np.sin(2 * np.pi * 48 * tb) * np.exp(-tb * 18) * .55)
    Lc = int(1.4 * sr); tc = np.arange(Lc) / sr
    chime = (np.sin(2 * np.pi * 1318.5 * tc) + .5 * np.sin(2 * np.pi * 1975.5 * tc)) * np.exp(-tc * 3) * .07
    tk = np.arange(int(.06 * sr)) / sr
    tick = np.sin(2 * np.pi * 1700 * tk) * np.exp(-tk * 80) * .09
    burst = np.convolve(rng.standard_normal(Lb), np.ones(8) / 8, 'same') * np.exp(-tb * 6) * .25
    for t0, kind in v.cues:
        if kind == 'whoosh': put(t0 - .45, whoosh)
        elif kind == 'boom': put(t0, boom)
        elif kind == 'beat': put(t0, lub()); put(t0 + .28, lub() * .7)
        elif kind == 'chime': put(t0, chime)
        elif kind == 'tick': put(t0, tick)
        elif kind == 'burst': put(t0, burst)
    # subida hacia el destello
    Ls = int(2.2 * sr); ts = np.arange(Ls) / sr
    swell = np.convolve(rng.standard_normal(Ls), np.ones(20) / 20, 'same') * (ts / 2.2) ** 2 * .3
    put(T - 2.2, swell)
    fade = np.ones(n); fi = int(.8 * sr); fade[:fi] = np.linspace(0, 1, fi)
    out = np.clip(out * fade, -1, 1)
    st = np.stack([out, out], 1)
    w = wave.open(out_wav, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st * 32767 * .95).astype(np.int16).tobytes()); w.close()


def finish(v, vmp4, wav, final):
    """Une el video, su audio y el cierre KRONOS (que empieza en blanco)."""
    outro = '/home/claude/v3d/outro.mp4'
    tmp = final.replace('.mp4', '.tmp.mp4')
    fc = (f'[1:a]loudnorm=I=-17:TP=-2:LRA=11,aresample=48000[a0];'
          f'[2:a]aresample=48000,afade=t=in:d=0.25[a1];'
          f'[a0][a1]acrossfade=d=0.3[a];'
          f'[0:v]fps=30,format=yuv420p,setsar=1[v0];[2:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0[v]')
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', vmp4, '-i', wav, '-i', outro, '-filter_complex', fc,
                        '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', tmp])
    if r.returncode == 0: os.replace(tmp, final)
    return r.returncode
