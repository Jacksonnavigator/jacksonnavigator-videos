#!/bin/bash
# usage: run.sh <dir> [extra node script...]
cd /home/claude/yt && python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!; sleep 1
cd /tmp/pw && node render.mjs "$1"
shift; for s in "$@"; do node $s; done
kill $SRV
