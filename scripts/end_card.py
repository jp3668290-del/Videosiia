#!/usr/bin/env python3
"""Genera la escena 6 (cierre promocional) de DRIPCORNER.ES.

Vídeo vertical 1080x1920, 30 fps, 7 s, con beat urbano sintetizado.
Uso: python3 scripts/end_card.py [salida.mp4]
"""
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 7.0
BPM = 140
BEAT = 60 / BPM
FONT_DIR = "/usr/share/fonts/opentype/inter/"
F_BLACK = FONT_DIR + "InterDisplay-Black.otf"
F_XBOLD = FONT_DIR + "InterDisplay-ExtraBold.otf"
F_BLACK_IT = FONT_DIR + "InterDisplay-BlackItalic.otf"

ACCENT = (255, 214, 0)      # amarillo "drip"
PURPLE = (124, 44, 255)
ORANGE = (255, 106, 0)
WHITE = (255, 255, 255)

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output" / "escena6_dripcorner_cierre.mp4"
TMP = ROOT / "output" / ".tmp"


# ---------------------------------------------------------------- utilidades
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur)


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def ease_out_back(x, s=1.9):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def ease_in_out(x):
    return 0.5 - 0.5 * math.cos(math.pi * x)


def text_img(text, font_path, size, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0)):
    font = ImageFont.truetype(font_path, size)
    l, t, r, b = font.getbbox(text, stroke_width=stroke)
    pad = 8 + stroke
    img = Image.new("RGBA", (r - l + pad * 2, b - t + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=font, fill=fill,
                             stroke_width=stroke, stroke_fill=stroke_fill)
    return img


def glow(img, radius, color, strength=1.0):
    pad = radius * 3
    base = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    a = img.split()[3]
    solid = Image.new("RGBA", img.size, color + (255,))
    solid.putalpha(a.point(lambda v: int(v * strength)))
    base.paste(solid, (pad, pad), solid)
    return base.filter(ImageFilter.GaussianBlur(radius)), pad


def with_alpha(img, alpha):
    if alpha >= 0.999:
        return img
    out = img.copy()
    out.putalpha(img.split()[3].point(lambda v: int(v * alpha)))
    return out


def paste_center(canvas, img, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01:
        return
    if abs(scale - 1) > 0.002:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                         Image.LANCZOS)
    img = with_alpha(img, alpha)
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


# ---------------------------------------------------------------- fondo
yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32) * 4


def background(t, pulse):
    # dos focos de luz (morado / naranja) que orbitan despacio
    c1 = (W * (0.3 + 0.15 * math.sin(t * 0.9)), H * (0.32 + 0.06 * math.cos(t * 0.7)))
    c2 = (W * (0.75 + 0.12 * math.cos(t * 0.8)), H * (0.72 + 0.05 * math.sin(t * 1.1)))
    d1 = np.exp(-((xx - c1[0]) ** 2 + (yy - c1[1]) ** 2) / (2 * 380 ** 2))
    d2 = np.exp(-((xx - c2[0]) ** 2 + (yy - c2[1]) ** 2) / (2 * 420 ** 2))
    k = 0.55 + 0.25 * pulse
    rgb = np.zeros((H // 4, W // 4, 3), np.float32) + np.array([8, 8, 14], np.float32)
    rgb += d1[..., None] * np.array(PURPLE, np.float32) * k
    rgb += d2[..., None] * np.array(ORANGE, np.float32) * k * 0.8
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    # rejilla en perspectiva que avanza (suelo "pasarela")
    horizon = H * 0.58
    for i in range(14):
        z = ((i + (t * 1.6) % 1) / 14)
        y = horizon + (H - horizon) * z ** 2
        d.line([(0, y), (W, y)], fill=(255, 255, 255, int(10 + 40 * z)), width=2)
    for i in range(-10, 11):
        d.line([(W / 2 + i * 30, horizon), (W / 2 + i * 260, H)], fill=(255, 255, 255, 22), width=2)
    return img


def sweep(canvas, t):
    """Transición de entrada: flash + barras diagonales."""
    p = prog(t, 0, 0.75)
    if p >= 1:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    colors = [ACCENT, WHITE, PURPLE, ORANGE]
    for i, c in enumerate(colors):
        off = (ease_in_out(clamp(p * 1.4 - i * 0.12)) * 2.6 - 0.8) * (W + H)
        bw = 220
        poly = [(off - H, H), (off, 0), (off + bw, 0), (off + bw - H, H)]
        d.polygon(poly, fill=c + (235,))
    canvas.alpha_composite(layer)
    flash = 1 - ease_out_cubic(prog(t, 0, 0.35))
    if flash > 0:
        canvas.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * flash))))


