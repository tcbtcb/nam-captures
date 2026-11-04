# 2026-11-01: Hermida Audio Dover Drive

Nine captures: od1 / od2 / dist, each in bal / bri / dark.
Models are in `complete-models/dover-*-a1.nam` and `-a2.nam`.

## Setup

- Same input as the Super AT: NAM's standard sweep plus guitar playing, mono 48 kHz 16-bit.
- Delay: **-10 samples** (NAM's calibration gave -6 or -7 on every file).
- Validation: the sweep's first 9 seconds. Training: 10-180.5s + 190-511s.
- 100 epochs, A1 and A2 (full + lite), Apple silicon (MPS).
- Levels matched to the input on Live's slow (RMS) meter. Even at od1 (gain ~8 o'clock) the Dover squashes harder than the Super AT dimed: crest factor ~9-10 dB vs ~12.
- The od2 and dist exports are 512.0s and the od1 exports 516.9s; the sweep copy is trimmed to match each (NAM needs equal lengths; the first 512s are identical).
- `od1-bri` was exported as `od2-bri` by mistake and renamed.

## Results

ESR on the validation clip (lower is better; NAM calls < 0.01 "Great!", < 0.035 "Not bad!").

| Capture | A1 | A2 full | A2 lite |
|---|---|---|---|
| od1-bal | 0.0030 | 0.0029 | 0.0035 |
| od1-bri | 0.0028 | 0.0029 | 0.0036 |
| od1-dark | 0.0033 | 0.0031 | 0.0038 |
| od2-bal | 0.0042 | 0.0041 | 0.0057 |
| od2-bri | 0.0041 | 0.0040 | 0.0057 |
| od2-dark | 0.0046 | 0.0050 | 0.0061 |
| dist-bal | 0.0123 | 0.0120 | 0.0197 |
| dist-bri | 0.0113 | 0.0114 | 0.0194 |
| dist-dark | 0.0130 | 0.0121 | 0.0218 |

- od1 and od2 are well under 0.01. dist is just over (~0.012): the closer to fuzz, the harder to model. A2 lite loses the most there.
- About 70-75 min per capture (A1 + A2) on a 60W charger.

## Rerun

```
python3 make_config.py dover-<gain>-<tone> ...   # writes config/data-*.json
./run_all.sh [names...]                          # trains (all configs if no names), copies models, scores
```

Needs the audio in `audio/`, which is not in git.
