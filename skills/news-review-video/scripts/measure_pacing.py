#!/usr/bin/env python3
"""Замер темпа монтажа готового видео по стандарту новостного разбора.

Считает по факту: резы в минуту, длину плана, долю секунд с резкой сменой картинки,
замороженные и «спокойные» участки. Сравнивает с порогами стандарта и печатает вердикт.

Пороги выведены из измерений референса (см. references/style-standard.md):
тело 5–12 резов/мин, интро ≥18, замороженных кадров ≥2 с нет вообще,
«спокойные» участки (почти без движения) не длиннее 8 с, самый длинный план без реза 25,4 с.

Примеры:
    python measure_pacing.py render/episode-1080p.mp4
    python measure_pacing.py render/episode-1080p.mp4 --intro 66 --json report.json

Требуется ffmpeg/ffprobe в PATH (или --ffmpeg) и Pillow.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics as st
import subprocess
import sys
import tempfile

THRESHOLDS = {
    "intro_cuts_per_min_min": 18.0,    # интро-тизер: не медленнее 18 резов/мин
    "body_cuts_per_min_min": 5.0,      # тело: нижняя граница
    "body_cuts_per_min_max": 12.0,     # тело: верхняя граница (выше — быстрее референса)
    "frozen_mad": 0.5,                 # «кадр заморожен» (0-255)
    "frozen_run_seconds": 2.0,         # замороженный участок такой длины = брак
    "calm_mad": 4.0,                   # «почти нет движения»
    "calm_run_seconds": 10.0,          # спокойный участок такой длины = брак
    "hard_change_mad": 16.0,           # «картинка резко сменилась»
    "warn_seconds_without_cut": 30.0,  # предупреждение: слишком длинный план без реза
    "scene_score": 0.2,                # порог детектора сцен
}


def find_binary(name: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    found = shutil.which(name)
    if found:
        return found
    for cand in (
        rf"C:\ffmpeg\bin\{name}.exe",
        rf"C:\WINDOWS\{name}.exe",
        rf"C:\Program Files\ffmpeg\bin\{name}.exe",
        f"/usr/bin/{name}",
        f"/usr/local/bin/{name}",
    ):
        if os.path.exists(cand):
            return cand
    sys.exit(f"error: {name} not found; pass --ffmpeg <path>")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def probe_duration(ffprobe: str, path: str) -> float:
    res = run([ffprobe, "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", path])
    try:
        return float(res.stdout.decode().strip())
    except ValueError:
        sys.exit(f"error: cannot read duration of {path}: {res.stderr.decode()[:300]}")


def extract_frames(ffmpeg: str, path: str, fps: float, outdir: str) -> list[str]:
    pattern = os.path.join(outdir, "f_%06d.png")
    run([ffmpeg, "-hide_banner", "-nostats", "-y", "-i", path,
         "-vf", f"fps={fps},scale=160:90,format=gray", "-f", "image2", pattern])
    return sorted(f for f in os.listdir(outdir) if f.endswith(".png"))


def motion_series(framedir: str, files: list[str]) -> list[float]:
    from PIL import Image, ImageChops
    mad, prev = [], None
    for name in files:
        im = Image.open(os.path.join(framedir, name)).convert("L")
        if prev is not None:
            diff = ImageChops.difference(prev, im)
            data = list(diff.getdata())
            mad.append(sum(data) / len(data))
        prev = im
    return mad


def scene_cuts(ffmpeg: str, path: str, threshold: float) -> list[float]:
    res = run([ffmpeg, "-hide_banner", "-nostats", "-i", path, "-an",
               "-vf", f"select=gt(scene\\,{threshold}),metadata=mode=print",
               "-f", "null", "-"])
    log = res.stderr.decode("utf-8", "replace")
    cuts, pending = [], None
    for line in log.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            pending = float(m.group(1))
            continue
        m = re.search(r"lavfi\.scene_score=([0-9.]+)", line)
        if m and pending is not None:
            cuts.append(pending)
            pending = None
    return cuts


def runs_below(mad: list[float], fps: float, threshold: float, limit: float) -> list[dict]:
    runs, start = [], None
    for i, x in enumerate(mad):
        if x < threshold:
            start = i if start is None else start
        else:
            if start is not None and (i - start) / fps >= limit:
                runs.append({"start": round(start / fps, 1), "seconds": round((i - start) / fps, 1)})
            start = None
    if start is not None and (len(mad) - start) / fps >= limit:
        runs.append({"start": round(start / fps, 1), "seconds": round((len(mad) - start) / fps, 1)})
    return runs


def main() -> int:
    ap = argparse.ArgumentParser(description="Замер темпа монтажа по стандарту новостного разбора")
    ap.add_argument("video")
    ap.add_argument("--intro", type=float, default=60.0, help="длина интро-тизера в секундах (по умолчанию 60)")
    ap.add_argument("--sample-fps", type=float, default=1.0, help="частота выборки кадров для анализа движения")
    ap.add_argument("--json", dest="json_out", help="сохранить отчёт в JSON")
    ap.add_argument("--ffmpeg", help="путь к ffmpeg")
    ap.add_argument("--ffprobe", help="путь к ffprobe")
    args = ap.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f"error: file not found: {args.video}")

    ffmpeg = find_binary("ffmpeg", args.ffmpeg)
    ffprobe = find_binary("ffprobe", args.ffprobe)
    duration = probe_duration(ffprobe, args.video)
    fps = args.sample_fps

    with tempfile.TemporaryDirectory() as tmp:
        files = extract_frames(ffmpeg, args.video, fps, tmp)
        if not files:
            sys.exit("error: ffmpeg produced no frames — is this a video file?")
        mad = motion_series(tmp, files)

    cuts = scene_cuts(ffmpeg, args.video, THRESHOLDS["scene_score"])
    per_minute = []
    for m in range(int(duration // 60) + 1):
        lo, hi = m * 60.0, (m + 1) * 60.0
        per_minute.append(sum(1 for c in cuts if lo <= c < hi))

    def window(lo: float, hi: float) -> dict:
        lo_i, hi_i = int(lo * fps), min(len(mad), int(hi * fps))
        xs = mad[lo_i:hi_i] or [0.0]
        cut_n = sum(1 for c in cuts if lo <= c < hi)
        span = max((hi - lo) / 60.0, 1e-9)
        return {
            "seconds": round(hi - lo, 1),
            "cuts": cut_n,
            "cuts_per_min": round(cut_n / span, 1),
            "median_motion": round(st.median(xs), 2),
            "hard_change_share": round(100.0 * sum(1 for x in xs if x >= THRESHOLDS["hard_change_mad"]) / len(xs), 1),
            "calm_share": round(100.0 * sum(1 for x in xs if x < THRESHOLDS["calm_mad"]) / len(xs), 1),
        }

    intro = window(0.0, min(args.intro, duration))
    body = window(min(args.intro, duration), duration)
    gaps = [b - a for a, b in zip(cuts, cuts[1:])]
    max_gap = max(gaps) if gaps else duration
    frozen = runs_below(mad, fps, THRESHOLDS["frozen_mad"], THRESHOLDS["frozen_run_seconds"])
    calm = runs_below(mad, fps, THRESHOLDS["calm_mad"], THRESHOLDS["calm_run_seconds"])

    checks = [
        {"name": "интро не медленнее 18 резов/мин", "ok": intro["cuts_per_min"] >= THRESHOLDS["intro_cuts_per_min_min"],
         "value": intro["cuts_per_min"]},
        {"name": "тело 5–12 резов/мин", "ok": THRESHOLDS["body_cuts_per_min_min"] <= body["cuts_per_min"] <= THRESHOLDS["body_cuts_per_min_max"],
         "value": body["cuts_per_min"]},
        {"name": "нет замороженных кадров ≥ 2 с", "ok": not frozen, "value": len(frozen)},
        {"name": "нет «спокойных» участков ≥ 10 с", "ok": not calm, "value": len(calm)},
    ]
    warnings = []
    if max_gap > THRESHOLDS["warn_seconds_without_cut"]:
        warnings.append(f"план без реза длиннее {THRESHOLDS['warn_seconds_without_cut']:.0f} с: {max_gap:.1f} с")
    if body["hard_change_share"] < 25.0:
        warnings.append(f"мало резкой смены картинки в теле: {body['hard_change_share']}% секунд (в референсе 35–45%)")

    print(f"=== Замер темпа: {os.path.basename(args.video)} ===")
    print(f"длительность {duration:.1f} с | резов всего {len(cuts)} | резов/мин {len(cuts) / (duration / 60.0):.1f}")
    print(f"интро 0–{intro['seconds']:.0f} с : {intro['cuts_per_min']} резов/мин, "
          f"медиана движения {intro['median_motion']}, резкая смена {intro['hard_change_share']}% секунд")
    print(f"тело {body['seconds']:.0f} с     : {body['cuts_per_min']} резов/мин, "
          f"медиана движения {body['median_motion']}, резкая смена {body['hard_change_share']}% секунд, "
          f"спокойных секунд {body['calm_share']}%")
    print(f"максимум без реза: {max_gap:.1f} с | замороженных участков: {len(frozen)} | спокойных ≥10 с: {len(calm)}")
    if frozen:
        print("  заморожено:", ", ".join(f"{r['start']}s×{r['seconds']}s" for r in frozen[:10]))
    if calm:
        print("  спокойные:", ", ".join(f"{r['start']}s×{r['seconds']}s" for r in calm[:10]))
    print("резы по минутам:", per_minute)
    print("--- вердикт ---")
    failed = 0
    for c in checks:
        mark = "PASS" if c["ok"] else "FAIL"
        if not c["ok"]:
            failed += 1
        print(f"  [{mark}] {c['name']} (факт: {c['value']})")
    for w in warnings:
        print(f"  [WARN] {w}")
    print("ИТОГ:", "соответствует стандарту" if failed == 0 else f"не соответствует стандарту ({failed} из {len(checks)})")

    if args.json_out:
        report = {
            "file": args.video, "duration": duration, "cuts_total": len(cuts),
            "cuts_per_min": round(len(cuts) / (duration / 60.0), 1),
            "cuts_per_minute_series": per_minute,
            "intro": intro, "body": body,
            "max_seconds_without_cut": round(max_gap, 1),
            "frozen_runs": frozen, "calm_runs": calm,
            "checks": checks, "warnings": warnings, "passed": failed == 0,
            "thresholds": THRESHOLDS,
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print("отчёт сохранён:", args.json_out)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
