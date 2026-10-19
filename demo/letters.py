"""Handwritten letter strokes for the scripted demo. Units: x-height box, baseline y=1, x-height top y=0.5,
ascender top y=0. Each letter: (width, [stroke, ...]), stroke = [(x, y), ...]."""
import math


def arc(cx, cy, r, a0, a1, n=16, ry=None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy - ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def line(x0, y0, x1, y1, n=8):
    return [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]


LETTERS = {
    " ": (0.48, []),  # word gap: wide enough that the recognizer splits words
    "h": (0.6, [line(0.05, 0, 0.05, 1) + line(0.05, 1, 0.05, 0.72, 3)[1:] + arc(0.27, 0.72, 0.22, 180, 0, 10)[1:]
                + line(0.49, 0.72, 0.49, 1, 4)[1:]]),
    "e": (0.55, [line(0.05, 0.76, 0.47, 0.76, 6) + arc(0.26, 0.76, 0.21, 0, 300, 20, ry=0.24)[1:]]),
    "l": (0.25, [line(0.08, 0, 0.08, 1, 10)]),
    "o": (0.55, [arc(0.26, 0.75, 0.22, 90, 450, 24, ry=0.25)]),
    "w": (0.8, [line(0.02, 0.5, 0.17, 1, 5) + line(0.17, 1, 0.37, 0.55, 5)[1:] + line(0.37, 0.55, 0.57, 1, 5)[1:]
                + line(0.57, 1, 0.74, 0.5, 5)[1:]]),
    "r": (0.42, [line(0.05, 0.5, 0.05, 1, 6) + line(0.05, 1, 0.05, 0.75, 3)[1:] + arc(0.25, 0.72, 0.2, 180, 60, 8)[1:]]),
    "d": (0.6, [arc(0.26, 0.75, 0.22, 20, 340, 22, ry=0.25), line(0.48, 0, 0.48, 1, 10)]),
    "a": (0.55, [arc(0.25, 0.75, 0.21, 40, 330, 20, ry=0.24), line(0.46, 0.5, 0.46, 1, 6)]),
    "n": (0.55, [line(0.05, 0.5, 0.05, 1, 6) + line(0.05, 1, 0.05, 0.72, 3)[1:] + arc(0.26, 0.72, 0.21, 180, 0, 10)[1:]
                 + line(0.47, 0.72, 0.47, 1, 4)[1:]]),
    "m": (0.85, [line(0.05, 0.5, 0.05, 1, 6) + line(0.05, 1, 0.05, 0.72, 3)[1:] + arc(0.22, 0.72, 0.17, 180, 0, 8)[1:]
                 + line(0.39, 0.72, 0.39, 1, 4)[1:] + line(0.39, 1, 0.39, 0.72, 3)[1:]
                 + arc(0.56, 0.72, 0.17, 180, 0, 8)[1:] + line(0.73, 0.72, 0.73, 1, 4)[1:]]),
    "k": (0.5, [line(0.05, 0, 0.05, 1, 10), line(0.42, 0.5, 0.07, 0.78, 5) + line(0.07, 0.78, 0.45, 1, 5)[1:]]),
    "H": (0.65, [line(0.05, 0, 0.05, 1, 10), line(0.55, 0, 0.55, 1, 10), line(0.05, 0.5, 0.55, 0.5, 6)]),
    "y": (0.55, [line(0.03, 0.5, 0.26, 0.97, 6), line(0.5, 0.5, 0.08, 1.45, 10)]),
    "s": (0.45, [arc(0.24, 0.625, 0.18, 30, 270, 12, ry=0.125) + arc(0.24, 0.875, 0.18, 90, -150, 12, ry=0.125)[1:]]),
}


def word_strokes(word, x, y, size, gap=0.12):
    """Pixel strokes for `word` with its x-height box top-left at (x, y); size = pixels per unit."""
    strokes = []
    for ch in word:
        w, parts = LETTERS[ch]
        strokes += [[(x + px * size, y + py * size) for px, py in s] for s in parts]
        x += (w + gap) * size
    return strokes
