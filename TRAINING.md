# Training a pedal

Run everything from the repo folder (`nam-captures`).

**1. Export** from Live: mono, 48 kHz, 16-bit, named per [NAMING.md](NAMING.md)
(`pedal-gain-tone[-extra]`). A `main-nam` prefix and spaces are fine; they get cleaned up.
Also export the sweep-plus file once.

**2. Prep** (checks the files, trims, renames, writes configs):

```
python3 tools/prep.py tests/<date>-<pedal> <sweep.wav> <exported files...>
```

e.g. `python3 tools/prep.py tests/2026-11-06-tumnus ~/exports/main-nam-sweep-plus.wav ~/exports/main-nam-tumnus-*.wav`

Read what it prints. **SKIPPED** = fix and re-run. **WARNING** = look, then decide.
**NOTE: new pedal name** = check the spelling. It ends with the train command.

**3. Train** (paste the command prep printed):

```
cd tests/<date>-<pedal>
caffeinate -i ./run_all.sh <names...>
```

About 70 min per capture. Models go to `complete-models/`, scores print at the end (lower is better; under 0.01 is great).
To pause for music, from the repo folder: `tools/training.sh pause` / `resume` (with `sudo` and the full path from another user).

**4. Listen, then commit and push** the models and the test folder (audio and run files are ignored by git):

```
git add complete-models tests/<date>-<pedal>
git commit -m "Add <pedal> models"
git push
```
