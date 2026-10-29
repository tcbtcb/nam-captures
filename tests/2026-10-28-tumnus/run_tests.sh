#!/bin/zsh
# Trains the oct-28 test captures on Apple silicon (MPS).
# Phase 1: captures 1 and 2, A1 and A2.
# Phase 2: capture 3 step 2, starting from capture 1's best checkpoint.
# Settings (env vars):
#   LEARN        learning config in config/   (default demo.json = 10 epochs)
#   RUNS         output folder                (default runs)
#   SKIP_PHASE1  set to skip captures 1 and 2 (reuse existing ones in RUNS)
set -e
cd "${0:A:h}"  # run from this test folder
export MPLBACKEND=Agg
C=config
LEARN=${LEARN:-demo.json}
RUNS=${RUNS:-runs}
mkdir -p "$RUNS"

train() {  # name data model
  rm -rf "$RUNS/$1"; mkdir -p "$RUNS/$1"
  echo "=== $1 start $(date +%T)"
  nam-full "$C/$2" "$C/$3" "$C/$LEARN" "$RUNS/$1" --no-show > "$RUNS/$1/train.log" 2>&1
  echo "=== $1 done  $(date +%T)"
}

# Best checkpoint = lowest ESR in the filename.
# nam-full writes each run into a timestamped subfolder of the outdir.
best_ckpt() {
  ls $RUNS/$1/*/lightning_logs/version_0/checkpoints/*_ESR=*.ckpt \
    | python3 -I -c 'import sys,re; p=[l.strip() for l in sys.stdin]; print(min(p,key=lambda s: float(re.search(r"ESR=([0-9.e+-]+?)_MSE",s).group(1))))'
}

with_ckpt() {  # src_model_config ckpt out_name
  python3 -I -c 'import json,sys; c=json.load(open(sys.argv[1])); c["checkpoint_path"]=sys.argv[2]; json.dump(c,open(sys.argv[3],"w"),indent=4)' \
    "$C/$1" "$PWD/$2" "$C/$3"
}

if [[ -z "$SKIP_PHASE1" ]]; then
train c1-sweep-only-A1      data_1_sweep_only.json          pantheon_model.json
train c1-sweep-only-A2      data_1_sweep_only.json          malo_model_packed.json
train c2-sweep-plus-one-A1  data_2_sweep_plus_one_file.json pantheon_model.json
train c2-sweep-plus-one-A2  data_2_sweep_plus_one_file.json malo_model_packed.json
fi

A1_CKPT=$(best_ckpt c1-sweep-only-A1)
A2_CKPT=$(best_ckpt c1-sweep-only-A2)
with_ckpt pantheon_model.json     "$A1_CKPT" model_3b_A1_from_c1.json
with_ckpt malo_model_packed.json  "$A2_CKPT" model_3b_A2_from_c1.json
train c3-two-step-A1  data_3b_songs_finetune.json  model_3b_A1_from_c1.json
train c3-two-step-A2  data_3b_songs_finetune.json  model_3b_A2_from_c1.json
echo "=== ALL DONE $(date +%T)"