# ---------------------------------------------------------------- recursos de texto
LOGO = "DRIPCORNER"
letters = [text_img(ch, F_BLACK_IT, 150) for ch in LOGO]
dot_es = text_img(".ES", F_BLACK_IT, 150, fill=ACCENT)
logo_full = Image.new("RGBA", (sum(l.width - 14 for l in letters) + dot_es.width + 20, letters[0].height),
                      (0, 0, 0, 0))
_x = 0
letter_pos = []
for l in letters:
    letter_pos.append(_x + l.width / 2)
    logo_full.alpha_composite(l, (_x, 0))
    _x += l.width - 14
dot_pos = _x + dot_es.width / 2
logo_full.alpha_composite(dot_es, (_x, 0))
logo_w = logo_full.width
logo_glow, logo_glow_pad = glow(logo_full, 28, PURPLE, 0.9)

tag1 = text_img("TU ESTILO,", F_BLACK, 118, stroke=6)
tag2 = text_img("A OTRO NIVEL", F_BLACK, 118, fill=ACCENT, stroke=6)
desc1 = text_img("DESCUBRE", F_XBOLD, 92, stroke=5)
desc2_txt = text_img("DRIPCORNER.ES", F_BLACK, 96, fill=(10, 10, 14))
cta_txt = text_img("LINK EN LA BIO", F_BLACK, 84, fill=(10, 10, 14))
arrow = text_img("↓", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120, fill=ACCENT)


def pill(txt_img, color, padx=60, pady=34):
    w, h = txt_img.width + padx * 2, txt_img.height + pady * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=color + (255,))
    img.alpha_composite(txt_img, (padx, pady))
    return img


desc2 = pill(desc2_txt, ACCENT)
cta = pill(cta_txt, WHITE, 70, 38)
cta_glow, cta_glow_pad = glow(cta, 30, ACCENT, 0.8)


# ---------------------------------------------------------------- composición por fotograma
def beat_pulse(t):
    ph = (t % BEAT) / BEAT
    return math.exp(-ph * 6)


def frame(t):
    pulse = beat_pulse(t) if t > 0.6 else 0
    canvas = background(t, pulse)

    # --- logo: entra letra a letra, luego sube y se reduce
    move = ease_in_out(prog(t, 2.1, 0.6))
    logo_cy = 760 - move * 330
    logo_scale = (1.0 - move * 0.22) * (1 + 0.025 * pulse)
    max_w = W - 80
    fit = min(1.0, max_w / logo_w)
    s = logo_scale * fit
    x0 = W / 2 - logo_w * s / 2
    ga = ease_out_cubic(prog(t, 1.4, 0.5))
    if ga > 0:
        paste_center(canvas, logo_glow, W / 2, logo_cy, s, ga * (0.7 + 0.3 * pulse))
    for i, (l, px) in enumerate(zip(letters, letter_pos)):
        p = prog(t, 0.35 + i * 0.07, 0.45)
        if p <= 0:
            continue
        sc = s * (2.2 - 1.2 * ease_out_back(p))
        paste_center(canvas, l, x0 + px * s, logo_cy - (1 - ease_out_cubic(p)) * 120, sc,
                     ease_out_cubic(p))
    p = prog(t, 0.35 + len(letters) * 0.07, 0.4)
    if p > 0:
        paste_center(canvas, dot_es, x0 + dot_pos * s + (1 - ease_out_cubic(p)) * 300, logo_cy,
                     s * (0.6 + 0.4 * ease_out_back(p)), ease_out_cubic(p))
    # subrayado
    p = ease_out_cubic(prog(t, 1.3, 0.5))
    if p > 0:
        d = ImageDraw.Draw(canvas)
        bw = logo_w * s * p
        y = logo_cy + 105 * s
        d.rounded_rectangle((W / 2 - bw / 2, y, W / 2 + bw / 2, y + 14 * s), radius=6, fill=ACCENT)

    # --- "TU ESTILO, / A OTRO NIVEL"  (2.4 – 4.2 s)
    out = ease_in_out(prog(t, 4.05, 0.3))
    for img, st, cy in ((tag1, 2.45, 920), (tag2, 2.75, 1060)):
        p = prog(t, st, 0.4)
        if p > 0 and out < 1:
            e = ease_out_back(p, 1.4)
            paste_center(canvas, img, W / 2 - out * W, cy + (1 - e) * 90,
                         (0.85 + 0.15 * e) * (1 + 0.03 * pulse * (img is tag2)),
                         ease_out_cubic(p))

    # --- "DESCUBRE / DRIPCORNER.ES" (4.2 – 7 s)
    p = prog(t, 4.2, 0.35)
    if p > 0:
        paste_center(canvas, desc1, W / 2 + (1 - ease_out_cubic(p)) * W, 920, 1, ease_out_cubic(p))
    p = prog(t, 4.45, 0.4)
    if p > 0:
        paste_center(canvas, desc2, W / 2, 1065, 0.5 + 0.5 * ease_out_back(p), ease_out_cubic(p))

    # --- CTA "LINK EN LA BIO" (5.1 – 7 s)
    p = prog(t, 5.1, 0.45)
    if p > 0:
        e = ease_out_back(p)
        sc = (0.6 + 0.4 * e) * (1 + 0.06 * pulse)
        paste_center(canvas, cta_glow, W / 2, 1400, sc, ease_out_cubic(p) * (0.5 + 0.5 * pulse))
        paste_center(canvas, cta, W / 2, 1400, sc, ease_out_cubic(p))
        bob = abs(math.sin((t - 5.1) * math.pi / BEAT)) * 30
        paste_center(canvas, arrow, W / 2, 1570 + bob, 1, ease_out_cubic(prog(t, 5.4, 0.3)))

    sweep(canvas, t)
    # fundido final corto
    fo = prog(t, DUR - 0.25, 0.25)
    if fo > 0:
        canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(140 * fo))))
    return canvas.convert("RGB")


