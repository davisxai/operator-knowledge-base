#!/usr/bin/env python3
# One long video in, one person folder out: people/<name>/raw, transcript, analysis.
# usage: python3 pull.py <name> <youtube-url-or-local-file> [--root people] [--video] [--transcript-only] [--no-captions] [--whisper groq|openai] [--chunk-minutes 10]
#
# Transcript routes, in order:
#   1. the video's own captions through yt-dlp (free, timestamped). Manual captions first, then auto-generated.
#   2. Groq whisper-large-v3-turbo (GROQ_API_KEY), audio split into chunks under the 25 MB upload limit, segment timestamps kept.
#   3. OpenAI gpt-transcribe (OPENAI_API_KEY), same chunks, one timestamp per chunk.
# Keys are read from the environment, then ~/.config/watch/.env, then ./.env.
# The caption parser and the stdlib multipart upload follow the watch skill by Bradley Bonanno (github.com/bradautomates/claude-video, MIT).

import argparse, io, json, mimetypes, os, re, shutil, subprocess, sys, time, urllib.error, urllib.request, uuid
from datetime import date
from pathlib import Path

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_MODEL = "whisper-large-v3-turbo"
OPENAI_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "gpt-transcribe"
# Listed prices on 2026-11-10. Groq: console.groq.com/docs/speech-to-text. OpenAI: developers.openai.com/api/docs/pricing.
GROQ_USD_PER_HOUR = 0.04
OPENAI_USD_PER_MINUTE = 0.0045

TS_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2})[.,](\d{3})")
TAG_RE = re.compile(r"<[^>]+>")


def need(binary):
    if shutil.which(binary) is None:
        sys.exit(f"{binary} is not installed. On macOS: brew install {binary}")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not s:
        sys.exit("name must contain letters or digits")
    return s


def load_key(preferred=None):
    order = [("groq", "GROQ_API_KEY"), ("openai", "OPENAI_API_KEY")]
    if preferred:
        order = [o for o in order if o[0] == preferred]
    files = [Path.home() / ".config" / "watch" / ".env", Path.cwd() / ".env"]
    for backend, var in order:
        value = os.environ.get(var, "").strip()
        if not value:
            for f in files:
                if not f.exists():
                    continue
                for line in f.read_text().splitlines():
                    k, _, v = line.strip().partition("=")
                    if k.strip() == var and v.strip():
                        value = v.strip().strip('"').strip("'")
                        break
                if value:
                    break
        if value:
            return backend, value
    return None, None


def video_meta(url):
    r = run(["yt-dlp", "--no-warnings", "--no-playlist", "--dump-single-json", url])
    if r.returncode != 0:
        sys.exit(f"yt-dlp could not read the video: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.returncode}")
    j = json.loads(r.stdout)
    return {
        "title": j.get("title"),
        "channel": j.get("channel") or j.get("uploader"),
        "duration_seconds": j.get("duration"),
        "upload_date": j.get("upload_date"),
        "url": j.get("webpage_url") or url,
        "id": j.get("id"),
    }


def download_media(url, raw, video):
    if video:
        cmd = ["yt-dlp", "--no-warnings", "--no-playlist", "-f", "bv*[height<=720]+ba/b[height<=720]/b", "--merge-output-format", "mp4", "-o", str(raw / "source.%(ext)s"), url]
    else:
        # the native audio stream, no re-encode: m4a when YouTube has one, otherwise webm (opus). Both upload to Whisper as is.
        cmd = ["yt-dlp", "--no-warnings", "--no-playlist", "-f", "ba[ext=m4a]/ba", "-o", str(raw / "source.%(ext)s"), url]
    r = run(cmd)
    if r.returncode != 0:
        sys.exit(f"download failed: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.returncode}")
    files = sorted(raw.glob("source.*"))
    return files[-1] if files else None


def fetch_captions(url, folder):
    # manual captions first, then auto-generated, so the source is recorded honestly
    for flag, label in (("--write-subs", "captions-manual"), ("--write-auto-subs", "captions-auto")):
        for old in folder.glob("captions.*.vtt"):
            old.unlink()
        run(["yt-dlp", "--no-warnings", "--no-playlist", "--skip-download", flag, "--sub-langs", "en.*,en", "--sub-format", "vtt/best", "--convert-subs", "vtt", "-o", str(folder / "captions.%(ext)s"), url])
        vtts = sorted(folder.glob("captions.*.vtt"))
        if vtts:
            keep = next((v for v in vtts if v.name == "captions.en.vtt"), vtts[0])
            for v in vtts:
                if v != keep:
                    v.unlink()
            return keep, label
    return None, None


