"""Read script.json, voice it in ElevenLabs, write vo.mp3 and timing.json.

Usage (from your reel folder):
    python3 scripts/build_vo.py            # voice every take
    python3 scripts/build_vo.py --only=0   # re-voice take 0, keep the rest
    python3 scripts/build_vo.py --resplice # rebuild vo.mp3 from saved takes, no API call

Needs: ELEVENLABS_API_KEY in your environment (or a .env file in the reel folder), ffmpeg.

script.json:
{
  "voice_id": "your cloned voice id",
  "model": "eleven_v4",
  "speed": 1.0,
  "segs": [
    ["s01", "Video editing just became a coding problem."],
    ["s02", "Here's the setup. Six steps."],
    ["h02", 0.9],
    ["s03", "One. Open Claude Code in an empty folder."]
  ]
}

A [key, "text"] entry is spoken. A [key, seconds] entry is silence: use it to hold a short beat
on screen. Every silence splits the recording into separate takes, so no cut ever lands inside
a word. timing.json gets the start and end of every entry plus the onset of every word.
"""
import base64, json, os, subprocess, sys, urllib.request

ROOT = os.getcwd()
VO = os.path.join(ROOT, "assets", "vo")
os.makedirs(VO, exist_ok=True)

env = os.path.join(ROOT, ".env")
if os.path.exists(env):
    for line in open(env):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ.setdefault(k, v.strip('"'))

cfg = json.load(open(os.path.join(ROOT, "script.json")))
SEGS = [tuple(e) for e in cfg["segs"]]
VOICE, MODEL, SPEED = cfg["voice_id"], cfg.get("model", "eleven_v4"), float(cfg.get("speed", 1.0))
RESPLICE = "--resplice" in sys.argv
ONLY = next((set(int(x) for x in a.split("=")[1].split(",")) for a in sys.argv[1:] if a.startswith("--only=")), None)
LEAD, TAIL, HEAD, FOOT = 0.1, 0.05, 0.03, 0.08

# group spoken lines into takes, split at every silence entry
takes, cur = [], []
for e in SEGS:
    if isinstance(e[1], str): cur.append(e)
    elif cur: takes.append(cur); cur = []
if cur: takes.append(cur)

def tts(text):
    body = {"text": text, "model_id": MODEL, "output_format": "mp3_44100_128",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.2, "speed": SPEED, "use_speaker_boost": True}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        data=json.dumps(body).encode(), headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)

info = []
for i, take in enumerate(takes):
    raw, alf = os.path.join(VO, f"take_{i}.mp3"), os.path.join(VO, f"take_{i}.json")
    if RESPLICE or (ONLY is not None and i not in ONLY):
        res = json.load(open(alf))
    else:
        res = tts("\n\n".join(t for _, t in take))
        json.dump(res, open(alf, "w")); open(raw, "wb").write(base64.b64decode(res["audio_base64"]))
    al = res["alignment"]; st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    joined = "".join(al["characters"])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw]).decode())
    spans, cursor = {}, 0
    for key, text in take:
        hit = joined.find(text, cursor)
        if hit < 0: raise SystemExit(f"line not found in take {i}: {key}. Re-voice without --resplice.")
        j = hit + len(text) - 1
        words, k = [], 0
        for w in text.split(" "):
            while joined[hit + k] == " ": k += 1
            words.append(st[hit + k]); k += len(w)
        spans[key] = {"start": st[hit], "end": en[j], "words": words}; cursor = j + 1
    first = min(s["start"] for s in spans.values()); last = max(s["end"] for s in spans.values())
    info.append({"raw": raw, "a": max(0.0, first - HEAD), "b": min(dur, last + FOOT), "spans": spans})

pieces, out, timing, ti = [("sil", LEAD)], LEAD, [], 0
for e in SEGS:
    key = e[0]
    if isinstance(e[1], str):
        if ti < len(info) and key == takes[ti][0][0]:
            t = info[ti]; off = out - t["a"]
            pieces.append(("take", ti)); out += t["b"] - t["a"]
            for k2, text in takes[ti]:
                sp = t["spans"][k2]
                timing.append({"key": k2, "text": text, "start": round(sp["start"] + off, 3), "end": round(min(sp["end"], t["b"]) + off, 3),
                               "words": [round(w - sp["start"], 3) for w in sp["words"]]})
            ti += 1
    else:
        d = float(e[1]); timing.append({"key": key, "text": "[silence]", "start": round(out, 3), "end": round(out + d, 3)})
        pieces.append(("sil", d)); out += d
pieces.append(("sil", TAIL)); total = round(out + TAIL, 3)

fc, inputs = [], []
for n, (kind, x) in enumerate(pieces):
    if kind == "take":
        t = info[x]; idx = len(inputs) // 2; inputs += ["-i", t["raw"]]; d = t["b"] - t["a"]
        fc.append(f"[{idx}:a]atrim={t['a']}:{t['b']},asetpts=PTS-STARTPTS,aresample=44100,afade=t=in:st=0:d=0.02,afade=t=out:st={max(0.0, d - 0.03):.3f}:d=0.03[p{n}]")
    else:
        fc.append(f"aevalsrc=0:d={x}:s=44100[p{n}]")
fc.append("".join(f"[p{n}]" for n in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "44100",
                "-c:a", "libmp3lame", "-q:a", "2", os.path.join(VO, "vo.mp3")], check=True)
json.dump({"total": total, "segments": timing}, open(os.path.join(VO, "timing.json"), "w"), indent=1)
for s in timing:
    print(f'{s["key"]:6} {s["start"]:6.2f} -> {s["end"]:6.2f}  {s["text"]}')
print("TOTAL", total, "seconds |", len(takes), "takes")