# ---------------------------------------------------------------- música (beat urbano sintetizado)
SR = 44100


def synth_beat(dur):
    n = int(SR * dur)
    out = np.zeros(n, np.float32)
    rng = np.random.default_rng(7)
    step = BEAT / 4  # semicorcheas

    def add(sig, at):
        i = int(at * SR)
        if i >= n:
            return
        j = min(n, i + len(sig))
        out[i:j] += sig[: j - i]

    def kick():
        tt = np.arange(int(0.45 * SR)) / SR
        f = 45 + 120 * np.exp(-tt * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 6) * 0.9

    def b808(freq, length):
        tt = np.arange(int(length * SR)) / SR
        f = freq * (1 + 0.6 * np.exp(-tt * 40))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return np.tanh(s * 2.2) * np.exp(-tt * 1.6) * 0.45

    def snare():
        tt = np.arange(int(0.25 * SR)) / SR
        noise = rng.standard_normal(len(tt)).astype(np.float32)
        noise = np.diff(noise, prepend=0)  # paso alto simple
        return (noise * 0.35 + np.sin(2 * np.pi * 190 * tt) * 0.4) * np.exp(-tt * 18)

    def hat(open_=False):
        tt = np.arange(int((0.12 if open_ else 0.04) * SR)) / SR
        noise = np.diff(rng.standard_normal(len(tt) + 1)).astype(np.float32)
        return noise * np.exp(-tt * (25 if open_ else 90)) * 0.12

    def pad_chord(freqs, length):
        tt = np.arange(int(length * SR)) / SR
        s = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.001 * tt) for f in freqs)
        env = np.minimum(1, tt / 0.3) * np.minimum(1, (length - tt) / 0.4)
        return s * env * 0.05

    # riser + impacto en la transición
    tt = np.arange(int(0.6 * SR)) / SR
    riser = rng.standard_normal(len(tt)).astype(np.float32) * (tt / 0.6) ** 2 * 0.25
    add(riser[::-1] * 0.6, 0.0)
    add(kick() * 1.2, 0.0)

    bars = int(dur / (BEAT * 4)) + 1
    roots = [55.0, 55.0, 43.65, 49.0]  # A1, A1, F1, G1
    chords = [(220, 261.6, 329.6), (220, 261.6, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7)]
    t0 = 0.6
    for b in range(bars):
        bt = t0 + b * BEAT * 4
        add(pad_chord(chords[b % 4], BEAT * 4), bt)
        for s16 in range(16):
            at = bt + s16 * step
            if s16 in (0, 10):
                add(kick(), at)
                add(b808(roots[b % 4], BEAT * 1.8), at)
            if s16 in (4, 12):
                add(snare(), at)
            if s16 % 2 == 0 or (b % 2 == 1 and s16 in (13, 15)):
                add(hat(open_=(s16 == 14)), at)
    # fade out
    fl = int(0.5 * SR)
    out[-fl:] *= np.linspace(1, 0, fl)
    out = np.tanh(out * 1.3) * 0.85
    return out


def write_wav(path, sig):
    stereo = np.stack([sig, sig], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- render
def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav = TMP / "beat.wav"
    write_wav(wav, synth_beat(DUR))
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav),
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(OUT)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(DUR * FPS)
    for i in range(total):
        proc.stdin.write(frame(i / FPS).tobytes())
        if i % 30 == 0:
            print(f"  fotograma {i}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("Listo:", OUT)


if __name__ == "__main__":
    main()
