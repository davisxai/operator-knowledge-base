"""Write the voice timing into index.html. Rerun it every time the voice changes.

Usage (from your reel folder):  python3 scripts/apply_timing.py

What it rewrites in index.html:
- const SEG = {...}    start and end of every script entry, in seconds
- const WORDS = {...}  the onset of every word in every spoken line, relative to the line start
- const DUR = n;       the total length
- data-duration on #root and the #vo audio element
- every <section class="clip" data-from="s01" data-to="s03"> window: it opens 0.15s before
  its first line and closes 0.15s after the next spoken line starts, so scenes overlap for the cut.

It prints any scene that stays on screen under 2.5 seconds. Fold those into a neighbour or add a
silence entry after the line in script.json.
"""
import json, re

t = json.load(open("assets/vo/timing.json"))
segs = t["segments"]
order = [s["key"] for s in segs]
seg = {s["key"]: {"start": s["start"], "end": s["end"]} for s in segs}
words = {s["key"]: s["words"] for s in segs if "words" in s}
DUR = round(t["total"], 3)

html = open("index.html").read()
html = re.sub(r"const SEG = \{.*?\};", "const SEG = " + json.dumps(seg) + ";", html, count=1, flags=re.S)
html = re.sub(r"const WORDS = \{.*?\};", "const WORDS = " + json.dumps(words) + ";", html, count=1, flags=re.S)
html = re.sub(r"const DUR = [0-9.]+;", f"const DUR = {DUR};", html, count=1)
html = re.sub(r'(id="root"[^>]*?data-duration=")[0-9.]+(")', rf"\g<1>{DUR}\2", html, count=1)
html = re.sub(r'(id="vo"[^>]*?data-duration=")[0-9.]+(")', rf"\g<1>{DUR}\2", html, count=1)

short = {}
def window(m):
    tag, a_key, b_key = m.group(0), m.group("a"), m.group("b")
    first = order.index(a_key) == 0
    start = 0 if first else seg[a_key]["start"] - 0.15
    spoken = [k for k in order[order.index(b_key) + 1:] if k in words]
    end = seg[spoken[0]]["start"] + 0.15 if spoken else DUR
    if end - start < 2.5: short[a_key] = round(end - start, 2)
    tag = re.sub(r'data-start="[0-9.]*"', f'data-start="{round(start, 3)}"', tag)
    return re.sub(r'data-duration="[0-9.]*"', f'data-duration="{round(end - start, 3)}"', tag)

html = re.sub(r'<section[^>]*class="clip"[^>]*data-from="(?P<a>[^"]+)"[^>]*data-to="(?P<b>[^"]+)"[^>]*>', window, html)
open("index.html", "w").write(html)
print("applied | total", DUR, "seconds")
if short: print("UNDER 2.5s ON SCREEN:", short)
