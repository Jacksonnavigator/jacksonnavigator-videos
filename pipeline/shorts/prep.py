import json,os
base='/home/claude/yt/shorts'
for sh in json.load(open(f'{base}/shorts.json')):
    d=f"{base}/{sh['id']}"; os.makedirs(f'{d}/audio',exist_ok=True)
    sc=[dict(s,id=s['id'],nocap=True) for s in sh['scenes']]
    json.dump(sc,open(f'{d}/scenes.json','w'),indent=1)
print('ok')
