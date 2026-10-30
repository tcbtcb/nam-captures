#!/bin/zsh
# Trains every capture in config/data-*.json on Apple silicon (MPS):
# all A1 models first, then all A2. Each finished model is copied to
# complete-models/<capture>-<format>.nam right away.
# A failed capture is logged and skipped; the rest keep going.
cd "${0:A:h}"
export MPLBACKEND=Agg
MODELS=../../complete-models
mkdir -p runs "$MODELS"

for fmt in a1 a2; do
  for cfg in config/data-*.json; do
    name=${${cfg:t:r}#data-}
    out=runs/$name-$fmt
    rm -rf "$out"; mkdir -p "$out"
    echo "=== $name $fmt start $(date +%T)"
    if nam-full "$cfg" "config/model-$fmt.json" config/learning-100ep.json "$out" --no-show \
         > "$out/train.log" 2>&1 && [[ -f $(echo $out/*/model.nam) ]]; then
      cp $out/*/model.nam "$MODELS/$name-$fmt.nam"
      echo "=== $name $fmt done  $(date +%T)"
    else
      echo "!!! $name $fmt FAILED $(date +%T) (see $out/train.log)"
    fi
  done
done

python3 -I score.py
echo "=== ALL DONE $(date +%T)"
