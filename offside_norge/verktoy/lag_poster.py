"""Render @offside_norge-poster fra JSON.
Bruk: python3 lag_poster.py poster.json UTMAPPE
poster.json: [{"id": "n2026-11-20-1", "palett": "kveld", "tekst": "Linje 1\n\nPunchline"}]
Paletter: se PAL i generer.py (kveld, gress, kritt, norge, manutd, palace, viking, glimt, start, brann, rbk).
Nye lagfarger kan gis som "palett": ["#bakgrunn", "#tekst", "#aksent"].
"""
import json, os, sys
import generer as g
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
g.OUT = out
for p in json.load(open(src)):
    pal = p["palett"]
    if isinstance(pal, list):
        g.PAL["_egen"] = tuple(pal); pal = "_egen"
    png = g.render(p["id"], pal, "", p["tekst"])
    jpg = png[:-4] + ".jpg"
    Image.open(png).convert("RGB").save(jpg, quality=92)
    os.remove(png)
    print(jpg)
