#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_a051933_kp00486968_20260727
RUN="$ROOT/runs/formal_libero40_fbfm_kp00486968_20_a051933"
EXPECTED_COMMIT=a051933e2b058d74bb268e94080464569d99ce39

[[ $(git -C "$ROOT/source/FBFM/wam/dreamzero-libero" rev-parse HEAD) == "$EXPECTED_COMMIT" ]]
git -C "$ROOT/source/FBFM/wam/dreamzero-libero" diff-index --quiet HEAD --
mkdir -p "$RUN/workers" "$RUN/shards"

for gpu in $(seq 0 7); do
  apps=$(nvidia-smi --id="$gpu" --query-compute-apps=pid --format=csv,noheader | sed '/^$/d' | wc -l)
  memory=$(nvidia-smi --id="$gpu" --query-gpu=memory.used --format=csv,noheader,nounits)
  if (( apps != 0 || memory >= 1024 )); then
    echo "refusing launch: GPU $gpu is busy (apps=$apps memory_mib=$memory)" >&2
    exit 10
  fi
done

for port in $(seq 19000 19007); do
  if ss -ltnH | awk '{print $4}' | grep -Eq "[:.]${port}$"; then
    echo "refusing launch: TCP port $port is already listening" >&2
    exit 11
  fi
done

for gpu in $(seq 0 7); do
  port=$((19000 + gpu))
  worker="$RUN/workers/gpu$gpu"
  mkdir -p "$worker"
  nohup setsid bash "$ROOT/runtime/run_worker.sh" "$gpu" "$port" formal \
    >"$worker/supervisor.log" 2>&1 </dev/null &
  echo "$!" > "$worker/launcher.pid"
done

nohup setsid bash "$ROOT/runtime/monitor.sh" \
  >"$RUN/monitor-supervisor.log" 2>&1 </dev/null &
echo "$!" > "$RUN/monitor-launcher.pid"
