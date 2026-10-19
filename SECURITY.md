# Security and privacy

ZEHEN watches your camera and controls your mouse and keyboard, so it has to be trustworthy.

## What ZEHEN does with your data

- **Camera video stays in memory.** Each frame is analysed and dropped. Nothing is shown, recorded,
  saved or uploaded.
- **Everything runs on your PC.** Hand tracking (MediaPipe) and handwriting recognition (Windows) work
  offline. The only network request is a one-time download of the hand model if it's missing.
- **Settings** are a small JSON file at `%USERPROFILE%\.zehen.json`: camera number, tutorial status,
  favourite apps. No personal data.
- **No telemetry, no accounts, no ads.**

## Staying in control

- ⏸ on the panel pauses tracking; ✕ quits
- A fist pauses gestures
- Touching the real mouse or touchpad makes ZEHEN let go of the cursor
- "Close window" sends a normal close request, so apps still ask to save

## Reporting a vulnerability

If you find a way ZEHEN could leak data or be misused to control a PC, please don't open a public
issue. Contact the maintainer privately through GitHub ([@priyanshusta](https://github.com/priyanshusta))
with steps to reproduce. You'll get a reply within a week, and credit in the changelog if you'd like.
