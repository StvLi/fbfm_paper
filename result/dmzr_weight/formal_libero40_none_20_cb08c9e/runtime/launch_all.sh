#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_none_cb08c9e_20260726
RUN="$ROOT/runs/formal_libero40_none_20_cb08c9e"
mkdir -p "$RUN/workers" "$RUN/shards"

for gpu in $(seq 0 7); do
  apps=$(nvidia-smi --id="$gpu" --query-compute-apps=pid --format=csv,noheader | sed '/^$/d' | wc -l)
  memory=$(nvidia-smi --id="$gpu" --query-gpu=memory.used --format=csv,noheader,nounits)
  if (( apps != 0 || memory >= 1024 )); then
    echo "refusing launch: GPU $gpu is busy (apps=$apps memory_mib=$memory)" >&2
    exit 10
  fi
done

for port in $(seq 18900 18907); do
  if ss -ltnH | awk '{print $4}' | grep -Eq "[:.]${port}$"; then
    echo "refusing launch: TCP port $port is already listening" >&2
    exit 11
  fi
done

for gpu in $(seq 0 7); do
  port=$((18900 + gpu))
  worker="$RUN/workers/gpu$gpu"
  mkdir -p "$worker"
  nohup setsid bash "$ROOT/runtime/run_worker.sh" "$gpu" "$port" \
    >"$worker/supervisor.log" 2>&1 </dev/null &
  echo "$!" > "$worker/launcher.pid"
done

nohup setsid bash "$ROOT/runtime/monitor.sh" \
  >"$RUN/monitor-supervisor.log" 2>&1 </dev/null &
echo "$!" > "$RUN/monitor-launcher.pid"
