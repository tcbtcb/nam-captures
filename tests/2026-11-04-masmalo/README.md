# 2026-11-04: Fulltone Mas Malo

Fifteen captures: edge / od1 / od2 / fuzz in bal and bri (the pedal is dark overall, so no `dark`),
two alternate edge settings (`-2`), and five with a booster in front (`-boost-may`: Brian May / KAT,
`-boost-buxom`: Friedman Buxom Boost).
Models are in `complete-models/masmalo-*-a1.nam` and `-a2.nam`.

## Setup

- Same input as the other pedals: NAM's standard sweep plus guitar playing, mono 48 kHz 16-bit.
  Exports are 511.0s (the second batch was exported longer and trimmed to 511s; the extra was silence).
- Delay: **-10 samples**. NAM's calibration gave -6 to -8 on most files; a few gave odd values
  (-1, -3, -395) because this pedal is noisy (about -53 dBFS, vs about -64 for the others). The actual click
  onset is about -6 in every file.
- Validation: the sweep's first 9 seconds. Training: 10-180.5s + 190-510.5s.
- 100 epochs, A1 and A2 (full + lite), Apple silicon (MPS).
- Ten captures trained on the M1 Pro laptop, the five booster captures on the M4 Pro Mac mini.
  The mini's models re-score identically on the laptop.
- `edge-bri` was recorded about 5 dB below the input level, so that model plays a bit quieter.

## Results

ESR on the validation clip (lower is better; NAM calls < 0.01 "Great!").

| Capture | A1 | A2 full | A2 lite |
|---|---|---|---|
| edge-bal | 0.0049 | 0.0049 | 0.0049 |
| edge-bal-2 | 0.0055 | 0.0055 | 0.0058 |
| edge-bri | 0.0049 | 0.0050 | 0.0053 |
| edge-bri-2 | 0.0061 | 0.0060 | 0.0067 |
| od1-bal | 0.0013 | 0.0013 | 0.0016 |
| od1-bri | 0.0013 | 0.0013 | 0.0018 |
| od2-bal | 0.0016 | 0.0015 | 0.0023 |
| od2-bri | 0.0018 | 0.0018 | 0.0031 |
| fuzz-bal | 0.0022 | 0.0021 | 0.0043 |
| fuzz-bri | 0.0026 | 0.0027 | 0.0053 |
| od1-bri-boost-may | 0.0030 | 0.0032 | 0.0050 |
| od2-bri-boost-may | 0.0022 | 0.0022 | 0.0036 |
| dist-bri-boost-may | 0.0031 | 0.0035 | 0.0058 |
| od2-bal-boost-buxom | 0.0011 | 0.0010 | 0.0016 |
| od2-bri-boost-buxom | 0.0013 | 0.0012 | 0.0022 |

- Everything is well under 0.01, including A2 lite.
- The edge captures score highest (worst): at low gain the pedal's hiss is a bigger share of the signal,
  and noise can't be modeled.
- The fuzz settings model much more easily than the Dover's dist (~0.002 vs ~0.012).
- Booster in front works: the boost's gain shows up as how hard it drives the Mas Malo, which NAM
  captures directly (a boost captured alone would come out as roughly unity gain plus EQ on this rig).

## Rerun

```
python3 make_config.py masmalo-<gain>-<tone>[-extra] ...   # writes config/data-*.json
./run_all.sh [names...]                                    # trains, copies models, scores
```

Needs the audio in `audio/`, which is not in git.
