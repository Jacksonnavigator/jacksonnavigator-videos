# Video pipeline (free, no recording)

- `setup.sh` — installs the free AI voice (Kokoro), a headless browser and Python/Node deps.
- A video = a folder with `scenes.json` (see `videos/v1`). Scene types: phone, desktop, split, terminal, title, list, flow, brief, end. Each scene has `say` (narration).
- `python3 tts.py <dir>` → narration clips + `timed.json`
- `run.sh <dir>` → renders each scene (headless browser frames + narration) into `seg/`
- `finalize.sh <dir> <out.mp4>` → joins scenes, normalises audio for YouTube
- Shorts: `shorts/shorts.json` → `shorts/prep.py`, then tts + run.sh per short, then `shorts/compose.py` (1080x1920 with title and captions)
- Mock pages for screens live in `mock/`, the demo safari site in `site/`.
