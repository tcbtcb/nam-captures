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

A new capture of the same gear and settings **replaces** the old files under the same name. No version numbers. Git keeps the old version in history.

`complete-models/` is flat (no dated folders), so a new model simply overwrites the old one. Dates and test details live in `tests/<date-pedal>/`.
