# Change Log

## MediaPipe video timestamp fix

Updated `zehen.py` so timestamps passed to MediaPipe's video hand detector are
strictly increasing. Consecutive camera frames can otherwise receive the same
millisecond timestamp after converting the monotonic clock value to an integer.

MediaPipe rejects duplicate or decreasing timestamps with:

`ValueError: Input timestamp must be monotonically increasing.`

The tracker now advances the timestamp by at least one millisecond when needed,
preventing the hand-tracking thread from crashing during normal camera use.