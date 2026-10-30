"""Score each trained model on its capture's sweep validation (0-9s).
ESR = error energy / target energy (lower is better; NAM calls < 0.01 "Great!").
A2 files are scored per size (lite / full)."""
import glob, json, os
import numpy as np, soundfile as sf, torch
from nam.models import init_from_nam

ROOT = os.path.dirname(os.path.abspath(__file__))
SR, DELAY, VAL = 48000, -10, (0.0, 9.0)


def esr(model, x, y):
    # NAM pairs output sample t with input sample t - DELAY
    a, b = int(VAL[0] * SR), int(VAL[1] * SR)
    shift = -DELAY
    pre = min(a + shift, model.receptive_field)
    with torch.no_grad():
        pred = model(torch.from_numpy(x[a + shift - pre:b + shift]), pad_start=True).numpy()[pre:]
    target = y[a:b]
    return float(np.sum((target - pred) ** 2) / np.sum(target ** 2))


def models_in(path):
    cfg = json.load(open(path))
    if cfg["architecture"] == "SlimmableContainer":
        subs = cfg["config"]["submodels"]
        return [(n, init_from_nam(s["model"])) for n, s in zip(["lite", "full"], subs)]
    return [("a1", init_from_nam(cfg))]


rows = []
for path in sorted(glob.glob(f"{ROOT}/runs/*/*/model.nam")):
    run = os.path.basename(os.path.dirname(os.path.dirname(path)))
    name = run.rsplit("-", 1)[0]
    x, _ = sf.read(f"{ROOT}/audio/{name}-sweep.wav", dtype="float32")
    y, _ = sf.read(f"{ROOT}/audio/{name}-proc.wav", dtype="float32")
    for size, m in models_in(path):
        m.eval()
        rows.append((name, size, esr(m, x, y)))

print(f"{'capture':20s} {'model':5s} {'ESR':>8s}")
for r in rows:
    print(f"{r[0]:20s} {r[1]:5s} {r[2]:8.4f}")
json.dump(rows, open(f"{ROOT}/scores.json", "w"), indent=2)
