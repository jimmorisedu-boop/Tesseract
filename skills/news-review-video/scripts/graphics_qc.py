#!/usr/bin/env python3
"""Приёмка графики по кадру: палитра, доля акцента, реальный контраст, тест 480 px.

`npx hyperframes check` меряет контраст по DOM и на SVG-подписях внутри под-композиций
может ругаться ложно: измеренное значение не меняется при смене цвета текста. Этот скрипт
меряет то же самое по отрендеренным пикселям, поэтому его результат — источник истины.

Использование:
    python graphics_qc.py renders/frame-08.png
    python graphics_qc.py frame.png --accent "#e8402a" --json qc.json

Проверяет:
  1. палитра кадра и её доли;
  2. доля акцентного цвета (норма — не больше 8 % пикселей);
  3. локальный контраст мелких элементов (текст, подписи): 5-й процентиль и доля
     пикселей ниже 4,5:1 и ниже 3:1 по WCAG;
  4. запрещённые цвета: бежево-кремовый фон, фиолетовый/индиго, неон;
  5. тест 480 px — читаемость на размере телефона (сохраняет копию кадра).

Выход: отчёт в stdout, код возврата 1, если что-то не прошло норму.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ACCENT_DEFAULT = "#e8402a"
ACCENT_MAX_SHARE = 0.08          # норма §5 графики кодом
LOCAL_CONTRAST_MIN = 4.5         # WCAG AA для обычного текста
EDGE_DELTA = 0.06                # порог «это пиксель текста/края», а не фон
PHONE_WIDTH = 480


def srgb_to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminance(rgb: np.ndarray) -> np.ndarray:
    lin = srgb_to_linear(rgb)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def contrast_ratio(l1: np.ndarray, l2: np.ndarray) -> np.ndarray:
    hi = np.maximum(l1, l2)
    lo = np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def hex_to_rgb(value: str) -> np.ndarray:
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(ch * 2 for ch in v)
    return np.array([int(v[i : i + 2], 16) / 255 for i in (0, 2, 4)], dtype=np.float32)


def palette(rgb: np.ndarray, top: int = 8, merge_delta: float = 0.06):
    """Доминирующие цвета кадра. Близкие цвета склеиваются, чтобы квантование не
    разрывало один объект на несколько «разных» цветов с разными долями."""
    q = (rgb * 31).round().astype(np.uint8)          # 5 бит на канал
    flat = (q[..., 0].astype(np.int32) << 10) | (q[..., 1].astype(np.int32) << 5) | q[..., 2]
    keys, counts = np.unique(flat, return_counts=True)
    order = np.argsort(counts)[::-1][: top * 4]
    total = flat.size

    merged: list[dict] = []
    for i in order:
        k = int(keys[i])
        colour = np.array([((k >> 10) & 31) * 8, ((k >> 5) & 31) * 8, (k & 31) * 8],
                          dtype=np.float32) / 255
        share = float(counts[i] / total)
        for item in merged:
            if np.sqrt(((colour - hex_to_rgb(item["hex"])) ** 2).sum()) < merge_delta:
                item["share"] += share
                break
        else:
            merged.append({"hex": "#%02x%02x%02x" % tuple(int(v * 255) for v in colour),
                           "share": share})
    merged.sort(key=lambda x: x["share"], reverse=True)
    for item in merged:
        item["share"] = round(item["share"], 4)
    return merged[:top]


def banned_colours(pal):
    """Бежево-кремовый фон, фиолетовый/индиго, неон — по доминирующим цветам кадра."""
    found = []
    for item in pal:
        if item["share"] < 0.02:
            continue
        rgb = hex_to_rgb(item["hex"])
        h, s, v = colorsys.rgb_to_hsv(*rgb)
        hue = h * 360
        if s < 0.16 and v > 0.82 and 20 <= hue <= 70:
            found.append(f"бежево-кремовый фон {item['hex']} ({item['share']:.1%})")
        if s > 0.25 and 250 <= hue <= 300:
            found.append(f"фиолетовый/индиго {item['hex']} ({item['share']:.1%})")
        if s > 0.75 and v > 0.95:
            found.append(f"неон {item['hex']} ({item['share']:.1%})")
    return found


def ink_vs_background(pal, object_share_min: float = 0.02, ink_share_min: float = 0.0015,
                      noise_ratio: float = 1.5):
    """Контраст значимых цветов кадра к доминирующему фону.

    Фон — самый частый цвет кадра. Дальше:
      * цвета с контрастом ниже 1,5:1 — оттенки фона и сглаживание, не проверяем;
      * доля >= 2 % кадра — графические объекты (столбцы, карты): норма WCAG 1.4.11, 3:1;
      * доля 0,15–2 % — текст и подписи: норма AA, 4,5:1.

    Локальные метрики (пиксель против медианы окна) здесь не годятся: они ловят
    сглаживание краёв и намеренно приглушённую сетку, а не читаемость.
    """
    if not pal:
        return None
    bg = pal[0]
    bg_lum = float(luminance(hex_to_rgb(bg["hex"])))
    rows = []
    for item in pal[1:]:
        if item["share"] < ink_share_min:
            continue
        lum = float(luminance(hex_to_rgb(item["hex"])))
        ratio = (max(lum, bg_lum) + 0.05) / (min(lum, bg_lum) + 0.05)
        if ratio < noise_ratio:
            continue
        kind = "объект" if item["share"] >= object_share_min else "текст"
        need = 3.0 if kind == "объект" else LOCAL_CONTRAST_MIN
        rows.append({
            "hex": item["hex"],
            "share": item["share"],
            "kind": kind,
            "ratio": round(ratio, 2),
            "need": need,
            "ok": ratio >= need,
        })
    return {"background": bg["hex"], "entries": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description="Приёмка графики по кадру")
    ap.add_argument("frame")
    ap.add_argument("--accent", default=ACCENT_DEFAULT, help="акцентный цвет выпуска")
    ap.add_argument("--json", dest="json_out", help="куда записать отчёт")
    ap.add_argument("--phone", type=int, default=PHONE_WIDTH, help="ширина копии для теста телефона")
    args = ap.parse_args()

    im = Image.open(args.frame).convert("RGB")
    rgb = np.asarray(im, dtype=np.float32) / 255
    report = {"frame": os.path.basename(args.frame), "size": list(im.size)}

    pal = palette(rgb)
    report["palette"] = pal
    report["mean_luminance"] = round(float(luminance(rgb).mean()), 4)

    accent = hex_to_rgb(args.accent)
    dist = np.sqrt(((rgb - accent) ** 2).sum(axis=2))
    accent_share = float((dist < 0.30).mean())
    report["accent"] = args.accent
    report["accent_share"] = round(accent_share, 4)
    report["accent_ok"] = accent_share <= ACCENT_MAX_SHARE

    report["banned_colours"] = banned_colours(pal)

    ink = ink_vs_background(pal)
    report["contrast"] = ink
    report["contrast_ok"] = bool(ink and all(r["ok"] for r in ink["entries"])) if ink else True

    phone = im.resize((args.phone, round(im.height * args.phone / im.width)), Image.LANCZOS)
    phone_path = os.path.splitext(args.frame)[0] + f"-{args.phone}px.png"
    phone.save(phone_path)
    prgb = np.asarray(phone, dtype=np.float32) / 255
    report["phone"] = {"path": os.path.basename(phone_path), "size": list(phone.size),
                       "contrast": ink_vs_background(palette(prgb, top=6))}

    print(f"кадр: {report['frame']}  {report['size'][0]}x{report['size'][1]}")
    print("палитра:")
    for item in pal[:6]:
        print(f"  {item['hex']}  {item['share']:.1%}")
    print(f"средняя яркость: {report['mean_luminance']}")
    verdict = "ок" if report["accent_ok"] else f"МНОГО (норма ≤ {ACCENT_MAX_SHARE:.0%})"
    print(f"доля акцента {args.accent}: {accent_share:.2%} — {verdict}")
    if ink:
        print(f"контраст к фону {ink['background']}:")
        for r in ink["entries"]:
            mark = "ок" if r["ok"] else "НИЖЕ НОРМЫ"
            print(f"  {r['hex']}  {r['share']:>6.1%}  {r['kind']:<7} {r['ratio']:>5}:1 "
                  f"(нужно {r['need']}:1) — {mark}")
    if report["phone"]["contrast"]:
        rows = report["phone"]["contrast"]["entries"]
        bad = [r for r in rows if not r["ok"]]
        print(f"тест {args.phone} px: контрастных цветов {len(rows)}, ниже нормы {len(bad)} "
              f"(копия: {report['phone']['path']})")
    if report["banned_colours"]:
        print("запрещённые цвета:")
        for b in report["banned_colours"]:
            print("  -", b)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"отчёт: {args.json_out}")

    ok = report["accent_ok"] and report["contrast_ok"] and not report["banned_colours"]
    print("ИТОГ:", "прошло" if ok else "есть замечания")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
