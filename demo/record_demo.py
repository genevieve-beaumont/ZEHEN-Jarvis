"""Records the ZEHEN demo video on your live desktop: docs/media/zehen-demo.mp4 and .gif.

    python -m pip install imageio-ffmpeg
    python demo/record_demo.py

Everything in it is real: the HUD, guide panel, launcher (your open windows and apps) and writing pad
come from zehen.py; tapping the Notepad tile really opens Notepad; Windows reads the handwriting and
the text is typed with real keystrokes; zoom is a real Ctrl+scroll and the swipe a real Alt+Tab.
Only the hand is scripted (a recorder can't wave for you). It records your whole screen for ~45 s:
don't touch the mouse or keyboard meanwhile.
"""
import ctypes
import math
import random
import subprocess
import sys
import threading
import time
import tkinter as tk
from ctypes import wintypes
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "demo")]
import zehen  # noqa: E402  (also makes the process DPI-aware, so screen grabs are full resolution)
import cv2  # noqa: E402
import imageio_ffmpeg  # noqa: E402  (pip install imageio-ffmpeg: a bundled ffmpeg)
import numpy as np  # noqa: E402
from letters import word_strokes  # noqa: E402
from PIL import ImageGrab  # noqa: E402

FPS = 30            # animation steps per second (motion itself follows the real clock)
VIDEO_FPS = 15      # recorded frames per second
OUT = ROOT / "docs" / "media"
GIF_WIDTH, GIF_FPS = 640, 8  # README GIF: ~2.5 MB, so it shows up fast on GitHub
POSES = {"point": (0, 1, 0, 0, 0), "palm": (1, 1, 1, 1, 1), "three": (0, 1, 1, 1, 0), "scroll": (0, 1, 1, 0, 0)}
user32 = ctypes.WinDLL("user32")
user32.MoveWindow.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.BOOL]


def hand_at(ptr, gesture, side=1, s=0.16):
    """21 wireframe landmarks (camera-frame fractions) with the index knuckle near the pointer."""
    m = zehen.MARGIN
    kx, ky = m + ptr[0] * (1 - 2 * m), m + ptr[1] * (1 - 2 * m)
    cx, cy = kx + 0.3 * s * side, ky - 0.15 * s
    up = POSES.get(gesture, POSES["point"])
    P = lambda dx, dy: (cx + dx * s * side, cy + dy * s)
    thumb_tip = P(-0.45, -0.12) if gesture == "pinch" else P(-0.85, 0.05) if up[0] else P(-0.2, 0.35)
    pts = [P(0, 1), P(-0.35, 0.75), P(-0.6, 0.5), P(-0.75, 0.28), thumb_tip]
    for i, (dx, dy, length) in enumerate(((-0.3, 0.15, 1), (-0.1, 0.12, 1.08), (0.1, 0.15, 1), (0.28, 0.22, 0.8))):
        mx, my = dx, dy
        if i == 0 and gesture == "pinch":  # index bends down to meet the thumb
            joints = [(mx - 0.05, my - 0.3), (-0.42, -0.28), (thumb_tip[0], thumb_tip[1])]
            pts += [P(mx, my), P(*joints[0]), P(*joints[1]), joints[2]]
        elif up[i + 1]:
            pts += [P(mx, my - k * length) for k in (0, 0.35, 0.6, 0.8)]
        else:
            pts += [P(mx, my), P(mx, my - 0.25), P(mx + 0.03, my - 0.1), P(mx + 0.02, my + 0.05)]
    return pts


