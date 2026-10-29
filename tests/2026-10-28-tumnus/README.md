# 2026-10-28: Wampler Tumnus, rig and training-data tests

## Questions

1. Does the new reamp box + DI + recording setup work as expected? (Guess: mostly, maybe small gain tweaks.)
2. Do extra training files beyond NAM's standard sweep add noticeable value? (Guess: the sweep alone gets nearly everything.)

## Captures

| | Training data |
|---|---|
| c1 | NAM standard sweep only |
| c2 | Sweep + sections of two songs, one file |
| c3 | Two steps: start from c1's model, then keep training on the songs only |

Each was trained as A1 (standard WaveNet) and A2 (packed: "full" and "lite" in one file).

## Setup details

- Latency: **2 samples**, measured from the sweep's calibration blips (10.5s and 11.5s). The recording software compensates for latency.
- Validation: the sweep's first 9 seconds, the same for every capture.
- Held-out song test: the last 20 seconds of the song section. No model trained on it.
- The sweep files are 189.5s (the official one is 190s). The cut-short validation copy at the end is left out of training.
- Original exports were stereo (identical channels). `audio/` holds the left-channel mono copies.
- The song DI input clips lightly (430 samples, longest run about 0.4ms). Accepted for this test.

## Results: 100 epochs

ESR, lower is better. NAM calls under 0.01 "Great!" and 0.01–0.035 "Not bad!"

| Capture | Model | Sweep validation | Held-out song |
|---|---|---|---|
| c1 sweep only | A1 | 0.0093 | 0.0117 |
| | A2 full | 0.0096 | 0.0114 |
| | A2 lite | 0.0117 | 0.0164 |
| c2 sweep + songs | A1 | **0.0085** | **0.0097** |
| | A2 full | 0.0089 | **0.0097** |
| | A2 lite | 0.0095 | 0.0103 |
| c3 two-step | A1 | 0.0095 | 0.0106 |
| | A2 full | 0.0103 | 0.0130 |
| | A2 lite | 0.0102 | 0.0109 |

At 10 epochs, every score was roughly twice as high.

## Findings

- **Rig works.** Noise floor is about -64 dBFS against a -19 to -24 dBFS signal (39–46 dB SNR). Noise alone would only limit ESR to about 0.0001, so it isn't what's holding scores back. Faint 60 Hz hum and tones near 22 kHz are present but tiny.
- **The sweep gets most of the way.** Adding real playing improved held-out song error by about 15–20% at 100 epochs, and by about a third at 10 epochs. A2 lite gained the most.
- **One combined file (c2) beat two-step (c3)** at 100 epochs. Use one file.
- **A2 full is about the same as A1.**
- **Same pedal, old vs. new rig:** the August Tumnus capture (old split setup) scored 0.021 for A1 at 10 epochs. The new rig scored 0.017–0.018. No sign the old looper method was better. The Pantheon's 0.006 is most likely because it's an easier pedal to model.
- Each setup ran once, so differences of about 0.001 may be noise.

Recommended model: `complete-models/2026-10-28-tumnus/tumnus-c2-sweep-plus-one-A1.nam` (or the A2 version).

## Rerun

```
./run_tests.sh                                                     # 10 epochs -> runs/
LEARN=learning_100ep.json RUNS=runs-100ep ./run_tests.sh           # 100 epochs -> runs-100ep/
python3 score_models.py runs-100ep                                  # score table
```

Needs the mono audio in `audio/`, which is not in git.
