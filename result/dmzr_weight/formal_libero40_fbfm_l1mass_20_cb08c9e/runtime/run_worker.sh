#!/usr/bin/env bash
set -euo pipefail

GPU="$1"
PORT="$2"
if [[ ! "$GPU" =~ ^[0-7]$ ]]; then
  echo "GPU must be in [0,7]: $GPU" >&2
  exit 2
fi

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726
OUTER="$ROOT/source/FBFM"
ROUTE="$OUTER/wam/dreamzero-libero"
RUN="$ROOT/runs/formal_libero40_fbfm_l1mass_20_cb08c9e"
WORKER="$RUN/workers/gpu$GPU"
SHARD="$RUN/shards/gpu$GPU"
PY=/mnt/project_eai_hs/zrm2/rlinf-dreamzero-venv/bin/python
CHECKPOINT=/mnt/project_eai_hs/zrm/checkpoints/dreamzero/RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000
TOKENIZER=/mnt/project_eai_hs/zrm/checkpoints/dreamzero/umt5-xxl
LIBERO_SOURCE=/mnt/project_eai_hs/zrm/FastWAM/third_party/LIBERO
LIBERO_LIB=/mnt/project_eai_hs/zrm/miniconda3/envs/libero/lib
COMMIT=cb08c9e552730d26cc446885e79a3e270a270d0c
STATE_WEIGHT=0.005833333333333334

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

TASK_ARGS=()
for task in "${TASKS[@]}"; do
  TASK_ARGS+=(--task "$task")
done
CLIENT_PYTHONPATH="$ROUTE/src:$OUTER:$ROOT/workspace/RLinf:$ROOT/workspace/dreamzero:$LIBERO_SOURCE"

if [[ "${3:-}" == "--tables-only" ]]; then
  mkdir -p "$SHARD"
  env CUDA_VISIBLE_DEVICES="$GPU" DREAMZERO_FBFM_ROUTE="$ROUTE" \
    LIBERO_CONFIG_PATH="$ROOT/runtime/libero_config" \
    LD_LIBRARY_PATH="$LIBERO_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    MUJOCO_GL=egl PYOPENGL_PLATFORM=egl PYTHONPATH="$CLIENT_PYTHONPATH" \
    "$PY" "$ROOT/runtime/run_shard_benchmark.py" \
    --base-workspace "$ROOT/workspace" --output "$SHARD" \
    "${TASK_ARGS[@]}" --mode FBFM --state-weight "$STATE_WEIGHT" \
    --trials 20 --max-steps 480 --seed 0 \
    --model-seed-rule fixed --solver-release-policy uniform \
    --host 127.0.0.1 --port "$PORT" --code-commit "$COMMIT" --tables-only
  exit 0
fi

mkdir -p "$WORKER" "$SHARD"
echo "$$" > "$WORKER/supervisor.pid"

apps=$(nvidia-smi --id="$GPU" --query-compute-apps=pid --format=csv,noheader | sed '/^$/d' | wc -l)
memory=$(nvidia-smi --id="$GPU" --query-gpu=memory.used --format=csv,noheader,nounits)
if (( apps != 0 || memory >= 1024 )); then
  echo "GPU $GPU is not exclusive: apps=$apps memory_mib=$memory" >&2
  exit 3
fi

rm -f "$WORKER/ready.json"
MODEL_PYTHONPATH="$ROUTE/src:$OUTER:$ROOT/workspace/RLinf:$ROOT/workspace/dreamzero:$LIBERO_SOURCE"
env CUDA_VISIBLE_DEVICES="$GPU" PYTHONUNBUFFERED=1 PYTHONPATH="$MODEL_PYTHONPATH" \
  "$PY" "$ROUTE/scripts/model_server.py" \
  --base-workspace "$ROOT/workspace" \
  --checkpoint "$CHECKPOINT" --tokenizer "$TOKENIZER" \
  --mode FBFM --state-weight "$STATE_WEIGHT" --device cuda:0 \
  --host 127.0.0.1 --port "$PORT" \
  --audit "$WORKER/solver.jsonl" --ready-file "$WORKER/ready.json" \
  >"$WORKER/server.log" 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$WORKER/server.pid"

cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
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

env CUDA_VISIBLE_DEVICES="$GPU" MUJOCO_EGL_DEVICE_ID="$GPU" \
  DREAMZERO_FBFM_ROUTE="$ROUTE" LIBERO_CONFIG_PATH="$ROOT/runtime/libero_config" \
  LD_LIBRARY_PATH="$LIBERO_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  MUJOCO_GL=egl PYOPENGL_PLATFORM=egl PYTHONUNBUFFERED=1 \
  PYTHONPATH="$CLIENT_PYTHONPATH" \
  "$PY" "$ROOT/runtime/run_shard_benchmark.py" \
  --base-workspace "$ROOT/workspace" --output "$SHARD" \
  "${TASK_ARGS[@]}" --mode FBFM --state-weight "$STATE_WEIGHT" \
  --trials 20 --max-steps 480 --seed 0 \
  --model-seed-rule fixed --solver-release-policy uniform \
  --host 127.0.0.1 --port "$PORT" --code-commit "$COMMIT"
