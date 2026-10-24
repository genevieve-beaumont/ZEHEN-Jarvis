# Security and privacy

ZEHEN watches your camera, listens for one word, and controls your mouse, keyboard and PowerShell, so it has to
be trustworthy. This page says exactly what it does.

## What ZEHEN does with your data

- **Camera video stays in memory.** Each frame is analysed and dropped. Nothing is shown, recorded, saved or
  uploaded.
- **The microphone is processed on your PC.** The wake word ("Zehen") is detected locally with Vosk. Audio is
  used only after you say it. It leaves the PC only if you added a Groq key, in which case that clip goes to
  Groq for transcription.
- **Requests go where your key points.** With a cloud key, your request, your installed app names, your open
  window titles and the output of commands ZEHEN ran go to that provider (Groq, Google or OpenRouter). Free
  plans can use data to improve products: read their terms. With no key, the offline model answers and nothing
  leaves the PC.
- **Downloads.** Models are fetched once from their public hosts (Google storage, alphacephei.com, GitHub,
  Hugging Face) into `%USERPROFILE%\.zehen`.
- **Settings** are a small JSON file at `%USERPROFILE%\.zehen.json`: camera number, tutorial status, favourite
  apps, voice options and, if you pasted one, your API key **in plain text**.
- **No telemetry, no accounts, no ads.**

## What Noor can do, and the risk

Noor turns your request into actions and runs them without asking: open apps, type, press shortcuts, click by
name in any app, and run **PowerShell as you**. That is deliberate and it is powerful. A wrong answer from the
model, or text from a web page or window title that manipulates it, can delete files or send messages.

Mitigations in the code, none of them a confirmation prompt:

- The model must answer in a fixed JSON action list. Anything else is dropped, and at most 5 actions run per step.
- A request runs at most 6 steps.
- The wake word only counts at the start of a phrase, and Noor is deaf while she speaks.
- Pausing stops her between steps.

If that is too much power, set `"voice": false` in `.zehen.json`. Hand control does not use the microphone or
any network.

## Staying in control

- The pause button on the panel, or a fist, pauses gestures and stops Noor between steps
- The close button quits
- Touching the real mouse or touchpad makes ZEHEN let go of the cursor
- "Close window" sends a normal close request, so apps still ask to save

## Reporting a vulnerability

If you find a way ZEHEN could leak data or be misused to control a PC, please don't open a public issue.
Contact the maintainer privately through GitHub ([@priyanshusta](https://github.com/priyanshusta)) with steps to
reproduce. You'll get a reply within a week, and credit in the changelog if you'd like.
