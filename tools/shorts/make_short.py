#!/usr/bin/env python3
"""ショート動画ジェネレーター（basuta / ikimono フォーマット）

使い方:
    python3 tools/shorts/make_short.py shorts/shako

フォルダ構成:
    shorts/<name>/script.json   台本（テロップ・字幕・シーン）
    shorts/<name>/voice/01.wav  VOICEVOX で書き出した音声（任意。字幕1行ごとに1ファイル）
    shorts/<name>/out/          出力先（short.mp4, voicevox_import.txt, description.txt）

voice/ に wav がなければ、読み上げ時間を推定した「音声なし」版を出力する。
wav を入れて再実行すると、音声の長さに合わせて字幕を切り替えた完成版になる。
"""
import json
import math
import random
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
TOP_H = 630
MID_Y0, MID_Y1 = 633, 1285
SUB_Y0 = 1300
LOGO_Y = 1790

YELLOW = (255, 255, 0)
RED = (230, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SUB_OUTLINE = (72, 176, 104)  # #48B068
COLORS = {"yellow": YELLOW, "red": RED, "white": WHITE}

FONT_HEAD = "/usr/share/fonts/opentype/mplus/Mplus1-Black.otf"
FONT_SUB = "/usr/share/fonts/opentype/mplus/Mplus2-Bold.otf"
FONT_LABEL = "/usr/share/fonts/opentype/mplus/Mplus1-Black.otf"

SEC_PER_CHAR = 0.14   # 音声がないときの推定（ずんだもん話速1.1前後）
LINE_PAD = 0.15       # 行と行の間の無音
TAIL = 0.6            # 最後の余韻

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def text_w(draw, s, f, stroke=0):
    l, t, r, b = draw.textbbox((0, 0), s, font=f, stroke_width=stroke)
    return r - l


# ---------- 文字組み ----------
NO_HEAD = set("、。，．・」』）！？ーぁぃぅぇぉっゃゅょァィゥェォッャュョ")


def wrap(draw, s, f, max_w, stroke):
    lines, cur = [], ""
    for ch in s:
        if cur and text_w(draw, cur + ch, f, stroke) > max_w and ch not in NO_HEAD:
            # 直近の句読点で切れるならそこで切る
            cut = max(cur.rfind("、"), cur.rfind("。"))
            if cut >= len(cur) - 7 and cut != len(cur) - 1 and cut > 0:
                lines.append(cur[:cut + 1])
                cur = cur[cut + 1:]
            else:
                lines.append(cur)
                cur = ""
        cur += ch
    if cur:
        lines.append(cur)
    return lines


def balanced_wrap(draw, s, f, max_w, stroke):
    """行数は最小のまま、各行の長さをそろえる（「だ。」だけ残るのを防ぐ）"""
    if "\n" in s:  # 台本で改行位置を指定した場合はそれに従う
        return s.split("\n")
    lines = wrap(draw, s, f, max_w, stroke)
    n = len(lines)
    if n == 1:
        return lines
    full = text_w(draw, s, f, stroke)
    target = full / n
    while target < max_w:
        cand = wrap(draw, s, f, target * 1.06, stroke)
        if len(cand) == n:
            return cand
        target += 20
    return lines


# ---------- 静的レイヤー ----------
def build_base(script):
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    centers = [135, 315, 505]
    for i, h in enumerate(script["headline"][:3]):
        size = h.get("size", 180)
        f = font(FONT_HEAD, size)
        while text_w(d, h["text"], f) > 1010 and size > 60:
            size -= 5
            f = font(FONT_HEAD, size)
        d.text((W // 2, centers[i]), h["text"], font=f, fill=COLORS[h["color"]], anchor="mm")
    f = font(FONT_HEAD, 64)
    if script.get("channel"):
        d.text((W // 2, LOGO_Y), script["channel"], font=f, fill=YELLOW, anchor="mm",
               stroke_width=6, stroke_fill=(200, 60, 0))
    return img


def build_mid_bg():
    h = MID_Y1 - MID_Y0
    bg = Image.new("RGB", (W, h))
    d = ImageDraw.Draw(bg)
    for y in range(h):
        k = y / h
        d.line([(0, y), (W, y)], fill=(int(10 + 20 * k), int(60 + 40 * k), int(110 + 50 * k)))
    # 水面の光
    for x in range(0, W, 140):
        d.polygon([(x, 0), (x + 60, 0), (x + 160, h), (x + 120, h)], fill=(30, 95, 150))
    return bg


rng = random.Random(7)
BUBBLES = [(rng.uniform(0, W), rng.uniform(0, 650), rng.uniform(6, 20), rng.uniform(30, 90)) for _ in range(26)]


def draw_bubbles(d, t):
    h = MID_Y1 - MID_Y0
    for x, y, r, v in BUBBLES:
        yy = (y - v * t) % (h + 40) - 20
        xx = x + 10 * math.sin(t * 2 + y)
        d.ellipse([xx - r, yy - r, xx + r, yy + r], outline=(170, 220, 255), width=3)


def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def outlined(d, xy, s, f, fill, stroke=8, sfill=BLACK, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


# ---------- 中段のシーン（自作の図解アニメ） ----------
def scene_hook(d, t, dur, sc, script):
    cx, cy = W // 2, 360
    p = ease(t / 0.35)
    shake = 12 * math.sin(t * 60) * max(0, 1 - t / 0.6)
    r1, r2 = 60 + 230 * p, 30 + 120 * p
    pts = []
    for i in range(32):
        a = i * math.pi / 16 + 0.1
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + shake + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(255, 210, 0), outline=(255, 90, 0), width=8)
    outlined(d, (cx + shake, cy), "バチン！", font(FONT_LABEL, int(70 + 60 * p)), RED, 10, WHITE)
    for i in range(14):
        a = i * math.pi / 7
        l0, l1 = r1 + 20, r1 + 20 + 80 * p
        d.line([(cx + l0 * math.cos(a), cy + l0 * math.sin(a)), (cx + l1 * math.cos(a), cy + l1 * math.sin(a))],
               fill=WHITE, width=6)


def scene_speed(d, t, dur, sc, script):
    p = ease(t / 1.2)
    f = font(FONT_LABEL, 50)
    rows = [("シャコのパンチ", 83, RED, "時速80km超"), ("一般道の車", 60, (190, 190, 190), "時速60km")]
    x0, maxw = 60, 700
    for i, (name, v, col, val) in enumerate(rows):
        y = 230 + i * 190
        outlined(d, (x0, y - 55), name, f, WHITE, 6, BLACK, "lm")
        w = int(maxw * (v / 90) * p)
        d.rounded_rectangle([x0, y, x0 + max(w, 10), y + 80], 16, fill=col, outline=WHITE, width=4)
        if p > 0.6:
            outlined(d, (x0 + w + 20, y + 40), val, font(FONT_LABEL, 44), WHITE, 6, BLACK, "lm")
    # スピード線
    for i in range(8):
        y = 200 + i * 50
        xs = (t * 1800 + i * 230) % (W + 300) - 300
        d.line([(xs, y), (xs + 200, y)], fill=(220, 240, 255), width=3)
    outlined(d, (W // 2, 600), "秒速 約23m", font(FONT_LABEL, 52), YELLOW, 7)


def scene_force(d, t, dur, sc, script):
    p = ease(t / 1.5)
    # シャコの体重（小さい箱）
    d.rounded_rectangle([90, 420, 210, 520], 12, fill=(255, 140, 60), outline=WHITE, width=4)
    outlined(d, (150, 560), "体重", font(FONT_LABEL, 44), WHITE, 6)
    # 力（大きくなる柱）
    hmax = 280
    hh = int(hmax * p)
    d.rounded_rectangle([300, 520 - hh, 500, 520], 16, fill=RED, outline=WHITE, width=5)
    outlined(d, (400, 560), "パンチの力", font(FONT_LABEL, 44), WHITE, 6)
    if p > 0.5:
        outlined(d, (400, 520 - hh - 40), "×数千倍", font(FONT_LABEL, 54), YELLOW, 8)
    # 貝殻（後半で割れる）
    cx, cy = 840, 400
    broken = t > dur * 0.55
    off = 40 * ease((t - dur * 0.55) / 0.4) if broken else 0
    shell = [(cx - 130, cy + 60), (cx, cy - 110), (cx + 130, cy + 60)]
    if not broken:
        d.chord([cx - 140, cy - 120, cx + 140, cy + 140], 180, 360, fill=(240, 220, 190), outline=WHITE, width=5)
        for k in range(-2, 3):
            d.line([(cx + k * 45, cy + 10), (cx + k * 20, cy - 110)], fill=(190, 150, 110), width=4)
    else:
        d.chord([cx - 140 - off, cy - 120, cx + 140 - off, cy + 140], 180, 270, fill=(240, 220, 190), outline=WHITE, width=5)
        d.chord([cx - 140 + off, cy - 120, cx + 140 + off, cy + 140], 270, 360, fill=(240, 220, 190), outline=WHITE, width=5)
        outlined(d, (cx, cy + 150), "パキッ！", font(FONT_LABEL, 64), YELLOW, 8)
    del shell


def scene_bubble(d, t, dur, sc, script):
    q = t / dur
    tx, ty = 820, 380
    # 獲物（貝）
    d.ellipse([tx - 70, ty - 50, tx + 70, ty + 50], fill=(240, 220, 190), outline=WHITE, width=5)
    # ハサミ（腕）
    reach = ease(q / 0.25)
    hx = 120 + (tx - 200 - 120) * reach
    d.rounded_rectangle([60, ty - 25, hx, ty + 25], 12, fill=(255, 140, 60), outline=WHITE, width=4)
    d.ellipse([hx - 40, ty - 55, hx + 60, ty + 55], fill=(255, 110, 40), outline=WHITE, width=5)
    outlined(d, (360, 200), "1. ハサミが当たる", font(FONT_LABEL, 46), WHITE if q < 0.4 else (150, 150, 150), 6)
    # 泡
    if q > 0.3:
        g = ease((q - 0.3) / 0.25)
        collapse = ease((q - 0.62) / 0.12) if q > 0.62 else 0
        r = 85 * g * (1 - collapse)
        bx, by = hx + 115, ty
        if r > 2:
            d.ellipse([bx - r, by - r, bx + r, by + r], outline=(200, 240, 255), width=7)
        outlined(d, (360, 280), "2. 泡ができる", font(FONT_LABEL, 46), WHITE if q < 0.65 else (150, 150, 150), 6)
        if collapse > 0.5:
            for i in range(12):
                a = i * math.pi / 6
                d.line([(bx + 20 * math.cos(a), by + 20 * math.sin(a)), (bx + 140 * math.cos(a), by + 140 * math.sin(a))],
                       fill=YELLOW, width=7)
            outlined(d, (W // 2, 560), "3. 泡がつぶれて2発目！", font(FONT_LABEL, 56), YELLOW, 8)


def scene_glass(d, t, dur, sc, script):
    x0, y0, x1, y1 = 160, 210, 920, 610
    d.rectangle([x0, y0, x1, y1], outline=(200, 235, 255), width=10)
    d.rectangle([x0 + 10, y0 + 120, x1 - 10, y1 - 10], fill=(40, 120, 180))
    outlined(d, (x0 + 80, y0 + 50), "水槽", font(FONT_LABEL, 44), WHITE, 6)
    p = ease((t - 0.4) / 1.2)
    cx, cy = 600, 380
    rr = random.Random(3)
    for i in range(10):
        a = i * math.pi / 5 + rr.uniform(-0.2, 0.2)
        ln = rr.uniform(120, 260) * p
        mx, my = cx + ln * 0.5 * math.cos(a + 0.15), cy + ln * 0.5 * math.sin(a + 0.15)
        ex, ey = cx + ln * math.cos(a), cy + ln * math.sin(a)
        d.line([(cx, cy), (mx, my), (ex, ey)], fill=WHITE, width=5)


def scene_next(d, t, dur, sc, script):
    p = ease(t / 0.5)
    outlined(d, (int(W // 2 - 600 * (1 - p)), 230), "NEXT", font(FONT_LABEL, 130), YELLOW, 10)
    outlined(d, (int(W // 2 + 600 * (1 - p)), 420), script.get("next_title", ""), font(FONT_LABEL, 120), WHITE, 10)


SCENES = {"hook": scene_hook, "speed": scene_speed, "force": scene_force,
          "bubble": scene_bubble, "glass": scene_glass, "next": scene_next}


# ---------- 写真ショット（フリー素材） ----------
MID_W, MID_H = W, MID_Y1 - MID_Y0
_photo_cache = {}


def load_photo(proj, name):
    if name not in _photo_cache:
        _photo_cache[name] = Image.open(proj / "assets" / f"{name}.jpg").convert("RGB")
    return _photo_cache[name]


def render_shot(img, shot, p):
    """ゆっくりズーム＋パン（ケン・バーンズ）。p は 0→1 の進み具合"""
    iw, ih = img.size
    aspect = MID_W / MID_H
    bw, bh = (iw, iw / aspect) if iw / ih < aspect else (ih * aspect, ih)
    z0, z1 = shot.get("zoom", [1.05, 1.18])
    z = z0 + (z1 - z0) * p
    cw, ch = bw / z, bh / z
    fx, fy = shot.get("focus", [0.5, 0.5])
    dx, dy = shot.get("pan", [0, 0])
    cx = (fx + dx * (p - 0.5)) * iw
    cy = (fy + dy * (p - 0.5)) * ih
    cw, ch = min(cw, iw), min(ch, ih)
    x0 = max(0.0, min(cx - cw / 2, iw - cw))
    y0 = max(0.0, min(cy - ch / 2, ih - ch))
    return img.resize((MID_W, MID_H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), (x0, y0, cw, ch)


def img_to_screen(pt, crop):
    x0, y0, cw, ch = crop
    return ((pt[0] - x0) / cw * MID_W, (pt[1] - y0) / ch * MID_H)


def scribble_circle(d, center, r, prog, seed=1, color=(255, 30, 30), width=9):
    """手描きっぽいゆがんだ丸を、ペンで描くように少しずつ描く"""
    rr = random.Random(seed)
    k1, k2 = rr.uniform(0.04, 0.09), rr.uniform(0.03, 0.07)
    ph1, ph2 = rr.uniform(0, 6), rr.uniform(0, 6)
    n = int(60 * min(1, prog))
    a0 = rr.uniform(0, 6.28)
    pts = []
    for i in range(n + 1):
        a = a0 + i / 60 * 2 * math.pi * 1.12
        rad = r * (1 + k1 * math.sin(3 * a + ph1) + k2 * math.sin(5 * a + ph2))
        pts.append((center[0] + rad * 1.15 * math.cos(a), center[1] + rad * math.sin(a)))
    if len(pts) > 1:
        d.line(pts, fill=color, width=width, joint="curve")


def tilted_label(mid, text, color, st, angle, pos):
    """少し傾けたテロップを、ポンと出す"""
    pop = 1 + 0.35 * max(0, 1 - st / 0.12)
    f = font(FONT_LABEL, int(96 * pop))
    tmp = Image.new("RGBA", (1100, 260), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((550, 130), text, font=f, fill=color, anchor="mm", stroke_width=10, stroke_fill=BLACK)
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, expand=False)
    mid.paste(tmp, (int(pos[0] - 550), int(pos[1] - 130)), tmp)


def draw_credit(d, text):
    f = font(FONT_SUB, 22)
    d.text((MID_W - 14, MID_H - 12), text, font=f, fill=(235, 235, 235), anchor="rd",
           stroke_width=2, stroke_fill=BLACK)


def credit_short(c):
    if c.get("short"):
        return c["short"]
    if c["license"] == "CC0":
        return "写真: iNaturalist (CC0)"
    who = c["attribution"].replace("(c) ", "").split(",")[0]
    return f"写真: {who} / iNaturalist ({c['license']})"



# ---------- 写真に重ねる図解パネル ----------
def panel(ov, box, alpha=170):
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle(box, 24, fill=(0, 0, 0, alpha), outline=(255, 255, 255, 230), width=4)
    return d


def ov_speed_chart(ov, lt, dur):
    """棒グラフ：シャコのパンチ vs 一般道の車"""
    d = panel(ov, (40, 150, 1040, 560))
    p = ease(lt / 0.9)
    f = font(FONT_LABEL, 44)
    rows = [("シャコのパンチ", 83, (235, 30, 30), "時速80km超"), ("一般道の車", 60, (200, 200, 200), "時速60km")]
    for i, (name, v, col, val) in enumerate(rows):
        y = 245 + i * 150
        d.text((80, y - 40), name, font=f, fill=WHITE, anchor="lm", stroke_width=4, stroke_fill=BLACK)
        w = int(640 * v / 90 * p)
        d.rounded_rectangle((80, y, 80 + max(w, 12), y + 70), 14, fill=col + (255,), outline=WHITE, width=3)
        if p > 0.7:
            d.text((100 + w, y + 35), val, font=font(FONT_LABEL, 46), fill=YELLOW, anchor="lm",
                   stroke_width=6, stroke_fill=BLACK)
    d.text((540, 525), "パンチの速さ：秒速 約23m", font=font(FONT_SUB, 34), fill=WHITE, anchor="mm")


def ov_shell_crack(ov, lt, dur):
    """貝殻が割れる図"""
    d = panel(ov, (620, 170, 1040, 560))
    cx, cy = 830, 380
    broken = lt > 0.9
    off = 34 * ease((lt - 0.9) / 0.3) if broken else 0
    shell = (240, 220, 190, 255)
    if not broken:
        d.chord((cx - 130, cy - 110, cx + 130, cy + 130), 180, 360, fill=shell, outline=WHITE, width=5)
        for k in range(-2, 3):
            d.line([(cx + k * 42, cy + 10), (cx + k * 18, cy - 100)], fill=(190, 150, 110, 255), width=4)
        # 近づく腕
        ax = 640 + 120 * ease(lt / 0.9)
        d.rounded_rectangle((620, cy - 18, ax, cy + 18), 10, fill=(255, 120, 50, 255))
    else:
        d.chord((cx - 130 - off, cy - 110, cx + 130 - off, cy + 130), 180, 270, fill=shell, outline=WHITE, width=5)
        d.chord((cx - 130 + off, cy - 110, cx + 130 + off, cy + 130), 270, 360, fill=shell, outline=WHITE, width=5)
        d.text((cx, cy + 120), "パキッ！", font=font(FONT_LABEL, 60), fill=YELLOW, anchor="mm",
               stroke_width=7, stroke_fill=BLACK)


def ov_bubble_steps(ov, lt, dur):
    """泡で2発目が入るしくみ（3ステップ）"""
    d = panel(ov, (40, 160, 1040, 600))
    q = lt / max(dur, 0.1)
    ty = 400
    tx = 860
    d.ellipse((tx - 60, ty - 45, tx + 60, ty + 45), fill=(240, 220, 190, 255), outline=WHITE, width=4)
    d.text((tx, ty + 75), "貝", font=font(FONT_SUB, 36), fill=WHITE, anchor="mm")
    reach = ease(q / 0.25)
    hx = 120 + (tx - 230 - 120) * reach
    d.rounded_rectangle((80, ty - 20, hx, ty + 20), 10, fill=(255, 140, 60, 255), outline=WHITE, width=3)
    d.ellipse((hx - 35, ty - 48, hx + 55, ty + 48), fill=(255, 110, 40, 255), outline=WHITE, width=4)
    steps = [("1 腕がぶつかる", 0.0), ("2 泡ができる", 0.3), ("3 泡がつぶれて衝撃！", 0.62)]
    for i, (txt, t0) in enumerate(steps):
        if q >= t0:
            current = i == 2 or q < steps[i + 1][1]
            col = YELLOW if current else (180, 180, 180)
            d.text((540 if i == 2 else 80 + i * 330, 215 if i < 2 else 555), txt, font=font(FONT_LABEL, 42),
                   fill=col, anchor="mm" if i == 2 else "lm", stroke_width=5, stroke_fill=BLACK)
    if q > 0.3:
        g = ease((q - 0.3) / 0.25)
        collapse = ease((q - 0.62) / 0.12) if q > 0.62 else 0
        r = 70 * g * (1 - collapse)
        bx = hx + 110
        if r > 2:
            d.ellipse((bx - r, ty - r, bx + r, ty + r), outline=(200, 240, 255, 255), width=6)
        if collapse > 0.5:
            for i in range(12):
                a = i * math.pi / 6
                d.line([(bx + 18 * math.cos(a), ty + 18 * math.sin(a)), (bx + 120 * math.cos(a), ty + 120 * math.sin(a))],
                       fill=YELLOW + (255,), width=6)


def ov_two_peaks(ov, lt, dur):
    """力のグラフ：1回のパンチで山が2つ（イメージ図）"""
    d = panel(ov, (60, 170, 1020, 590))
    x0, y0, x1, y1 = 130, 520, 960, 230
    d.line([(x0, y0), (x1, y0)], fill=WHITE + (255,), width=4)
    d.line([(x0, y0), (x0, y1)], fill=WHITE + (255,), width=4)
    d.text((x1, y0 + 30), "時間", font=font(FONT_SUB, 30), fill=WHITE, anchor="rm")
    d.text((x0 + 10, y1 - 10), "衝撃の強さ", font=font(FONT_SUB, 30), fill=WHITE, anchor="lm")
    p = ease(lt / 1.4)
    pts = []
    n = int(200 * p)
    for i in range(n + 1):
        u = i / 200
        v = 0.95 * math.exp(-((u - 0.3) / 0.045) ** 2) + 0.7 * math.exp(-((u - 0.62) / 0.03) ** 2)
        pts.append((x0 + u * (x1 - x0), y0 - v * (y0 - y1 - 20)))
    if len(pts) > 1:
        d.line(pts, fill=(255, 60, 60, 255), width=7, joint="curve")
    if p > 0.45:
        d.text((x0 + 0.3 * (x1 - x0) + 40, y1 + 25), "1発目（腕）", font=font(FONT_LABEL, 36), fill=YELLOW, anchor="lm",
               stroke_width=5, stroke_fill=BLACK)
    if p > 0.8:
        d.text((x0 + 0.62 * (x1 - x0) + 40, y1 + 60), "2発目（泡）", font=font(FONT_LABEL, 36), fill=YELLOW,
               anchor="lm", stroke_width=5, stroke_fill=BLACK)
    d.text((1000, 575), "※イメージ図", font=font(FONT_SUB, 24), fill=(220, 220, 220), anchor="rm")


def ov_glass_crack(ov, lt, dur):
    """画面全体にガラスのヒビ"""
    d = ImageDraw.Draw(ov)
    p = ease((lt - 0.3) / 0.6)
    cx, cy = 690, 330
    rr = random.Random(5)
    for i in range(14):
        a = i * 2 * math.pi / 14 + rr.uniform(-0.15, 0.15)
        ln = rr.uniform(260, 620) * p
        pts = [(cx, cy)]
        for k in range(1, 5):
            r = ln * k / 4
            pts.append((cx + r * math.cos(a) + rr.uniform(-14, 14), cy + r * math.sin(a) + rr.uniform(-14, 14)))
        d.line(pts, fill=(255, 255, 255, 230), width=4)
    if p > 0.5:
        for r in (70, 150):
            d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=(255, 255, 255, 160), width=3)


OVERLAYS = {"speed_chart": ov_speed_chart, "shell_crack": ov_shell_crack, "bubble_steps": ov_bubble_steps,
            "two_peaks": ov_two_peaks, "glass_crack": ov_glass_crack}


# ---------- 冒頭のパンチ（動画素材 or 写真での再現） ----------
_clip_cache = {}


def load_clip(proj, name):
    """assets/<name> の動画を中段サイズ（1080x652）のフレーム列にする"""
    if name not in _clip_cache:
        cmd = ["ffmpeg", "-v", "error", "-i", str(proj / "assets" / name), "-vf",
               f"scale={MID_W}:{MID_H}:force_original_aspect_ratio=increase,crop={MID_W}:{MID_H},fps={FPS}",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        raw = subprocess.run(cmd, check=True, capture_output=True).stdout
        n = len(raw) // (MID_W * MID_H * 3)
        size = MID_W * MID_H * 3
        _clip_cache[name] = [Image.frombytes("RGB", (MID_W, MID_H), raw[i * size:(i + 1) * size]) for i in range(n)]
    return _clip_cache[name]


def punch_fx(mid, lt, center, hit=0.32, pre=True):
    """パンチの瞬間の演出：（溜めのスピード線）→フラッシュ→衝撃線→「ドンッ」。hit は当たる時刻"""
    d = ImageDraw.Draw(mid, "RGBA")
    if lt < hit and not pre:
        return mid
    if lt < hit:  # 溜め：スピード線が中心に集まる
        k = lt / hit
        for i in range(28):
            a = i * 2 * math.pi / 28
            r0 = 700 - 380 * k
            d.line([(center[0] + r0 * math.cos(a), center[1] + r0 * math.sin(a)),
                    (center[0] + (r0 + 260) * math.cos(a), center[1] + (r0 + 260) * math.sin(a))],
                   fill=(255, 255, 255, 170), width=5)
        return mid
    u = lt - hit
    if u < 0.1:
        mid = Image.blend(mid, Image.new("RGB", mid.size, WHITE), 1 - u / 0.1)
        d = ImageDraw.Draw(mid, "RGBA")
    if u < 0.9:
        for i in range(18):
            a = i * 2 * math.pi / 18 + 0.1
            r0, r1 = 90 + 400 * ease(u / 0.25), 200 + 560 * ease(u / 0.25)
            d.line([(center[0] + r0 * math.cos(a), center[1] + r0 * math.sin(a)),
                    (center[0] + r1 * math.cos(a), center[1] + r1 * math.sin(a))], fill=(255, 230, 0, 230), width=9)
    if u < 2.2:
        tilted_label(mid, "ドンッ！", YELLOW, u, -8, (center[0] + 230, center[1] - 120))
    return mid

# ---------- タイミングと音声 ----------
def build_timeline(script, voice_dir):
    items, t, idx = [], 0.0, 0
    have_voice = False
    for si, sc in enumerate(script["scenes"]):
        s_start = t
        for ln in sc["lines"]:
            idx += 1
            wav = voice_dir / f"{idx:02d}.wav"
            if wav.exists():
                with wave.open(str(wav)) as w:
                    dur = w.getnframes() / w.getframerate()
                have_voice = True
            else:
                dur = SEC_PER_CHAR * len(ln["yomi"]) + 0.3
                wav = None
            items.append({"scene": si, "text": ln["text"], "start": t, "end": t + dur + LINE_PAD, "wav": wav,
                          "line": ln})
            t += dur + LINE_PAD
        sc["_start"], sc["_end"] = s_start, t
    return items, t + TAIL, have_voice


def build_audio(items, total, out_wav):
    params = None
    for it in items:
        if it["wav"]:
            with wave.open(str(it["wav"])) as w:
                params = w.getparams()
            break
    rate, ch, sw = params.framerate, params.nchannels, params.sampwidth
    buf = bytearray(int(total * rate) * ch * sw)
    for it in items:
        if not it["wav"]:
            continue
        with wave.open(str(it["wav"])) as w:
            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (rate, ch, sw):
                sys.exit(f"音声形式がそろっていません: {it['wav']}")
            data = w.readframes(w.getnframes())
        off = int(it["start"] * rate) * ch * sw
        buf[off:off + len(data)] = data[:len(buf) - off]
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(sw)
        w.setframerate(rate)
        w.writeframes(bytes(buf))


# ---------- メイン ----------
def main(proj):
    proj = Path(proj)
    script = json.loads((proj / "script.json").read_text(encoding="utf-8"))
    out = proj / "out"
    out.mkdir(exist_ok=True)
    items, total, have_voice = build_timeline(script, proj / "voice")

    # VOICEVOX 用のテキスト（1行＝1音声。テキスト読み込みでそのまま使える）
    yomi = [ln["yomi"] for sc in script["scenes"] for ln in sc["lines"]]
    (out / "voicevox_import.txt").write_text("\n".join(yomi) + "\n", encoding="utf-8")
    credits = {}
    cpath = proj / "assets" / "credits.json"
    if cpath.exists():
        credits = json.loads(cpath.read_text(encoding="utf-8"))
    used = []
    for sc in script["scenes"]:
        for ln in sc["lines"]:
            sh = ln.get("shot", {})
            for n in (sh.get("clip"), sh.get("img")):
                if n and n in credits and n not in used and (n != sh.get("img") or not sh.get("clip")
                                                             or not (proj / "assets" / sh["clip"]).exists()):
                    used.append(n)
    cred_txt = ""
    if used:
        cred_txt = "\n\n素材クレジット\n" + "\n".join(
            f"・{credits[n]['attribution']} {credits[n]['source']}" for n in used if n in credits)
    (out / "description.txt").write_text(script["title"] + "\n\n" + script.get("description", "") + cred_txt + "\n",
                                         encoding="utf-8")

    base = build_base(script)
    mid_bg = build_mid_bg()
    tmp = Image.new("RGB", (10, 10))
    md = ImageDraw.Draw(tmp)
    fsub = font(FONT_SUB, 76)
    sub_cache = {}

    audio = None
    if have_voice:
        audio = out / "voice_track.wav"
        build_audio(items, total, audio)

    mp4 = out / "short.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-"]
    bgm = script.get("bgm")
    bgm_path = (proj / bgm["file"]).resolve() if bgm else None
    if bgm_path and not bgm_path.exists():
        sys.exit(f"BGM が見つかりません: {bgm_path}")
    fade = f"afade=t=out:st={max(0.0, total - 1.5):.2f}:d=1.5"
    if audio and bgm_path:
        # 声が鳴っている間だけ BGM を下げる（ダッキング）
        vol = bgm.get("volume_with_voice", 0.22)
        cmd += ["-i", str(audio), "-stream_loop", "-1", "-i", str(bgm_path), "-filter_complex",
                f"[1:a]asplit=2[v1][v2];[2:a]atrim=0:{total:.2f},volume={vol},{fade}[b];"
                f"[b][v1]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[bd];"
                f"[v2][bd]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    elif audio:
        cmd += ["-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"]
    elif bgm_path:
        vol = bgm.get("volume", 0.5)
        cmd += ["-stream_loop", "-1", "-i", str(bgm_path), "-filter_complex",
                f"[1:a]atrim=0:{total:.2f},volume={vol},{fade}[a]",
                "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(mp4)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    nframes = int(math.ceil(total * FPS))
    cur = 0
    for fi in range(nframes):
        t = fi / FPS
        while cur < len(items) - 1 and t >= items[cur]["end"]:
            cur += 1
        it = items[cur]
        sc = script["scenes"][it["scene"]]
        frame = base.copy()
        st = t - sc["_start"]
        shot = it["line"].get("shot")
        if shot:
            lt = t - it["start"]
            prog = lt / max(0.1, it["end"] - it["start"])
            img = load_photo(proj, shot["img"])
            clip = shot.get("clip")
            if clip and (proj / "assets" / clip).exists():
                frames = load_clip(proj, clip)
                k = int(lt * FPS * shot.get("clip_speed", 1.0))
                mid = frames[min(k, len(frames) - 1)].copy()
                crop = (0, 0, img.size[0], img.size[1])
                hit = shot.get("clip_hit")
                if hit is not None:
                    if hit <= lt < hit + 0.45:  # 当たった瞬間の揺れ
                        amp = 22 * (1 - (lt - hit) / 0.45)
                        mid = mid.transform(mid.size, Image.AFFINE,
                                            (1, 0, amp * math.sin(lt * 90), 0, 1, amp * math.cos(lt * 70)))
                    hc = shot.get("clip_hit_pos", [0.5, 0.6])
                    mid = punch_fx(mid, lt, (MID_W * hc[0], MID_H * hc[1]), hit=hit, pre=False)
                shot = {k2: v for k2, v in shot.items() if k2 not in ("circle", "punch")}
                shot["_credit"] = clip
            else:
                sp = dict(shot)
                if shot.get("punch") and lt < 0.45:  # 急ズーム＋揺れ
                    z = 1.0 + 0.9 * ease(lt / 0.32)
                    sp["zoom"] = [z, z]
                    sp["focus"] = shot.get("circle", shot.get("focus", [0.5, 0.5]))[:2]
                mid, crop = render_shot(img, sp, prog)
                if shot.get("punch") and 0.32 <= lt < 0.8:
                    amp = 26 * (1 - (lt - 0.32) / 0.48)
                    mid = mid.transform(mid.size, Image.AFFINE,
                                        (1, 0, amp * math.sin(lt * 90), 0, 1, amp * math.cos(lt * 70)))
                if shot.get("punch"):
                    mid = punch_fx(mid, lt, (MID_W * 0.5, MID_H * 0.5))
            d = ImageDraw.Draw(mid)
            if shot.get("overlay"):
                ov = Image.new("RGBA", mid.size, (0, 0, 0, 0))
                OVERLAYS[shot["overlay"]](ov, lt, it["end"] - it["start"])
                mid = Image.alpha_composite(mid.convert("RGBA"), ov).convert("RGB")
                d = ImageDraw.Draw(mid)
            if shot.get("flash") and lt < 0.12:
                mid = Image.blend(mid, Image.new("RGB", mid.size, WHITE), 1 - lt / 0.12)
                d = ImageDraw.Draw(mid)
            if "circle" in shot and lt > shot.get("circle_at", 0.35):
                cx, cy, cr = shot["circle"]
                iw, ih = img.size
                center = img_to_screen((cx * iw, cy * ih), crop)
                scribble_circle(d, center, cr * MID_W, (lt - shot.get("circle_at", 0.35)) / 0.45, seed=len(it["text"]))
            ckey = shot.get("_credit", shot["img"])
            if ckey in credits:
                draw_credit(d, credit_short(credits[ckey]))
            lab = it["line"].get("label")
            if lab:
                tilted_label(mid, lab["text"], COLORS[lab["color"]], lt, lab.get("angle", 4),
                             lab.get("pos", [W // 2, 95]))
        else:
            mid = mid_bg.copy()
            d = ImageDraw.Draw(mid)
            draw_bubbles(d, t)
            SCENES[sc["visual"]](d, st, sc["_end"] - sc["_start"], sc, script)
            lab = sc.get("label")
            if lab:
                pop = 1 + 0.25 * max(0, 1 - st / 0.2)
                outlined(d, (W // 2, 80), lab["text"], font(FONT_LABEL, int(100 * pop)), COLORS[lab["color"]], 9)
        frame.paste(mid, (0, MID_Y0))
        fd = ImageDraw.Draw(frame)
        if it["text"] not in sub_cache:
            lines = balanced_wrap(md, it["text"], fsub, 1000, 6)[:3]
            size = 76
            while size > 50 and max(text_w(md, ln, font(FONT_SUB, size), 6) for ln in lines) > 1020:
                size -= 2
            sub_cache[it["text"]] = (lines, font(FONT_SUB, size))
        lines, fs = sub_cache[it["text"]]
        for i, line in enumerate(lines):
            fd.text((W // 2, SUB_Y0 + 45 + i * 110), line, font=fs, fill=WHITE, anchor="mm",
                    stroke_width=6, stroke_fill=SUB_OUTLINE)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg に失敗しました")

    print(f"出力: {mp4}  長さ: {total:.1f}秒  音声: {'あり' if have_voice else 'なし（推定タイミング）'}"
          f"  BGM: {bgm['file'] if bgm else 'なし'}")
    print(f"VOICEVOX 用テキスト: {out / 'voicevox_import.txt'}（{len(yomi)}行）")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "shorts/shako")