def to_seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_vtt(path):
    # YouTube auto-captions roll: each cue repeats the previous cue's last line before adding a new one,
    # with a near-zero-length bridge cue in between. Keep a line only when it is not the last line already kept.
    lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
    segs, i, last = [], 0, None
    while i < len(lines):
        m = TS_RE.match(lines[i])
        if not m:
            i += 1
            continue
        start, end = to_seconds(*m.groups()[:4]), to_seconds(*m.groups()[4:])
        i += 1
        fresh = []
        while i < len(lines) and lines[i].strip():
            t = re.sub(r"\s+", " ", TAG_RE.sub("", lines[i])).strip()
            if t and t != last:
                fresh.append(t)
                last = t
            i += 1
        if fresh:
            segs.append({"start": round(start, 2), "end": round(end, 2), "text": " ".join(fresh)})
        i += 1
    return segs


def chunk_audio(source, folder, minutes):
    need("ffmpeg")
    chunks = folder / "chunks"
    shutil.rmtree(chunks, ignore_errors=True)
    chunks.mkdir(parents=True)
    r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k", "-f", "segment", "-segment_time", str(minutes * 60), "-reset_timestamps", "1", str(chunks / "chunk_%03d.mp3")])
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed: {r.stderr.strip()}")
    files = sorted(chunks.glob("chunk_*.mp3"))
    if not files:
        sys.exit("ffmpeg produced no audio. Does the file have an audio track?")
    return files


def multipart(fields, path):
    boundary = f"----PullBoundary{uuid.uuid4().hex}"
    buf, eol = io.BytesIO(), b"\r\n"
    for k, v in fields.items():
        buf.write(f"--{boundary}".encode() + eol)
        buf.write(f'Content-Disposition: form-data; name="{k}"'.encode() + eol + eol)
        buf.write(str(v).encode() + eol)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    buf.write(f"--{boundary}".encode() + eol)
    buf.write(f'Content-Disposition: form-data; name="file"; filename="{path.name}"'.encode() + eol)
    buf.write(f"Content-Type: {mime}".encode() + eol + eol)
    buf.write(path.read_bytes() + eol)
    buf.write(f"--{boundary}--".encode() + eol)
    return buf.getvalue(), boundary


