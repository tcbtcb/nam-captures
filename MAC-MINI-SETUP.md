# Training on the Mac mini (isolated user)

Goal: NAM training on the music Mac without touching the music setup.
Everything lives in a separate **Standard** (non-admin) user's home folder.
Rule: **if any step asks for an admin password, stop.** (Step 1 is the only exception.)

## 1. Create the user (from the main user)

System Settings > Users & Groups > Add User:
- Type: **Standard** (not Administrator)
- Name: `nam`

This is the only step that needs your admin password.

## 2. Install Python (as `nam`)

Log in as `nam` (or Fast User Switching), open Terminal:

```
cd ~
curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh -b -p ~/miniconda3
~/miniconda3/bin/conda init zsh
```

Close and reopen Terminal. `which python3` should print `/Users/nam/miniconda3/bin/python3`.

## 3. Install the training tools

Same versions as the M1 laptop (Python 3.14):

```
pip install torch==2.11.0 neural-amp-modeler==0.13.0 pytorch-lightning==2.6.1 soundfile==0.14.0
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

The last line must print `True` (Apple GPU works). Install torch with pip, not conda: that was the Apple-silicon fix.

## 4. Get the repo and audio

```
git clone https://github.com/tcbtcb/nam-captures.git ~/nam-captures
```

(HTTPS works for a public repo. Pushing from the mini would need its own GitHub login; not needed to train.)

Audio isn't in git. Copy each test's `audio/` folder into the matching `~/nam-captures/tests/<test>/audio/`.

## 5. Train

```
cd ~/nam-captures/tests/<test>
caffeinate -i ./run_all.sh <capture names>     # or no names = every config in the folder
```

`caffeinate -i` keeps the Mac awake until training ends (no admin needed).
Finished models land in `~/nam-captures/complete-models/`.

## Pausing for music

Don't record while training runs. To pause (frees CPU/GPU, keeps progress):

```
sudo ~nam/nam-captures/tools/training.sh pause     # from the main user
~/nam-captures/tools/training.sh pause             # from the nam user
```

`resume` carries on where it stopped, hours or days later. `status` shows whether it's paused (`T`).
A restart loses the paused run; rerun `./run_all.sh` for that capture.

## Undo everything

Delete the `nam` user in System Settings > Users & Groups. Nothing else was installed.
