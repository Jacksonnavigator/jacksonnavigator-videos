import json,re,subprocess,sys
base='/home/claude/yt/shorts'
FIX=[(r'A\.I\.','AI'),(r'slash star','/*'),(r'slash index dot html','/index.html'),(r'dot env','.env'),(r'git ignore','.gitignore'),(r'Q R','QR'),(r'step by step','step-by-step')]
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return f"{h}:{m:02d}:{s:05.2f}"
def esc(t): return t.replace('\\','').replace('{','(').replace('}',')')
for sh in json.load(open(f'{base}/shorts.json')):
    if len(sys.argv)>1 and sh['id'] not in sys.argv[1:]: continue
    d=f"{base}/{sh['id']}"; sc=json.load(open(f'{d}/timed.json'))
    open(f'{d}/list.txt','w').write(''.join(f"file 'seg/{s['id']}.mp4'\n" for s in sc))
    subprocess.run(f"ffmpeg -y -loglevel error -f concat -safe 0 -i {d}/list.txt -c copy {d}/land.mp4",shell=True,check=True)
    total=sum(s['dur'] for s in sc)
    ev=[]; t0=0
    for s in sc:
        cap=s['say']
        for a,b in FIX: cap=re.sub(a,b,cap)
        prot=re.sub(r'(\S)\.(\S)',r'\1#\2',cap)
        ss=[x.strip().replace('#','.') for x in re.findall(r'[^.?!]+[.?!]+|[^.?!]+$',prot) if x.strip()]
        tot=sum(len(x) for x in ss); acc=0
        for x in ss:
            a=t0+0.15+(s['dur']-0.5)*acc/tot; acc+=len(x); b=t0+0.15+(s['dur']-0.5)*acc/tot
            ev.append(f"Dialogue: 0,{ts(a)},{ts(b+0.2)},Cap,,0,0,0,,{esc(x)}")
        t0+=s['dur']
    title=sh['title'].upper()
    ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Inter,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,70,70,230,1
Style: Sub,Inter,52,&H003DA3E8,&H003DA3E8,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,70,70,500,1
Style: Cap,Inter,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,3,18,0,2,80,80,520,1
Style: Foot,Inter,40,&H99FFFFFF,&H99FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,70,70,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{ts(0)},{ts(total)},Title,,0,0,0,,{esc(title)}
Dialogue: 0,{ts(0)},{ts(total)},Sub,,0,0,0,,{esc(sh['sub'])}
Dialogue: 0,{ts(0)},{ts(total)},Foot,,0,0,0,,@jacksonnavigator · full video on the channel
""" + "\n".join(ev) + "\n"
    open(f'{d}/caps.ass','w').write(ass)
    out=f"{base}/short-{sh['id']}.mp4"
    cmd=(f"ffmpeg -y -loglevel error -i {d}/land.mp4 -filter_complex "
         f"\"color=c=0x13201a:s=1080x1920:r=30[bg];[0:v]scale=1080:-2[v];[bg][v]overlay=0:640:shortest=1,ass={d}/caps.ass[o]\" "
         f"-map \"[o]\" -map 0:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -af loudnorm=I=-14:TP=-1.5 -c:a aac -b:a 160k -ar 48000 {out}")
    subprocess.run(cmd,shell=True,check=True); print('short',sh['id'],round(total,1))
