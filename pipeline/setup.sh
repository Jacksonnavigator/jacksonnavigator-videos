#!/bin/bash
# One-time setup in a fresh Linux workspace. Paths match the scripts: work dir /home/claude/yt, node deps /tmp/pw.
set -e
mkdir -p /home/claude/yt /tmp/kk /tmp/pw
cp -r "$(dirname "$0")"/{stage.html,thumb.html,tts.py,run.sh,finalize.sh,site,mock,shorts} /home/claude/yt/
cp "$(dirname "$0")"/{render.mjs,th.mjs} /tmp/pw/
chmod +x /home/claude/yt/*.sh
pip install --break-system-packages -q kokoro-onnx soundfile qrcode
cd /tmp/kk
[ -f voices.bin ] || curl -sSL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
[ -f kokoro.onnx ] || curl -sSL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
cd /tmp/pw && [ -f package.json ] || npm init -y >/dev/null
npm i -s @sparticuz/chromium puppeteer-core
echo SETUP_OK
