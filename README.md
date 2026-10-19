# ◉ ZEHEN

Control your Windows PC with your hands, using just your laptop camera. Move the cursor, click, drag,
scroll, zoom, switch apps, launch anything, and write in the air to type.

The camera runs hidden in the background. A see-through overlay shows a glowing cursor ring, and a small
guide panel in the top-right corner shows your tracked hand and the gesture you're making.

## Run it

Needs Windows 10/11 and Python 3.10+ ([python.org](https://www.python.org/downloads/)).

**Double-click `ZEHEN.bat`.** It finds Python even if it isn't on your PATH, installs the libraries on
first run, and starts ZEHEN without a console window.

Or from a terminal:

```bash
python -m pip install -r requirements.txt
python zehen.py
```

The first time, ZEHEN asks for camera permission and walks you through every gesture with a short
tutorial. Replay it any time with **tutorial ↻** on the panel.

## Gestures

| Gesture | Does |
|---|---|
| ☝ Index finger up | Move the cursor |
| 🤏 Pinch thumb + index | Click. Hold and move to drag. Two quick pinches = double-click |
| 👌 Index up, thumb to middle finger | Right-click |
| ✌ Two fingers up | Scroll: raise your hand to go up, lower it to go down |
| 🖐 Open palm, hold | Launcher. Hold again to close any panel |
| ✍ Three fingers up, hold | Writing pad |
| 🙌 Both hands pinch, then spread or close | Zoom in / out |
| 👋 Swipe your other hand sideways | Switch to your last app |
| ✊ Fist | Pause |

Your right hand drives the cursor and your left hand gives commands. With one hand up, either hand works.
Touch the real mouse or touchpad and ZEHEN lets go of the cursor for a moment.

## Launcher

Point at a tile and pinch to tap it.

- **Open windows**: jump to any window.
- **Apps**: your favourites, plus **Search all apps**: write an app's name in the air, then tap the match.
- **Controls**: keyboard, writing pad, files, desktop, task view, screenshot, maximize, minimize,
  close window, volume, play/pause.

## Writing pad

Pinch and write in the box. Pause for a second and Windows' built-in handwriting recognition turns the
ink into text and types it into the app you were using. It works offline and nothing leaves your PC.
Buttons: **⌫** (letter), **⌫ word**, **space**, **enter**, **clear ink**, **close**. If a word comes out
wrong, tap one of the "did you mean" chips.

## Settings

`%USERPROFILE%\.zehen.json`

| Key | Example | Meaning |
|---|---|---|
| `main_hand` | `"Left"` | Which hand drives the cursor (default `"Right"`) |
| `apps` | `["Spotify", "Notepad"]` | Favourite apps in the launcher, by Start menu name |
| `camera` | `1` | Camera ZEHEN found last time (it finds it again if this one stops working) |
| `tutorial_done` | `false` | Show the tutorial again on next start |

Feel tuning (smoothing, pinch sensitivity, hold time, scroll speed and so on) lives in the knobs at the
top of `zehen.py`.

## Troubleshooting

- **"Can't reach the camera"**: close other apps using it, and turn on Windows Settings › Privacy &
  security › Camera › *Let desktop apps access your camera*. Some laptops also have a shutter or F-key.
- **Virtual cameras** (PRISM Lens, OBS) are skipped automatically, since they only send a placeholder
  image. ZEHEN picks the first camera with a live picture.
- **Cursor too shaky or laggy**: lower `MIN_CUTOFF` for steadier, raise `BETA` for snappier.

## Privacy

The video is never shown, recorded, saved or sent anywhere. Hand tracking (MediaPipe) and handwriting
recognition (Windows) both run entirely on your computer.

## Check it

```bash
python zehen.py --test
```

Checks gesture detection, smoothing, app search, panel layouts, real handwriting recognition and the
hand model.

## Files

| File | What |
|---|---|
| `ZEHEN.bat` | Double-click launcher |
| `zehen.py` | The whole app |
| `hand_landmarker.task` | MediaPipe hand model (downloaded automatically if missing) |
| `zehen.ico` | App icon |
| `build.bat` | Optional: builds a standalone `dist\ZEHEN.exe` (needs ~1 GB free disk while building) |
