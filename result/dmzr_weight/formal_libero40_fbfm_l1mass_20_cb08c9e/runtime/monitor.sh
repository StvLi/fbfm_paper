#!/usr/bin/env bash
set -u

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726
RUN="$ROOT/runs/formal_libero40_fbfm_l1mass_20_cb08c9e"
PY=/mnt/project_eai_hs/zrm2/rlinf-dreamzero-venv/bin/python
EXPECTED=()
for suite in libero_spatial libero_object libero_goal libero_10; do
  for task_id in $(seq 0 9); do
    EXPECTED+=(--expected-task "$suite:$task_id")
  done
done

echo "$$" > "$RUN/monitor.pid"
while true; do
  "$PY" "$ROOT/runtime/aggregate_libero40_shards.py" \
    --root "$RUN" "${EXPECTED[@]}" >>"$RUN/aggregate.log" 2>&1 || true
  alive=0
  for gpu in $(seq 0 7); do
    pid_file="$RUN/workers/gpu$gpu/supervisor.pid"
    if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
      alive=$((alive + 1))
    fi
  done
  if [[ "$alive" -eq 0 ]]; then
    "$PY" "$ROOT/runtime/aggregate_libero40_shards.py" \
      --root "$RUN" "${EXPECTED[@]}" >>"$RUN/aggregate.log" 2>&1 || true
    exit 0
  fi
  sleep 30
done
