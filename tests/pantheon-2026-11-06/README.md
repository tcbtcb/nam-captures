# 2026-11-06: Wampler Pantheon, voice switch down

Nine captures: edge / od1 / od2, each in bal / bri / dark, all with the voice switch **down**.
Models are in `complete-models/pantheon-*-down-a1.nam` and `-a2.nam`.

## The voice switch (`-down` / `-mid` / `-up`)

The Pantheon has a three-way voice switch, and the extra part of each name says which position was used:

- **down**: the classic Bluesbreaker sound.
- **up**: a slightly modded voice, a bit like the "boost" mode on a King of Tone.
- **mid**: the highest gain, most modded voice.

Plan: a full set of nine captures for each position (27 captures, 54 models).
This folder is the `down` set.

## Setup

- Same input as the other pedals: NAM's standard sweep plus guitar playing, mono 48 kHz 16-bit.
- Delay -10 samples. Validation: the sweep's first 9 seconds. Training: 10-180.5s + 190-511s.
- 100 epochs, A1 and A2 (full + lite).
- First run done entirely with `tools/prep.py` and [TRAINING.md](../../TRAINING.md), trained on the M4 Pro Mac mini:
  about 40 min per capture (A1 + A2), vs about 70 on the M1 Pro laptop.

## Results

ESR on the validation clip (lower is better; NAM calls < 0.01 "Great!").

| Capture | A1 | A2 full | A2 lite |
|---|---|---|---|
| edge-bal-down | 0.0010 | 0.0010 | 0.0012 |
| edge-bri-down | 0.0008 | 0.0007 | 0.0010 |
| edge-dark-down | 0.0018 | 0.0019 | 0.0018 |
| od1-bal-down | 0.0012 | 0.0011 | 0.0016 |
| od1-bri-down | 0.0023 | 0.0022 | 0.0028 |
| od1-dark-down | 0.0015 | 0.0013 | 0.0023 |
| od2-bal-down | 0.0012 | 0.0011 | 0.0014 |
| od2-bri-down | 0.0008 | 0.0008 | 0.0009 |
| od2-dark-down | 0.0020 | 0.0021 | 0.0026 |

- Every model is under 0.003, including A2 lite: the cleanest set so far.
- The August 2026 Pantheon test (old rig, 10 epochs) scored about 0.006; these are 3-8x better.

## Rerun

```
./run_all.sh [names...]   # trains (all configs if no names), copies models, scores
```

Needs the audio in `audio/`, which is not in git.
