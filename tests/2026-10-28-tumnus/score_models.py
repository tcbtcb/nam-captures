"""Score every exported model in runs/ on the same audio:
  - sweep validation (0-9s), which every run also used for its own validation
  - held-out song audio (last 20s of the song section), which no run trained on
ESR = error energy / target energy (lower is better).
A2 (.nam SlimmableContainer) files are scored per submodel (lite / full)."""
import glob, json, os, sys
import numpy as np, soundfile as sf, torch
from nam.models import init_from_nam

ROOT = os.path.dirname(os.path.abspath(__file__))
RUNS = sys.argv[1] if len(sys.argv) > 1 else "runs"
SR, DELAY = 48000, 2
F2 = f"{ROOT}/audio/sweep-plus-one-file/main-nam"
x_all, _ = sf.read(f"{F2} train.wav", dtype="float32")
y_all, _ = sf.read(f"{F2} 2-Audio.wav", dtype="float32")
TESTS = {"sweep_val": (0.0, 9.0), "song_holdout": (381.5, 401.5)}


def esr(model, a, b):
    a, b = int(a * SR), int(b * SR)
    pre = min(a, model.receptive_field)
    with torch.no_grad():
        pred = model(torch.from_numpy(x_all[a - pre:b]), pad_start=True).numpy()[pre:]
    target = y_all[a + DELAY:b + DELAY]  # y lags x by DELAY samples
    return float(np.sum((target - pred) ** 2) / np.sum(target ** 2))


def models_in(path):
    cfg = json.load(open(path))
    if cfg["architecture"] == "SlimmableContainer":
        subs = cfg["config"]["submodels"]
        names = ["lite", "full"] if len(subs) == 2 else [str(i) for i in range(len(subs))]
        return [(n, init_from_nam(s["model"])) for n, s in zip(names, subs)]
    return [("A1", init_from_nam(cfg))]


rows = []
# nam-full writes each run into runs/<name>/<timestamp>/model.nam
for path in sorted(glob.glob(f"{ROOT}/{RUNS}/*/*/model.nam")):
    run = os.path.basename(os.path.dirname(os.path.dirname(path)))
    for name, m in models_in(path):
        m.eval()
        rows.append((run, name, *(esr(m, *TESTS[t]) for t in TESTS)))

print(f"{'run':24s} {'model':5s} {'sweep_val':>10s} {'song_holdout':>13s}")
for r in rows:
    print(f"{r[0]:24s} {r[1]:5s} {r[2]:10.4f} {r[3]:13.4f}")
json.dump(rows, open(f"{ROOT}/{RUNS}/scores.json", "w"), indent=2)
