# 2026-10-29: Keeley Super AT (Andy Timmons)

Ten captures: edge / od1 / od2, each in bal / bri / dark, plus `dist-bri` with the gain dimed.
Models are in `complete-models/superat-*-a1.nam` and `-a2.nam`.

## Setup

- One input file for every capture: NAM's standard sweep plus guitar playing (including volume-rolled-back passages), 512s, mono 48 kHz 16-bit.
- Delay: **-10 samples** for all ten. The output's onset lands about 6 samples before the input's calibration click in every file (likely converter filter pre-ringing or DAW latency compensation). -10 also matches NAM's own calibration. (The 2026-10-28 Tumnus test used +2, which was probably slightly off.)
- Validation: the sweep's first 9 seconds (NAM's standard validation clip).
- Training: 10-180.5s (sweep) + 190-511s (playing). The cut-short duplicate of the validation clip at 180.5-189.5s is left out. Checked: the validation audio does not appear anywhere in the training ranges.
- 100 epochs, A1 (standard WaveNet) and A2 (packed: full + lite), on Apple silicon (MPS).
- Fixed export-name typos: `od1-darl` -> `od1-dark`, `dist-nri` -> `dist-bri`.

## Results

ESR on the validation clip (lower is better; NAM calls < 0.01 "Great!").

| Capture | A1 | A2 full | A2 lite |
|---|---|---|---|
| edge-bal | 0.0025 | 0.0032 | 0.0035 |
| edge-bri | 0.0005 | 0.0007 | 0.0006 |
| edge-dark | 0.0035 | 0.0030 | 0.0029 |
| od1-bal | 0.0034 | 0.0034 | 0.0036 |
| od1-bri | 0.0004 | 0.0003 | 0.0006 |
| od1-dark | 0.0002 | 0.0002 | 0.0003 |
| od2-bal | 0.0006 | 0.0005 | 0.0009 |
| od2-bri | 0.0010 | 0.0011 | 0.0016 |
| od2-dark | 0.0006 | 0.0005 | 0.0010 |
| dist-bri | 0.0010 | 0.0010 | 0.0016 |

## Notes

- Every model, including A2 lite, is well under 0.01.
- A1 and A2 full are about the same. A2 lite is close behind.
- edge-bal, edge-dark, and od1-bal are the weakest (about 0.003). od1-bal had a small noise pop just before the calibration click; extra noise may be what limits these.
- ESR measures how closely the model copies the *recording*. Reamp level/impedance and interface coloring are in the recording, so they're copied too, and ESR can't judge them. Listening is the final test.
- All playing was used for training, so there's no held-out playing score this time. With the Tumnus, the held-out playing score was ~15-25% worse than the validation score.
- Run time: about 21 hours in total, mostly because the laptop was on a weak power supply. On full power, A1 took about 25 min and A2 about 43 min per capture (~11 hours for all ten).

## Rerun

```
./run_all.sh     # trains every config/data-*.json (A1, then A2), copies models to complete-models/, scores
python3 score.py # score table -> scores.json
```

Needs the audio in `audio/`, which is not in git.
