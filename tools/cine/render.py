import asyncio, sys, time, importlib
sys.path.insert(0, '/home/claude/cine')
from cine import record, audio, finish
for i, name in enumerate(sys.argv[1:]):
    m = importlib.import_module(name); v = m.make(); t0 = time.time()
    vm = f'/home/claude/cine/out/{v.id}_v.mp4'; wa = f'/home/claude/cine/out/{v.id}.wav'
    asyncio.run(record(v, vm)); audio(v, wa, seed=hash(v.id) % 5)
    rc = finish(v, vm, wa, f'/home/claude/cine/out/3d-{v.id}.mp4')
    print(v.id, 'rc', rc, f'{time.time()-t0:.0f}s', flush=True)
