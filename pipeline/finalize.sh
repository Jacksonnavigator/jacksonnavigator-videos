#!/bin/bash
# finalize.sh <dir> <outname>
cd $1 && python3 -c "
import json;sc=json.load(open('timed.json'))
open('list.txt','w').write(''.join(f\"file 'seg/{s['id']}.mp4'\n\" for s in sc))" && ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 160k -ar 48000 $2 && echo "final $2 $(ffprobe -v error -show_entries format=duration -of csv=p=0 $2)"
