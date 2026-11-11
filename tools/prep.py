"""Prepare exported captures for training (steps 1-3 in TRAINING.md).

    python3 tools/prep.py tests/<date>-<pedal> <sweep.wav> <exported files...>

For each exported file it:
  - works out the capture name (drops "main-nam", lowercases, spaces -> hyphens)
    and checks it follows NAMING.md: pedal-gain-tone[-extra]
  - checks the audio: mono, 48 kHz, 16-bit, not silent, no clipping, level near the sweep's
  - trims the sweep and the export to the same length (NAM needs equal lengths)
  - saves <name>-sweep.wav and <name>-proc.wav into the test folder's audio/
  - writes config/data-<name>.json
Then it prints the command to train them.
"""
import json, os, re, shutil, sys
import numpy as np, soundfile as sf

SR = 48000
GAINS = ["clean", "edge", "od1", "od2", "dist", "fuzz"]
TONES = ["bri", "bal", "dark"]
PREAMPS = ["ird", "asc1"]  # named preamp-gain-<switches...>-tone (see NAMING.md)
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")


def db(v):
    return 20 * np.log10(max(float(v), 1e-12))


def name_of(path):
    n = os.path.splitext(os.path.basename(path))[0].lower().replace(" ", "-")
    n = re.sub(r"^main-nam-*", "", n)
    return re.sub(r"-+", "-", n).strip("-")


def known_pedals():
    d = os.path.join(os.path.dirname(TEMPLATE), "..", "complete-models")
    return {f.split("-")[0] for f in os.listdir(d)} if os.path.isdir(d) else set()


def check_name(n):
    p = n.split("-")
    if p[0] in PREAMPS:
        if len(p) < 4:
            return "should be preamp-gain-<switches...>-tone"
        if p[1] not in GAINS:
            return f"gain '{p[1]}' isn't one of {GAINS}"
        if p[-1] not in TONES:
            return f"tone (last part) '{p[-1]}' isn't one of {TONES}"
        return None
    if len(p) < 3:
        return "should be pedal-gain-tone[-extra]"
    if p[1] not in GAINS:
        return f"gain '{p[1]}' isn't one of {GAINS}"
    if p[2] not in TONES:
        return f"tone '{p[2]}' isn't one of {TONES}"
    return None


def read(path):
    info = sf.info(path)
    problems = []
    if info.channels != 1:
        problems.append(f"{info.channels} channels (needs mono)")
    if info.samplerate != SR:
        problems.append(f"{info.samplerate} Hz (needs 48000)")
    if info.subtype != "PCM_16":
        problems.append(f"{info.subtype} (needs 16-bit)")
    if problems:
        return None, problems
    return sf.read(path, dtype="int16")[0], []


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    test, sweep_path, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    if os.path.basename(os.path.dirname(os.path.abspath(test))) != "tests":
        sys.exit(f"Test folder must be inside tests/, e.g. tests/2026-11-06-tumnus (got {test})")

    # New test folder: copy the scripts and model/learning configs from the template.
    for root, _, fs in os.walk(TEMPLATE):
        for f in fs:
            dst = os.path.join(test, os.path.relpath(os.path.join(root, f), TEMPLATE))
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(root, f), dst)
    os.makedirs(os.path.join(test, "audio"), exist_ok=True)

    sweep, problems = read(sweep_path)
    if problems:
        sys.exit(f"Sweep {sweep_path}: " + ", ".join(problems))

    pedals = known_pedals()
    ok = []
    for path in files:
        n = name_of(path)
        print(f"\n{os.path.basename(path)}  ->  {n}")
        err = check_name(n)
        if err:
            print(f"  SKIPPED: name {err}. Rename the file and run again.")
            continue
        if n.split("-")[0] not in pedals:
            print(f"  NOTE: '{n.split('-')[0]}' is a new pedal name. Check the spelling.")
        y, problems = read(path)
        if problems:
            print("  SKIPPED: " + ", ".join(problems) + ". Re-export.")
            continue
        if not np.any(y):
            print("  SKIPPED: the file is all silence. Re-export.")
            continue

        # Same length for both. Anything cut from the export should be silence.
        L = min(len(y), len(sweep))
        if np.any(y[L + SR // 10:]):  # ignore a short tail (<0.1s)
            print(f"  WARNING: export has audio past the sweep's end ({len(sweep) / SR:.1f}s); it was cut off.")
        if L < 200 * SR:
            print(f"  SKIPPED: only {L / SR:.1f}s long; the export looks cut short.")
            continue
        x, y = sweep[:L], y[:L]

        clip = int(np.sum((y == 32767) | (y == -32768)))
        a, b = 10 * SR, int(180.5 * SR)
        diff = db(np.sqrt(np.mean(y[a:b].astype(float) ** 2))) - db(np.sqrt(np.mean(x[a:b].astype(float) ** 2)))
        print(f"  {L / SR:.1f}s, level {diff:+.1f} dB vs sweep, clipped samples: {clip}")
        if clip:
            print("  WARNING: clipping. Lower the interface gain and re-record if it's more than a few samples.")
        if abs(diff) > 3:
            print("  WARNING: level is more than 3 dB away from the sweep. Fine if intended.")

        sf.write(os.path.join(test, "audio", f"{n}-sweep.wav"), x, SR, subtype="PCM_16")
        sf.write(os.path.join(test, "audio", f"{n}-proc.wav"), y, SR, subtype="PCM_16")

        # Validation: sweep's first 9s. Training: the rest, minus the cut-short copy
        # of the validation clip at 180.5-190s. Delay -10 fits this rig (see READMEs).
        pair = {"x_path": f"audio/{n}-sweep.wav", "y_path": f"audio/{n}-proc.wav",
                "delay": -10, "require_input_pre_silence": None}
        stop = min(511.0, L / SR - 0.5)
        cfg = {"train": [dict(pair, start_seconds=10.0, stop_seconds=180.5, ny=8192),
                         dict(pair, start_seconds=190.0, stop_seconds=stop, ny=8192)],
               "validation": dict(pair, start_seconds=0.0, stop_seconds=9.0, ny=None),
               "common": {}}
        os.makedirs(os.path.join(test, "config"), exist_ok=True)
        json.dump(cfg, open(os.path.join(test, "config", f"data-{n}.json"), "w"), indent=4)
        ok.append(n)

    print(f"\n{len(ok)} of {len(files)} ready.")
    if ok:
        print(f"\nTo train:\n  cd {test}\n  caffeinate -i ./run_all.sh {' '.join(ok)}")


if __name__ == "__main__":
    main()
