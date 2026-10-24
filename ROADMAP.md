# ZEHEN roadmap

> The films showed glowing hands moving windows through the air and an assistant that simply gets things done.
> ZEHEN gets there one real, working step at a time, on the laptop you already own.

Status: **shipped**, **in progress**, **planned**, **research**.

## v0.1 "Mark I": your hand is the mouse (shipped)

- Hidden camera, see-through HUD with a glowing cursor ring
- Move, click, double-click (open), drag, right-click, scroll
- Two hands: zoom by stretching, swipe to switch apps
- Launcher: open windows, favourite apps, search every installed app, system controls
- Air-writing pad: write with a pinch, Windows' offline handwriting recognition types it
- On-screen keyboard, guided tutorial, wireframe hand preview
- Finds the real camera automatically, skipping virtual ones; yields to the real mouse

## v0.2 "Noor": talk to it (shipped, being hardened)

- Wake word "Zehen" and an assistant named Noor, with a natural offline female voice
- Plans and runs actions, reads the results and continues: apps, windows, links, typing, shortcuts, PowerShell
- Clicks and types inside any app by name through Windows UI Automation
- Free cloud brain (Groq, Gemini, OpenRouter) or a free offline brain (Qwen3 1.7B)
- Glass panel that starts as a small pill and opens when you point at it

Next for voice:

- **In progress.** Better wake word: a trained "Zehen" model instead of the "zane" sound-alike
- **Planned.** Dictation mode: speak while the writing pad is open
- **Planned.** Point and speak: point at a window and say "maximize" or "send it to the left screen"
- **Planned.** Hindi and other languages for speech and replies
- **Planned.** Lower memory: load Noor's voice only when she speaks
- **Planned.** Vision for unlabeled icons and images, using a small local model

## v0.3 "Mark II": feel it (planned)

Make every gesture feel instant and certain.

- **Per-person calibration**: a 20-second wizard that learns your hand size, reach and pinch
- **Custom gestures**: record a pose once, bind it to any shortcut ("rock sign, screenshot")
- **Sound feedback**: soft clicks and whooshes so you hear what you did
- **Settings panel inside the HUD**: tune sensitivity with your hand, no JSON editing
- **Multi-monitor**: point at a screen, the cursor jumps there
- **Standalone installer**: one `ZEHEN-Setup.exe`, starts with Windows

## v0.4 "Holo-table": grab the interface (research)

Windows stop being flat rectangles.

- **Grab and throw windows**: pinch a window, fling it to another screen with momentum
- **Two-hand rotate and scale** for photos, maps and 3D models
- **Depth from one camera**: push forward to press, pull back to release
- **Radial command ring**: open palm brings up a circle of actions around your hand
- **Workspace layouts**: frame a rectangle with both hands to snap windows into it

## v1.0 "Stark": beyond the screen (research)

- **AR glasses and headsets**: the same gestures on a floating holographic desktop
- **Eye and hand**: look at a target, pinch to act on it, even across a big room
- **Smart home**: point at a lamp, pinch to switch it on
- **Gesture macros**: chain apps, keys and voice into one move
- **macOS and Linux** builds
- **Plugin API** so anyone can add gestures, actions and HUD widgets

## Ideas board

Not scheduled yet, all welcome: sign-language letters for typing, presenter mode for slides, game controller
mode, accessibility profiles for limited mobility, a "focus" gesture that hides every window except one.

Have an idea from a film you love? [Open a feature request](../../issues/new?template=feature_request.md).
