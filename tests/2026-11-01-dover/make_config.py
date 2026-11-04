"""Write config/data-<name>.json for each capture name given (e.g. dover-od1-bal).
Same layout as the Super AT: validation 0-9s, train 10-180.5s + 190-511s, delay -10."""
import json, sys
for name in sys.argv[1:]:
    pair = {"x_path": f"audio/{name}-sweep.wav", "y_path": f"audio/{name}-proc.wav",
            "delay": -10, "require_input_pre_silence": None}
    cfg = {"train": [dict(pair, start_seconds=10.0, stop_seconds=180.5, ny=8192),
                     dict(pair, start_seconds=190.0, stop_seconds=511.0, ny=8192)],
           "validation": dict(pair, start_seconds=0.0, stop_seconds=9.0, ny=None),
           "common": {}}
    json.dump(cfg, open(f"config/data-{name}.json", "w"), indent=4)
    print("wrote", name)