def transcribe_chunk(backend, key, path):
    if backend == "groq":
        endpoint, fields = GROQ_ENDPOINT, {"model": GROQ_MODEL, "response_format": "verbose_json", "temperature": "0"}
    else:
        endpoint, fields = OPENAI_ENDPOINT, {"model": OPENAI_MODEL, "response_format": "json"}
    body, boundary = multipart(fields, path)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "video-to-skills-pull/1.0 (python-urllib)"}
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(endpoint, data=body, headers=headers, method="POST"), timeout=300) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            if e.code == 429 or e.code >= 500:
                if attempt < 3:
                    wait = 2.0 * (2 ** attempt)
                    print(f"  {backend} returned {e.code}, retrying in {wait:.0f}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
            sys.exit(f"{backend} request failed: HTTP {e.code} {detail}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < 3:
                time.sleep(2.0 * (2 ** attempt))
                continue
            sys.exit(f"{backend} request failed: {e}")


def transcribe_audio(source, folder, backend, key, minutes):
    files = chunk_audio(source, folder, minutes)
    segs = []
    for i, f in enumerate(files):
        offset = i * minutes * 60
        print(f"  transcribing chunk {i + 1}/{len(files)} with {backend}")
        res = transcribe_chunk(backend, key, f)
        if backend == "groq" and res.get("segments"):
            for s in res["segments"]:
                segs.append({"start": round(offset + float(s["start"]), 2), "end": round(offset + float(s["end"]), 2), "text": s["text"].strip()})
        else:
            dur = audio_seconds(f)
            segs.append({"start": float(offset), "end": round(offset + dur, 2), "text": (res.get("text") or "").strip()})
    shutil.rmtree(folder / "chunks", ignore_errors=True)
    return [s for s in segs if s["text"]]


def audio_seconds(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def stamp(seconds):
    s = int(seconds)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"[{h}:{m:02d}:{sec:02d}]" if h else f"[{m:02d}:{sec:02d}]"


def blocks(segs, max_seconds=60, max_chars=700):
    out, cur = [], None
    for s in segs:
        if cur and (s["end"] - cur["start"] <= max_seconds) and (len(cur["text"]) + len(s["text"]) <= max_chars):
            cur["text"] += " " + s["text"]
            cur["end"] = s["end"]
        else:
            if cur:
                out.append(cur)
            cur = dict(s)
    if cur:
        out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser(description="Pull a long video into a person folder.")
    ap.add_argument("name", help="the person, becomes the folder name (e.g. hormozi)")
    ap.add_argument("source", help="YouTube URL or a local video/audio file")
    ap.add_argument("--root", default="people", help="parent folder (default: people)")
    ap.add_argument("--video", action="store_true", help="keep the full video up to 720p instead of audio only")
    ap.add_argument("--transcript-only", action="store_true", help="skip the raw download when captions exist")
    ap.add_argument("--no-captions", action="store_true", help="skip the captions route, go straight to Whisper")
    ap.add_argument("--whisper", choices=["groq", "openai"], help="force a transcription backend")
    ap.add_argument("--chunk-minutes", type=int, default=10, help="audio chunk length for the API routes (default 10)")
    a = ap.parse_args()

    need("yt-dlp")
    slug = slugify(a.name)
    person = Path(a.root) / slug
    raw, transcript, analysis = person / "raw", person / "transcript", person / "analysis"
    for d in (raw, transcript, analysis):
        d.mkdir(parents=True, exist_ok=True)

    is_url = a.source.startswith(("http://", "https://"))
    meta = {"title": None, "channel": None, "duration_seconds": None, "upload_date": None, "url": None, "id": None}
    segs, source_label, media = [], None, None

    if is_url:
        print(f"reading {a.source}")
        meta = video_meta(a.source)
        print(f"  {meta['title']}  ({meta['channel']}, {int((meta['duration_seconds'] or 0) // 60)} min)")
        if not a.no_captions:
            vtt, source_label = fetch_captions(a.source, transcript)
            if vtt:
                segs = parse_vtt(vtt)
                print(f"  captions: {source_label}, {len(segs)} cues")
        if not segs or not a.transcript_only:
            if segs and a.transcript_only:
                pass
            else:
                print("  downloading " + ("video" if a.video else "audio"))
                media = download_media(a.source, raw, a.video)
    else:
        src = Path(a.source).expanduser().resolve()
        if not src.exists():
            sys.exit(f"file not found: {src}")
        (raw / "SOURCE.txt").write_text(str(src) + "\n")
        meta.update({"title": src.stem, "url": str(src), "duration_seconds": round(audio_seconds(src))})
        media = src

    if not segs:
        backend, key = load_key(a.whisper)
        if not key:
            print("no captions and no API key. Set GROQ_API_KEY or OPENAI_API_KEY (environment, ~/.config/watch/.env, or ./.env) and rerun.")
            print(f"folder is ready at {person}")
            sys.exit(2)
        if media is None:
            media = download_media(a.source, raw, False)
        print(f"  no captions, transcribing with {backend}")
        segs = transcribe_audio(media, transcript, backend, key, a.chunk_minutes)
        source_label = f"{backend}-{GROQ_MODEL if backend == 'groq' else OPENAI_MODEL}"
        if not meta["duration_seconds"]:
            meta["duration_seconds"] = round(audio_seconds(media))

    if not segs:
        sys.exit("no transcript came back")

    (transcript / "segments.json").write_text(json.dumps(segs, indent=1))
    bl = blocks(segs)
    words = sum(len(s["text"].split()) for s in segs)
    head = [f"# {meta['title'] or slug}", ""]
    if meta["channel"]:
        head.append(f"- **Channel:** {meta['channel']}")
    if meta["url"]:
        head.append(f"- **Source:** {meta['url']}")
    if meta["duration_seconds"]:
        d = int(meta["duration_seconds"])
        head.append(f"- **Length:** {d // 60} min" if d >= 60 else f"- **Length:** {d} sec")
    head += [f"- **Transcript:** {source_label}, {words} words", f"- **Pulled:** {date.today().isoformat()}", ""]
    body = [f"{stamp(b['start'])} {b['text']}" for b in bl]
    (transcript / "transcript.md").write_text("\n".join(head) + "\n" + "\n\n".join(body) + "\n")
    meta.update({"transcript_source": source_label, "words": words, "blocks": len(bl), "pulled": date.today().isoformat(), "raw": str(media) if media else None})
    (transcript / "meta.json").write_text(json.dumps(meta, indent=1))

    print(f"\n{person}/")
    print(f"  raw/         {media.name if media else '(transcript only)'}")
    print(f"  transcript/  transcript.md ({words} words, {len(bl)} blocks), segments.json, meta.json")
    print(f"  analysis/    empty, the skill fills it")
    hours = (meta["duration_seconds"] or 0) / 3600
    if source_label and source_label.startswith("groq"):
        print(f"  cost: about ${hours * GROQ_USD_PER_HOUR:.2f} at Groq's listed ${GROQ_USD_PER_HOUR}/hour")
    elif source_label and source_label.startswith("openai"):
        print(f"  cost: about ${hours * 60 * OPENAI_USD_PER_MINUTE:.2f} at OpenAI's listed ${OPENAI_USD_PER_MINUTE}/minute")
    else:
        print("  cost: $0, captions")
    print(f"\nnext: open Claude Code in {Path(a.root).resolve().parent} and run  /video-to-skills {slug}")


if __name__ == "__main__":
    main()
