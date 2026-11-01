#!/bin/zsh
# Pause, resume, or check NAM training (nam-full) without losing progress.
#   tools/training.sh pause    # frees the CPU/GPU; progress is kept in memory
#   tools/training.sh resume   # carries on exactly where it stopped
#   tools/training.sh status
# Run from the training user as-is. From another user, put sudo in front.
# A paused run is lost if the Mac restarts.
pids=($(pgrep -f nam-full))
if (( ! $#pids )); then echo "No training running."; exit 0; fi
case $1 in
  pause)  kill -STOP $pids && echo "Paused: $pids" ;;
  resume) kill -CONT $pids && echo "Resumed: $pids" ;;
  status) ps -o pid,user,stat,etime,command -p ${(j:,:)pids}
          echo "(stat T = paused)" ;;
  *) echo "usage: $0 pause|resume|status"; exit 1 ;;
esac
