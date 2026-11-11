# 2026-11-06: Wampler Pantheon

33 captures: a set for each voice switch position, plus captures with a booster in front.
Models are in `complete-models/pantheon-*-a1.nam` and `-a2.nam`.

- **down**: edge / od1 / od2 in bal / bri / dark (9)
- **up**: edge / od1 / od2 in bal / bri / dark (9)
- **mid**: od1 / od2 / dist in bal / dark, dist also bri, plus two alternate settings `-2` (11)
- **boosts**: Friedman Buxom Boost (2, voice down) and Cascade germanium treble booster (4)

## The voice switch (`-down` / `-mid` / `-up`)

The Pantheon has a three-way voice switch, and the extra part of each name says which position was used:

- **down**: the classic Bluesbreaker sound.
- **up**: a slightly modded voice, a bit like the "boost" mode on a King of Tone.
- **mid**: the highest gain, most modded voice.

The Cascade captures have no voice in the name: with a treble booster in front the boost changes
the tone so much that the switch position barely matters.

## Setup

- Same input as the other pedals: NAM's standard sweep plus guitar playing, mono 48 kHz 16-bit.
- Delay -10 samples. Validation: the sweep's first 9 seconds. Training: 10-180.5s + 190-511s.
- 100 epochs, A1 and A2 (full + lite).
- Prepared with `tools/prep.py` per [TRAINING.md](../../TRAINING.md).
  down, mid and Buxom trained on the M4 Pro Mac mini (about 40 min per capture),
  up and Cascade on the M1 Pro laptop (about 70 min).

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
| edge-bal-up | 0.0057 | 0.0057 | 0.0078 |
| edge-bri-up | 0.0044 | 0.0042 | 0.0064 |
| edge-dark-up | 0.0094 | 0.0094 | 0.0109 |
| od1-bal-up | 0.0012 | 0.0012 | 0.0013 |
| od1-bri-up | 0.0005 | 0.0006 | 0.0008 |
| od1-dark-up | 0.0017 | 0.0019 | 0.0019 |
| od2-bal-up | 0.0011 | 0.0012 | 0.0015 |
| od2-bri-up | 0.0006 | 0.0005 | 0.0009 |
| od2-dark-up | 0.0025 | 0.0024 | 0.0031 |
| od1-bal-mid | 0.0072 | 0.0064 | 0.0093 |
| od1-dark-mid | 0.0052 | 0.0050 | 0.0074 |
| od1-dark-mid-2 | 0.0079 | 0.0087 | 0.0121 |
| od2-bal-mid | 0.0069 | 0.0060 | 0.0101 |
| od2-dark-mid | 0.0041 | 0.0043 | 0.0059 |
| od2-dark-mid-2 | 0.0087 | 0.0078 | 0.0123 |
| dist-bal-mid | 0.0020 | 0.0020 | 0.0023 |
| dist-bri-mid | 0.0224 | 0.0196 | 0.0375 |
| dist-dark-mid | 0.0024 | 0.0026 | 0.0029 |
| od2-bal-down-boost-buxom | 0.0017 | 0.0016 | 0.0029 |
| od2-bri-down-boost-buxom | 0.0016 | 0.0020 | 0.0028 |
| od2-bal-boost-cascade | 0.0018 | 0.0019 | 0.0027 |
| od2-bri-boost-cascade | 0.0031 | 0.0029 | 0.0046 |
| dist-bal-boost-cascade | 0.0029 | 0.0025 | 0.0044 |
| dist-bri-boost-cascade | 0.0031 | 0.0034 | 0.0047 |

- down is the cleanest set: everything under 0.003.
- up od1/od2 match or beat down; up edge is harder (0.004-0.011).
- mid od1/od2 run about 3-5x higher than down (0.004-0.009, a few lite models just over 0.01).
- dist-bri-mid is the outlier (0.02-0.037); the other mid dist settings are about 0.002.
  Possibly a recording issue; a re-record may be worth trying.
- The boosted captures all model well (0.0016-0.0047).
- The August 2026 Pantheon test (old rig, 10 epochs) scored about 0.006.

## Rerun

```
./run_all.sh [names...]   # trains (all configs if no names), copies models, scores
```

Needs the audio in `audio/`, which is not in git.
