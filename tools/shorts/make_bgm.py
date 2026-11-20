#!/usr/bin/env python3
"""ショート用のシンプルなBGMを合成する（自作音源なので著作権の心配なし）

使い方:
    python3 tools/shorts/make_bgm.py tools/shorts/bgm/light_pop.wav [秒数]
    ffmpeg -i tools/shorts/bgm/light_pop.wav -c:a aac -b:a 160k tools/shorts/bgm/light_pop.m4a  # リポジトリには m4a で置く

明るめのポップ: 105BPM / C - G - Am - F の繰り返し / プラック系のコード + ベース + 軽いドラム
ナレーションの邪魔にならないよう、中高域は控えめ・音数少なめにしている。
"""
import sys
import wave

import numpy as np

SR = 44100
BPM = 105
BEAT = 60 / BPM

NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def freq(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave + 1) - 69) / 12)


CHORDS = [  # (ルート, 構成音)
    ("C", [("C", 4), ("E", 4), ("G", 4)]),
    ("G", [("B", 3), ("D", 4), ("G", 4)]),
    ("A", [("A", 3), ("C", 4), ("E", 4)]),
    ("F", [("A", 3), ("C", 4), ("F", 4)]),
]


def env(n, attack=0.005, decay=0.25):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def pluck(f, dur, decay=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = 0.6 * np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t)
    return w * env(n, 0.004, decay)


def bass(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return w * env(n, 0.01, 0.5)


def kick(dur=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 120 * np.exp(-t * 18) + 45
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def hat(dur=0.06, seed=0):
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    x = np.diff(x, prepend=0)  # 高域寄りに
    return x * np.exp(-np.arange(n) / SR * 70)


def snap(dur=0.18, seed=1):
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    return (rng.standard_normal(n) * 0.6 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 22)


def add(buf, sig, start, gain):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i] * gain


def make(seconds):
    bars = int(np.ceil(seconds / (BEAT * 4)))
    total = bars * 4 * BEAT
    mix = np.zeros(int(total * SR) + SR)
    for b in range(bars):
        root, notes = CHORDS[b % 4]
        t0 = b * 4 * BEAT
        # コード：8分の裏で軽く刻む（アルペジオ気味）
        pattern = [0, 1, 2, 1, 0, 2, 1, 2]
        for k, idx in enumerate(pattern):
            nm, oc = notes[idx]
            add(mix, pluck(freq(nm, oc + 1), BEAT * 0.9, 0.28), t0 + k * BEAT / 2, 0.16)
        # ベース：1拍目と3拍目、3拍目裏
        rf = freq(root, 2)
        for st, g in ((0, 0.42), (2, 0.36), (2.5, 0.28)):
            add(mix, bass(rf, BEAT * 1.2), t0 + st * BEAT, g)
        # ドラム：キック1・3拍、スナップ2・4拍、ハット8分
        for st in (0, 2):
            add(mix, kick(), t0 + st * BEAT, 0.55)
        for st in (1, 3):
            add(mix, snap(seed=b * 4 + st), t0 + st * BEAT, 0.16)
        for k in range(8):
            add(mix, hat(seed=b * 8 + k), t0 + k * BEAT / 2, 0.05 if k % 2 == 0 else 0.08)
    mix = mix[: int(seconds * SR)]
    # フェードイン／アウト
    fi, fo = int(0.3 * SR), int(1.5 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 0.89  # 約 -1 dBFS
    return mix


def save(path, x):
    st = np.stack([x, x], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "tools/shorts/bgm/light_pop.wav"
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 64
    save(out, make(secs))
    print(f"出力: {out}（{secs:.0f}秒）")