class Recorder:
    """Grabs the screen on a thread at a steady VIDEO_FPS (repeats a frame if a grab runs late) and streams
    it into ffmpeg as H.264. OpenCV's own encoder ignores quality settings and writes ~12 Mbit/s."""

    def __init__(self, path, region, width=1280):
        self.region = region
        h = round(width * (region[3] - region[1]) / (region[2] - region[0]) / 2) * 2
        self.size = (width, h)
        self.ffmpeg = subprocess.Popen(
            [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
             "-s", f"{width}x{h}", "-r", str(VIDEO_FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        start, written = time.monotonic(), 0
        while self.running:
            frame = cv2.cvtColor(np.asarray(ImageGrab.grab(bbox=self.region)), cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
            due = int((time.monotonic() - start) * VIDEO_FPS) + 1
            while written < due:
                self.ffmpeg.stdin.write(frame.tobytes())
                written += 1

    def stop(self):
        self.running = False
        self.thread.join()
        self.ffmpeg.stdin.close()
        self.ffmpeg.wait()


def make_gif(mp4, gif):
    """One shared palette tuned to the cyan HUD; only changed rectangles are stored per frame."""
    vf = (f"fps={GIF_FPS},scale={GIF_WIDTH}:-1:flags=lanczos,split[a][b];"
          "[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle")
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(mp4), "-vf", vf,
                    str(gif)], check=True)




def card(root, W, H, lines):
    """A centred title card floating over the live desktop."""
    win = tk.Toplevel(root, bg=zehen.BG, highlightthickness=2, highlightbackground=zehen.CYAN)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    for text, size, color in lines:
        tk.Label(win, text=text, bg=zehen.BG, fg=color, font=("Segoe UI", size, "bold" if size > 30 else "normal"),
                 padx=60).pack(pady=(6, 6))
    win.update_idletasks()
    win.geometry(f"+{(W - win.winfo_width()) // 2}+{(H - win.winfo_height()) // 2 - 60}")
    return win


def notepad_window():
    for h, title in zehen.list_windows():
        if zehen.window_text(h, "GetClassNameW") == "Notepad":
            return h
    return None


def main():
    OUT.mkdir(exist_ok=True)
    W, H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    root = tk.Tk()
    t = zehen.Tracker(None, {"apps": ["Notepad", "Google Chrome", "Microsoft Edge", "File Explorer",
                                      "WhatsApp", "Settings", "Calculator"]}, start=False)
    t.apps = zehen.installed_apps()  # your real Start menu
    hud = zehen.HUD(root, t, {"tutorial_done": True})
    real_type = t._type
    notepad = {}

    def safe_type(text):  # real keystrokes, but only ever into Notepad
        h = notepad.get("hwnd")
        if h and int(zehen.u32.GetForegroundWindow() or 0) == int(h):
            real_type(text)
        else:
            t.chunks.append(text)
    t._type = safe_type

    def focus_notepad():
        if notepad.get("hwnd"):
            zehen.focus_window(notepad["hwnd"])

    def put(ptr=None, g=None, active=None, progress=0.0, hands=None, ptr2=None, zoom=False, flash="", pressed=None):
        if ptr:  # a real hand is never perfectly still
            now = time.monotonic()
            ptr = (ptr[0] + 0.0018 * math.sin(now * 11.3) + 0.0012 * math.sin(now * 17.9),
                   ptr[1] + 0.0018 * math.sin(now * 13.7 + 1) + 0.0012 * math.sin(now * 7.1))
            if not t.mode and not zoom and g in ("point", "pinch"):  # like ZEHEN: the real cursor follows
                zehen.pyautogui.moveTo(int(ptr[0] * W), int(ptr[1] * H))
        if hands is None:
            hands = [hand_at(ptr, g)] if ptr else []
        t.ui = t._layout()
        hover = next((b.id for b in t.ui.buttons if ptr and zehen.inside(b.r, *ptr)), None) if t.mode else None
        with t.lock:
            ink = [list(s) for s in t.ink]
        t.state = SimpleNamespace(hands=hands, gesture=g, active=active or g, since=0.0, ptr=ptr, ptr2=ptr2,
                                  progress=progress, zoom=zoom, mode=t.mode, ui=t.ui, hover=hover, pressed=pressed,
                                  ink=ink, flash=flash)

    ease = lambda x: x * x * (3 - 2 * x)

    def timed(secs):
        """Progress 0..1 on the real clock, one value per animation step: the video keeps true speed
        even when screen capture makes the steps run late."""
        start = time.monotonic()
        while True:
            p = min((time.monotonic() - start) / secs, 1.0)
            yield p
            if p >= 1:
                return

    def hold(secs, **kw):
        for _ in timed(secs):
            put(**kw)
            yield

    def glide(a, b, secs, **kw):
        bend = random.uniform(-0.12, 0.12)  # arms move in arcs, not rulers
        for p in timed(secs):
            e = ease(p)
            arc = math.sin(math.pi * e) * bend
            put(ptr=(a[0] + (b[0] - a[0]) * e + (b[1] - a[1]) * arc, a[1] + (b[1] - a[1]) * e - (b[0] - a[0]) * arc),
                **kw)
            yield

    def pose_hold(gesture, at, secs=1.2):
        for p in timed(secs):
            put(ptr=at, g=gesture, progress=min(p * secs / zehen.HOLD_S, 1.0))
            yield

    def find(label, section):
        return next(b for b in t._layout().buttons if label in b.label and b.id.startswith(section))

    def tile(label, section=""):
        r = find(label, section).r
        return ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)

    def tap(label, at, section=""):
        b = find(label, section)
        yield from hold(0.15, ptr=at, g="pinch")
        b.action()  # the real launcher / pad action
        yield from hold(0.35, ptr=at, g="pinch", pressed=b.id)
        yield from hold(0.25, ptr=at, g="point")

    def wait_foreground(match, secs=4.0, at=(0.5, 0.5)):
        for _ in timed(secs):
            put(ptr=at, g="point")
            yield
            h = int(zehen.u32.GetForegroundWindow() or 0)
            if h and match(zehen.window_text(h), zehen.window_text(h, "GetClassNameW")):
                return

    def write(word, at):
        """Draw the word with a pinch, pause, let Windows read it, and type the result."""
        size = 0.15 * H
        strokes = [[(x / W, y / H) for x, y in s] for s in word_strokes(word, at[0] * W, 0.5 * H - size, size)]
        pos = at
        for s in strokes:
            yield from glide(pos, s[0], 0.25, g="point")
            with t.lock:
                t.ink.append([s[0]])
            for p in timed(len(s) / 40):  # pen speed: ~40 points per second
                k = max(1, int(p * (len(s) - 1)))
                with t.lock:
                    t.ink[-1] = s[:k + 1]
                put(ptr=s[k], g="pinch")
                yield
            with t.lock:
                t.ink[-1] = s
            pos = s[-1]
        yield from hold(0.6, ptr=pos, g="point")
        t.recognizing, got = True, []
        threading.Thread(target=lambda: got.append(zehen.recognize(strokes, *zehen.pyautogui.size())),
                         daemon=True).start()
        while not got:
            put(ptr=pos, g="point")
            yield
        focus_notepad()
        t._got_text(got[0])
        with t.lock:
            t.ink = []
        t.recognizing = False
        yield from hold(1.2, ptr=pos, g="point")

    def script():
        random.seed(7)
        hud.panel.withdraw()
        intro = card(root, W, H, [("◉ ZEHEN", 64, zehen.CYAN), ("Control your PC with your hands", 24, zehen.TEXT),
                                  ("laptop camera · no extra hardware · runs offline", 13, zehen.DIM)])
        yield from hold(2.5)
        intro.destroy()
        hud.panel.deiconify()
        yield from hold(0.4)
        yield from glide((0.58, 0.72), (0.42, 0.38), 1.3, g="point")             # hand comes up, cursor follows
        yield from glide((0.42, 0.38), (0.6, 0.5), 0.9, g="point")

        # 1. open Notepad from the launcher
        yield from pose_hold("palm", (0.6, 0.5))
        t.set_mode("launcher")
        t.windows.sort(key=lambda w: "YouTube" not in w[1])
        yield from hold(0.5, ptr=(0.6, 0.5), g="point")
        yield from glide((0.6, 0.5), tile("Google Chrome", "APPS"), 0.8, g="point")
        yield from glide(tile("Google Chrome", "APPS"), tile("Notepad", "APPS"), 0.6, g="point")
        yield from tap("Notepad", tile("Notepad", "APPS"), "APPS")             # really opens Notepad
        yield from wait_foreground(lambda title, cls: cls == "Notepad", at=(0.3, 0.35))
        notepad["hwnd"] = notepad_window()
        if notepad["hwnd"]:
            zehen.u32.ShowWindow(notepad["hwnd"], 9)  # restore, then sit below the writing pad
            user32.MoveWindow(notepad["hwnd"], int(0.24 * W), int(0.705 * H), int(0.52 * W), int(0.24 * H), True)
            focus_notepad()
            zehen.pyautogui.hotkey("ctrl", "n")  # a fresh tab, so nothing of yours gets typed over
        yield from hold(0.8, ptr=(0.3, 0.35), g="point")

        # 2. write "Hey" in the air
        yield from glide((0.3, 0.35), (0.5, 0.42), 0.6, g="point")
        yield from pose_hold("three", (0.5, 0.42))
        t.set_mode("pad")
        yield from hold(0.4, ptr=(0.5, 0.42), g="point")
        yield from write("Hey", (0.4, 0.4))
        yield from pose_hold("palm", (0.5, 0.42))                              # palm closes the pad
        t.set_mode(None)
        yield from hold(0.3, ptr=(0.5, 0.42), g="point")

        # 3. jump to Edge (YouTube) from the launcher
        yield from pose_hold("palm", (0.5, 0.42))
        t.set_mode("launcher")
        t.windows.sort(key=lambda w: "YouTube" not in w[1])
        yield from hold(0.4, ptr=(0.5, 0.42), g="point")
        yt = tile("YouTube", "OPEN") if any("YouTube" in w[1] for w in t.windows) else tile("Edge", "APPS")
        yield from glide((0.5, 0.42), yt, 0.8, g="point")
        yield from tap("YouTube" if any("YouTube" in w[1] for w in t.windows) else "Edge", yt,
                       "OPEN" if any("YouTube" in w[1] for w in t.windows) else "APPS")
        yield from wait_foreground(lambda title, cls: "Edge" in title or "YouTube" in title, at=yt)
        yield from glide(yt, (0.45, 0.4), 0.7, g="point")                       # browse: hover a few videos
        yield from glide((0.45, 0.4), (0.62, 0.48), 0.8, g="point")

        # 4. two fingers: scroll YouTube down, then back up
        for p in timed(2.2):
            y = 0.5 + 0.08 * ease(min(p * 3, 1.0))      # lower the V = scroll down
            zehen.pyautogui.scroll(-90)
            put(ptr=(0.62, y), g="scroll", hands=[hand_at((0.62, y), "scroll")])
            yield
        for p in timed(1.4):
            y = 0.58 - 0.16 * ease(min(p * 3, 1.0))     # raise it = scroll up
            zehen.pyautogui.scroll(120)
            put(ptr=(0.62, y), g="scroll", hands=[hand_at((0.62, y), "scroll")])
            yield
        yield from hold(0.4, ptr=(0.62, 0.42), g="point")

        # 5. both hands: stretch to zoom the page in, squeeze to zoom back out
        zehen.pyautogui.moveTo(int(0.5 * W), int(0.5 * H))
        for zoom_in in (True, False):
            done = 0
            for p in timed(1.6):
                e = ease(p) if zoom_in else 1 - ease(p)
                spread = 0.07 + 0.15 * e
                right, left = (0.5 + spread, 0.55), (0.5 - spread, 0.55)
                if done < int(p * 3):
                    zehen.ctrl_scroll(1 if zoom_in else -1)  # real Ctrl+wheel
                    done += 1
                put(ptr=right, ptr2=left, g="pinch", active="zoom", zoom=True,
                    hands=[hand_at(right, "pinch"), hand_at(left, "pinch", side=-1)])
                yield
            yield from hold(0.3, ptr=(0.57, 0.55), g="point")

        # 6. other hand swipes: back to Notepad
        switched = False
        for p in timed(1.6):
            left = (0.12 + 0.32 * ease(min(p * 2, 1.0)), 0.5)
            if p > 0.5 and not switched:
                zehen.pyautogui.hotkey("alt", "tab")
                switched = True
            put(ptr=(0.64, 0.55), ptr2=left, g="point", active="swipe", flash="⇄  SWITCH APP" if p > 0.5 else "",
                hands=[hand_at((0.64, 0.55), "point"), hand_at(left, "palm", side=-1)])
            yield
        yield from hold(1.2, ptr=(0.64, 0.55), g="point")
        hud.panel.withdraw()
        put()
        outro = card(root, W, H, [("◉ ZEHEN", 64, zehen.CYAN), ("github.com/priyanshusta/ZEHEN", 24, zehen.TEXT),
                                  ("open source · MIT · real app, scripted hand", 13, zehen.DIM)])
        yield from hold(3.0)
        outro.destroy()

    zehen.pyautogui.moveTo(W // 2, H // 3)  # off the taskbar: no window previews popping up
    zehen.pyautogui.hotkey("win", "m")      # minimize everything: a clean desktop that stays clean
                                            # (Win+D brings windows back as soon as a new one appears)
    time.sleep(3.0)                         # let the minimize animations finish before recording
    recorder = Recorder(OUT / "zehen-demo.mp4", (0, 0, W, H))
    steps = script()

    def step():
        try:
            next(steps)
            root.after(int(1000 / FPS), step)
        except StopIteration:
            recorder.stop()
            root.destroy()

    root.after(500, step)
    root.mainloop()
    zehen.pyautogui.hotkey("win", "shift", "m")  # give you your windows back
    make_gif(OUT / "zehen-demo.mp4", OUT / "zehen-demo.gif")
    for f in ("zehen-demo.mp4", "zehen-demo.gif"):
        print(f, f"{(OUT / f).stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
