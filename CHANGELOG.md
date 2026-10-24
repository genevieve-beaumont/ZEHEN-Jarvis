# Changelog

All notable changes to ZEHEN. Format: [Keep a Changelog](https://keepachangelog.com), versions: [SemVer](https://semver.org).

## [Unreleased]

### Added
- Voice control: say "Zehen" and ask for anything. An AI model plans, runs actions (including PowerShell),
  reads the output and continues, then answers out loud in a natural female voice (Kokoro, offline). Wake word runs offline (Vosk)
- Free cloud key (Groq, Gemini, OpenRouter) or a small offline model that downloads once; Groq Whisper for
  better speech recognition when the key is Groq's
- Voice chip in the panel with a live orb: listening, thinking, speaking
- Click and type inside any app by name through Windows UI Automation (`ui_list`, `click`), no vision model
- Her name is Noor: she greets you at start-up and replies in a calm, quick style
- The wake word only counts at the start of a phrase, so ordinary talk never wakes her
- She learns how you say "Zehen" (three samples, MFCC and dynamic time warping, fully on the PC): accent-proof
  and far fewer false wakes than a speech model that has never heard the word
- Instant commands with no AI: scroll, click, double and right click, go back, tabs, copy and paste, zoom, volume,
  media, window controls, "type ...", "search ...", "open YouTube", and chains joined by "and" or "then"
- "Click on <name>" works inside any app through UI Automation; "open <site>" knows the common sites
- Conversation: she answers like a person, remembers the last few requests and keeps listening for your reply
- Camera toggle (CAM button, or "turn off the camera") for voice-only use: the camera really stops
- The tutorial is spoken, step by step, then teaches her your voice; first run sets up the offline brain with a
  progress bar and says when it is ready
- Fluid glass pill: a live waveform follows your voice, replies appear as a small caption under it, panel size
  eases instead of snapping, and every panel button now responds to clicks
- Funnier, still professional greetings
- First-run setup checklist: packages, hand model, wake-word ear, voice, hearing and brain, each skipped when
  already on the PC, downloaded with progress when missing, retried next launch if it failed.
  `python zehen.py --setup` runs it from a terminal
- "Play the first video", "play <title>" and "play <anything> on YouTube" click the right video through UI
  Automation (ads skipped), searching YouTube when the title is not on the page
- "Click on the search bar" (or any text box) says "Ready to type" and starts dictation: what you say is typed
  with punctuation until you say "stop typing" or "send"
- Hearing: Whisper on the PC transcribes what you say (accent-tolerant, knows your app and window names, 0.4 s),
  with the wake-word model as a backup transcript; mishearings like "like" for "click" are recovered, one stray
  word is ignored, and the language model is told the request came from speech
- Bring your own AI key (Groq, Gemini, OpenRouter, OpenAI or any OpenAI-compatible service) with a verify step,
  and a clean fall back to the offline brain when a key is missing, rejected or out of free requests
- Switch tabs and windows by name ("switch to the SAM 7 TFPB tab"), live caption of what you said

### Changed
- Side panel is now frosted glass (Windows acrylic blur) and starts as a small pill showing what your hand or voice is doing; point at it to open the full panel, which folds back on its own. The tutorial gains a voice step

## [0.1.0] · 2026-10-19 · "Mark I"

First release: control Windows with your hands through the laptop camera.

### Added
- Hand tracking with MediaPipe, camera hidden, see-through HUD overlay with a glowing cursor ring
- Gestures: move, click, double-pinch to open, drag, right-click, scroll, pause
- Two hands: stretch to zoom, swipe the other hand to switch apps
- Launcher (hold an open palm): open windows, favourite apps, search all apps, system controls
- Writing pad (hold three fingers): air-writing typed through Windows' offline handwriting recognition,
  with "did you mean" suggestions, ⌫, ⌫ word, space, enter
- Writing pad cleans each stroke as the pen lifts: the pen follows the pinched fingertips, tremor is
  smoothed, pinch hooks are trimmed, near-straight lines snap straight and loops snap round
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
