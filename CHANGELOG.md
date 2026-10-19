# Changelog

All notable changes to ZEHEN. Format: [Keep a Changelog](https://keepachangelog.com), versions: [SemVer](https://semver.org).

## [0.1.0] · 2026-10-19 · "Mark I"

First release: control Windows with your hands through the laptop camera.

### Added
- Hand tracking with MediaPipe, camera hidden, see-through HUD overlay with a glowing cursor ring
- Gestures: move, click, double-pinch to open, drag, right-click, scroll, pause
- Two hands: stretch to zoom, swipe the other hand to switch apps
- Launcher (hold an open palm): open windows, favourite apps, search all apps, system controls
- Writing pad (hold three fingers): air-writing typed through Windows' offline handwriting recognition,
  with "did you mean" suggestions, ⌫, ⌫ word, space, enter
- On-screen keyboard
- Guide panel with live wireframe hands and a step-by-step tutorial
- Camera permission screen with help when the camera is blocked
- `ZEHEN.bat` launcher that finds Python without PATH and installs libraries on first run
- `python zehen.py --test` self-test
- Demo video recorded and edited with WinScreen Studio, plus `demo/record_demo.py` to re-record it
- Project website (`docs/index.html`), MIT license, roadmap, contributing guide, templates

### Fixed during development
- Picks the real webcam instead of virtual cameras (PRISM Lens, OBS) that send a black placeholder
- Camera opens in about 1 second instead of 23 (Media Foundation hardware transforms off)
- Handwriting recognition no longer freezes: results are polled instead of awaited
- Touching the real mouse near a screen corner no longer stops the app; ZEHEN yields the cursor instead
- Double-pinch lands as a real double-click, even though hand clicks drift a few pixels
- Typing from the writing pad no longer drops letters in apps like Notepad
