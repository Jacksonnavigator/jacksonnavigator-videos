import json,sys,soundfile as sf,numpy as np
from kokoro_onnx import Kokoro
d=sys.argv[1]; voice=sys.argv[2] if len(sys.argv)>2 else 'am_michael'
k=Kokoro('/tmp/kk/kokoro.onnx','/tmp/kk/voices.bin')
sc=json.load(open(f'{d}/scenes.json'))
import os
for s in sc:
    p=f"{d}/audio/{s['id']}.wav"
    if os.path.exists(p):
        a,sr=sf.read(p); s['dur']=round(len(a)/sr,3); continue
    a,sr=k.create(s['say'],voice=voice,speed=1.05,lang='en-us')
    pad=np.zeros(int(sr*0.35),dtype=a.dtype)
    a=np.concatenate([pad[:int(sr*0.15)],a,pad])
    sf.write(f"{d}/audio/{s['id']}.wav",a,sr); s['dur']=round(len(a)/sr,3)
json.dump(sc,open(f'{d}/timed.json','w'),indent=1)
print(sum(s['dur'] for s in sc))
