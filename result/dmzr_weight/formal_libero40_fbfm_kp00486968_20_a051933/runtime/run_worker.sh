#!/usr/bin/env bash
set -euo pipefail

GPU="${1:?missing GPU index}"
PORT="${2:?missing TCP port}"
PROFILE="${3:-formal}"
if [[ ! "$GPU" =~ ^[0-7]$ ]]; then
  echo "GPU must be in [0,7]: $GPU" >&2
  exit 2
fi
if [[ "$PROFILE" != formal && "$PROFILE" != smoke ]]; then
  echo "profile must be formal or smoke: $PROFILE" >&2
  exit 2
fi

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_a051933_kp00486968_20260727
OUTER="$ROOT/source/FBFM"
ROUTE="$OUTER/wam/dreamzero-libero"
PY=/mnt/project_eai_hs/zrm2/rlinf-dreamzero-venv/bin/python
CHECKPOINT=/mnt/project_eai_hs/zrm/checkpoints/dreamzero/RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000
TOKENIZER=/mnt/project_eai_hs/zrm/checkpoints/dreamzero/umt5-xxl
LIBERO_SOURCE=/mnt/project_eai_hs/zrm/FastWAM/third_party/LIBERO
LIBERO_LIB=/mnt/project_eai_hs/zrm/miniconda3/envs/libero/lib
COMMIT=a051933e2b058d74bb268e94080464569d99ce39
STATE_WEIGHT=0.005833333333333334
STATE_FEEDBACK_KP=0.0486968

if [[ "$PROFILE" == smoke ]]; then
  RUN="$ROOT/runs/smoke_libero_spatial1_fbfm_kp00486968_a051933"
  TASKS=(libero_spatial:1)
  TRIALS=1
else
  RUN="$ROOT/runs/formal_libero40_fbfm_kp00486968_20_a051933"
  TRIALS=20
  case "$GPU" in
    0) TASKS=(libero_spatial:0 libero_spatial:8 libero_object:6 libero_goal:4 libero_10:2) ;;
    1) TASKS=(libero_spatial:1 libero_spatial:9 libero_object:7 libero_goal:5 libero_10:3) ;;
    2) TASKS=(libero_spatial:2 libero_object:0 libero_object:8 libero_goal:6 libero_10:4) ;;
    3) TASKS=(libero_spatial:3 libero_object:1 libero_object:9 libero_goal:7 libero_10:5) ;;
    4) TASKS=(libero_spatial:4 libero_object:2 libero_goal:0 libero_goal:8 libero_10:6) ;;
    5) TASKS=(libero_spatial:5 libero_object:3 libero_goal:1 libero_goal:9 libero_10:7) ;;
    6) TASKS=(libero_spatial:6 libero_object:4 libero_goal:2 libero_10:0 libero_10:8) ;;
    7) TASKS=(libero_spatial:7 libero_object:5 libero_goal:3 libero_10:1 libero_10:9) ;;
  esac
fi

WORKER="$RUN/workers/gpu$GPU"
SHARD="$RUN/shards/gpu$GPU"
TASK_ARGS=()
for task in "${TASKS[@]}"; do
  TASK_ARGS+=(--task "$task")
done
MODEL_PYTHONPATH="$ROUTE/src:$OUTER:$ROOT/workspace/RLinf:$ROOT/workspace/dreamzero:$LIBERO_SOURCE"
CLIENT_PYTHONPATH="$MODEL_PYTHONPATH"

if [[ "${4:-}" == "--tables-only" ]]; then
  [[ "$PROFILE" == formal ]] || { echo "tables-only is formal-only" >&2; exit 2; }
  mkdir -p "$SHARD"
  env CUDA_VISIBLE_DEVICES="$GPU" LIBERO_CONFIG_PATH="$ROOT/runtime/libero_config" \
    LD_LIBRARY_PATH="$LIBERO_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    MUJOCO_GL=egl PYOPENGL_PLATFORM=egl PYTHONPATH="$CLIENT_PYTHONPATH" \
    "$PY" "$ROUTE/scripts/run_libero_benchmark.py" \
    --base-workspace "$ROOT/workspace" --output "$SHARD" \
    "${TASK_ARGS[@]}" --mode FBFM --state-weight "$STATE_WEIGHT" \
    --state-feedback-kp "$STATE_FEEDBACK_KP" --trials "$TRIALS" \
    --max-steps 480 --seed 0 --model-seed-rule fixed \
    --solver-release-policy uniform --host 127.0.0.1 --port "$PORT" \
    --code-commit "$COMMIT" --tables-only
  exit 0
