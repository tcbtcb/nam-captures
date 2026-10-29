# nam-captures

Neural Amp Modeler (NAM) captures of my pedals and preamps, made with a reamp box and DI.

- `complete-models/` — finished `.nam` files, one folder per capture session.
- `tests/` — one folder per test session: run scripts, configs, and results. Audio and training output stay local (see `.gitignore`).
- File names follow [NAMING.md](NAMING.md).

## Setup

- Python from the miniconda base env, with `neural-amp-modeler` 0.13.0.
- PyTorch installed from pip (`torch==2.11.0`), not conda, so Apple silicon GPU (MPS) works. That's about 27x faster than CPU. Learning configs use `"accelerator": "mps"`.
- Audio: 48 kHz, 16-bit, **mono**. Export mono; stereo exports have to be converted first.
