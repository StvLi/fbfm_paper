#!/usr/bin/env bash
set -u

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_a051933_kp00486968_20260727
RUN="$ROOT/runs/formal_libero40_fbfm_kp00486968_20_a051933"
PY=/mnt/project_eai_hs/zrm2/rlinf-dreamzero-venv/bin/python
LOG="$RUN/persistent-supervisor.log"

mkdir -p "$RUN"
exec >>"$LOG" 2>&1

episode_count() {
  "$PY" - "$RUN" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
keys = set()
for path in root.glob("shards/gpu*/tasks/*/task_*/episodes.jsonl"):
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        keys.add((record["suite"], int(record["task_id"]), int(record["trial_id"])))
print(len(keys))
PY
}

pid_alive() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid=$(cat "$pid_file")
  [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null
}

wait_for_monitor() {
  while pid_alive "$RUN/monitor.pid"; do
    sleep 30
  done
}

printf '%s persistent supervisor started\n' "$(date --iso-8601=seconds)"

while true; do
  count=$(episode_count) || {
    printf '%s episode count failed; retrying\n' "$(date --iso-8601=seconds)"
    sleep 60
    continue
  }
  printf '%s unique episodes=%s\n' "$(date --iso-8601=seconds)" "$count"

  if (( count == 800 )); then
    touch "$RUN/.persistent_complete"
    printf '%s formal run complete\n' "$(date --iso-8601=seconds)"
    while true; do sleep 3600; done
  fi
  if (( count > 800 )); then
    touch "$RUN/.persistent_failed"
    printf '%s refusing launch: episode count exceeds 800\n' "$(date --iso-8601=seconds)"
    while true; do sleep 3600; done
  fi

  if pid_alive "$RUN/monitor.pid"; then
    printf '%s adopting existing monitor\n' "$(date --iso-8601=seconds)"
    wait_for_monitor
    continue
  fi

  alive=0
  for gpu in $(seq 0 7); do
    if pid_alive "$RUN/workers/gpu$gpu/supervisor.pid"; then
      alive=$((alive + 1))
    fi
  done
  if (( alive > 0 )); then
    printf '%s found %s live supervisors without monitor; starting monitor\n' \
      "$(date --iso-8601=seconds)" "$alive"
    nohup setsid bash "$ROOT/runtime/monitor.sh" \
      >"$RUN/monitor-supervisor.log" 2>&1 </dev/null &
    echo "$!" > "$RUN/monitor-launcher.pid"
    sleep 2
    wait_for_monitor
    continue
  fi

  rm -f "$RUN/.persistent_failed"
  printf '%s launching formal workers from episode %s\n' \
    "$(date --iso-8601=seconds)" "$count"
  if bash "$ROOT/runtime/launch_all.sh"; then
    sleep 2
    wait_for_monitor
  else
    status=$?
    printf '%s launch_all failed with status %s; retrying\n' \
      "$(date --iso-8601=seconds)" "$status"
    sleep 60
  fi
done