fi

mkdir -p "$WORKER" "$SHARD"
echo "$$" > "$WORKER/supervisor.pid"
rm -f "$WORKER/.done" "$WORKER/.failed" "$WORKER/ready.json"

apps=$(nvidia-smi --id="$GPU" --query-compute-apps=pid --format=csv,noheader | sed '/^$/d' | wc -l)
memory=$(nvidia-smi --id="$GPU" --query-gpu=memory.used --format=csv,noheader,nounits)
if (( apps != 0 || memory >= 1024 )); then
  echo "GPU $GPU is not exclusive: apps=$apps memory_mib=$memory" >&2
  exit 3
fi

env CUDA_VISIBLE_DEVICES="$GPU" PYTHONUNBUFFERED=1 PYTHONPATH="$MODEL_PYTHONPATH" \
  "$PY" "$ROUTE/scripts/model_server.py" \
  --base-workspace "$ROOT/workspace" \
  --checkpoint "$CHECKPOINT" --tokenizer "$TOKENIZER" \
  --mode FBFM --state-weight "$STATE_WEIGHT" \
  --state-feedback-kp "$STATE_FEEDBACK_KP" --device cuda:0 \
  --host 127.0.0.1 --port "$PORT" \
  --audit "$WORKER/solver.jsonl" --ready-file "$WORKER/ready.json" \
  >"$WORKER/server.log" 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$WORKER/server.pid"

cleanup() {
  status=$?
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
  if (( status == 0 )); then
    touch "$WORKER/.done"
  else
    printf '%s\n' "$status" > "$WORKER/.failed"
  fi
}
trap cleanup EXIT

for _ in $(seq 1 360); do
  [[ -f "$WORKER/ready.json" ]] && break
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "model server exited before ready" >&2
    exit 4
  fi
  sleep 5
done
[[ -f "$WORKER/ready.json" ]] || { echo "model server readiness timeout" >&2; exit 5; }

"$PY" - "$WORKER/ready.json" "$STATE_WEIGHT" "$STATE_FEEDBACK_KP" <<'PY'
import json
import math
import sys

ready = json.load(open(sys.argv[1], encoding="utf-8"))
state_weight = float(sys.argv[2])
kp = float(sys.argv[3])
assert ready["mode"] == "FBFM", ready
assert math.isclose(float(ready["state_weight"]), state_weight, rel_tol=0, abs_tol=1e-15), ready
assert math.isclose(float(ready["state_feedback_kp"]), kp, rel_tol=0, abs_tol=1e-15), ready
assert math.isclose(float(ready["effective_state_weight"]), state_weight * kp, rel_tol=0, abs_tol=1e-15), ready
PY

env CUDA_VISIBLE_DEVICES="$GPU" MUJOCO_EGL_DEVICE_ID="$GPU" \
  LIBERO_CONFIG_PATH="$ROOT/runtime/libero_config" \
  LD_LIBRARY_PATH="$LIBERO_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  MUJOCO_GL=egl PYOPENGL_PLATFORM=egl PYTHONUNBUFFERED=1 \
  PYTHONPATH="$CLIENT_PYTHONPATH" \
  "$PY" "$ROUTE/scripts/run_libero_benchmark.py" \
  --base-workspace "$ROOT/workspace" --output "$SHARD" \
  "${TASK_ARGS[@]}" --mode FBFM --state-weight "$STATE_WEIGHT" \
  --state-feedback-kp "$STATE_FEEDBACK_KP" --trials "$TRIALS" \
  --max-steps 480 --seed 0 --model-seed-rule fixed \
  --solver-release-policy uniform --host 127.0.0.1 --port "$PORT" \
  --code-commit "$COMMIT"
