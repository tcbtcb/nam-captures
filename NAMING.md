# Naming conventions

One pattern for everything (audio and models), so it's obvious what goes with what.

## Pattern

```
pedal-gain-tone[-extra]
```

All lowercase, parts separated by hyphens, no spaces.

| Part | Allowed values | Notes |
|---|---|---|
| `pedal` | gear name: `tumnus`, `pantheon`, `dover`, ... | Pedal or preamp. One word. |
| `gain` | `clean` < `edge` < `od1` < `od2` < `dist` < `fuzz` | In order of increasing gain. Fixed list. |
| `tone` | `bri`, `bal`, `dark` | Bright, balanced, dark. Fixed list. |
| `extra` | free text, optional | A switch or mode setting, e.g. `switchup`. Leave it off if not needed. |

Common extras:

- `-2`, `-3`, ...: another way to get the same gain and tone with different knob settings (e.g. `masmalo-edge-bal-2`). Not a recapture; see below.
- `-boost-<name>`: a booster in front of the pedal, captured together as one chain (e.g. `masmalo-od2-bri-boost-buxom`). Boosts alone aren't captured: on this rig a boost by itself comes out as roughly unity gain plus EQ.

## Models (`.nam`)

```
pedal-gain-tone[-extra]-format.nam
```

`format` is `a1` or `a2`, always last.

```
pantheon-od1-bri-switchup-a1.nam
dover-dist-bal-a2.nam
```

## Audio (`.wav`)

Each capture is a pair: what went into the gear, and what came out.

```
pedal-gain-tone[-extra]-sweep.wav   # signal sent to the gear (the NAM sweep + any extra playing)
pedal-gain-tone[-extra]-proc.wav    # processed: what came back from the gear
```

```
dover-dist-bal-sweep.wav
dover-dist-bal-proc.wav
```

Format: **48 kHz, 16-bit, mono**. Put the sweep and any extra playing in **one file**. In the 2026-10-28 tests, that beat both sweep-only and two separate files.

## Recaptures

A new capture of the same gear and settings **replaces** the old files under the same name. No version numbers. Git keeps the old version in history. (`-2` is for a *different* setting, not a redo.)

`complete-models/` is flat (no dated folders), so a new model simply overwrites the old one. Dates and test details live in `tests/<date-pedal>/`.
