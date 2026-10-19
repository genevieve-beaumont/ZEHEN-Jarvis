# Contributing to ZEHEN

Thanks for wanting to help build the interface from the movies. Every gesture idea, bug report and
pull request makes ZEHEN better.

## Ways to help

- 🐛 **Report a bug**: [open an issue](../../issues/new?template=bug_report.md). Say what you did, what
  happened, and paste the output of `python zehen.py --test`.
- 💡 **Suggest a feature**: [feature request](../../issues/new?template=feature_request.md). Movie
  references welcome. Check the [roadmap](ROADMAP.md) first.
- 🧪 **Test on your hardware**: different cameras, lighting and screens find the best bugs.
- 🛠️ **Send code**: pick something from the roadmap or an issue labelled `good first issue`.

## Set up

```bash
git clone https://github.com/priyanshusta/ZEHEN.git
cd ZEHEN
python -m pip install -r requirements.txt
python zehen.py --test
python zehen.py
```

## How the code is laid out

Everything lives in `zehen.py`, top to bottom:

| Part | What it does |
|---|---|
| Tuning knobs | Every sensitivity value, with a comment saying which way to turn it |
| `classify()` | Turns 21 hand landmarks into a gesture name |
| `OneEuro` | Cursor smoothing: steady when still, fast when moving |
| Windows helpers | Open windows, installed apps, handwriting recognition |
| `Tracker` | Camera loop on a background thread: gestures → actions; builds panel layouts |
| `HUD` | Tk overlay and guide panel; draws whatever `Tracker.state` says |
| Camera setup | Permission screen, finding a live camera |
| `selftest()` | Checks you can run without a camera |

The tracker never touches the UI directly: it publishes a snapshot (`self.state`) every frame and
the HUD draws it. Keep it that way, and keep new feel-related numbers in the tuning knobs.

## Pull requests

1. Keep each PR to one change, and say in the description how it feels to use.
2. Run `python zehen.py --test` and try the gesture for real with your hand.
3. Add a check to `selftest()` when you add logic that can break.
4. Match the existing style: plain names, short functions, comments that explain *why*.
5. Add a line to [CHANGELOG.md](CHANGELOG.md).

## Code of conduct

Be kind. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
