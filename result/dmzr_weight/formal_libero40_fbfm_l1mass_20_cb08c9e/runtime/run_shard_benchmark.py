#!/usr/bin/env python3
"""Run an explicit, resumable shard of the LIBERO-40 benchmark."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROUTE = Path(os.environ["DREAMZERO_FBFM_ROUTE"]).resolve()
sys.path.insert(0, str(ROUTE / "src"))

from dreamzero_fbfm.experiment_ledger import (  # noqa: E402
    TaskSpec,
    load_jsonl,
    task_directory,
    write_tables,
)
from dreamzero_fbfm.settings import DEFAULT_STATE_WEIGHT  # noqa: E402


SUITES = ("libero_spatial", "libero_object", "libero_goal", "libero_10")


def discover_tasks(task_keys: list[str]) -> list[TaskSpec]:
    from libero.libero import benchmark

    registry = benchmark.get_benchmark_dict()
    specs: list[TaskSpec] = []
    seen: set[tuple[str, int]] = set()
    for task_key in task_keys:
        suite_name, separator, raw_task_id = task_key.partition(":")
        if not separator or suite_name not in SUITES:
            raise ValueError(f"invalid task key: {task_key!r}")
        task_id = int(raw_task_id)
        suite = registry[suite_name]()
        if task_id < 0 or task_id >= int(suite.n_tasks):
            raise ValueError(f"task id out of range: {task_key!r}")
        identity = (suite_name, task_id)
        if identity in seen:
            raise ValueError(f"duplicate task key: {task_key!r}")
        seen.add(identity)
        task = suite.get_task(task_id)
        specs.append(TaskSpec(suite_name, task_id, task.language))
    return specs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", action="append", required=True)
    parser.add_argument("--mode", choices=("NONE", "RTC", "FBFM"), default="FBFM")
    parser.add_argument("--state-weight", type=float, default=DEFAULT_STATE_WEIGHT)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--max-steps", type=int, default=480)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--solver-release-policy",
        choices=("uniform", "after_feedback"),
        default="uniform",
    )
    parser.add_argument(
        "--model-seed-rule", choices=("fixed", "trial_offset"), default="fixed"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--tables-only", action="store_true")
    args = parser.parse_args()

    if args.trials <= 0 or args.max_steps <= 0:
        raise ValueError("trials and max-steps must be positive")
    specs = discover_tasks(args.task)
    task_keys = [f"{spec.suite}:{spec.task_id}" for spec in specs]
    suites = list(dict.fromkeys(spec.suite for spec in specs))
    args.output.mkdir(parents=True, exist_ok=True)

    manifest = {
        "benchmark": "LIBERO",
        "mode": args.mode,
        "suites": suites,
        "tasks": len(specs),
        "task_keys": task_keys,
        "trials_per_task": args.trials,
        "expected_episodes": len(specs) * args.trials,
        "max_steps_by_suite": {suite: args.max_steps for suite in suites},
        "horizon_policy": "uniform_480_for_cross_suite_comparison",
        "environment_seed": args.seed,
        "model_seed_rule": args.model_seed_rule,
        "solver_release_policy": args.solver_release_policy,
        "feedback_observation_stride": 1,
        "feedback_encoding": "causal_rolling_past",
        "state_weight": args.state_weight,
        "code_commit": args.code_commit,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    manifest_path = args.output / "manifest.json"
    compared = (
        "mode",
        "suites",
        "tasks",
        "task_keys",
        "trials_per_task",
        "expected_episodes",
        "max_steps_by_suite",
        "model_seed_rule",
        "solver_release_policy",
        "feedback_encoding",
        "state_weight",
        "code_commit",
    )
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if any(existing.get(key) != manifest[key] for key in compared):
            raise ValueError("existing shard manifest does not match requested protocol")
    else:
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

    write_tables(args.output, specs, args.trials, mode=args.mode, code_commit=args.code_commit)
    if args.tables_only:
        return

    for spec in specs:
        directory = task_directory(args.output, spec)
        records = load_jsonl(directory / "episodes.jsonl")
        completed = sorted(int(record["trial_id"]) for record in records)
        if completed != list(range(len(completed))):
            raise ValueError(f"task output is not a resumable prefix: {directory}")
        remaining = args.trials - len(completed)
        if remaining <= 0:
            continue
        directory.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            str(ROUTE / "scripts" / "libero_experiment.py"),
            "--base-workspace",
            str(args.base_workspace),
            "--mode",
            args.mode,
            "--state-weight",
            str(args.state_weight),
            "--suite",
            spec.suite,
            "--task-id",
            str(spec.task_id),
            "--trial-start",
            str(len(completed)),
            "--trials",
            str(remaining),
            "--seed",
            str(args.seed),
            "--max-steps",
            str(args.max_steps),
            "--model-seed-rule",
            args.model_seed_rule,
            "--solver-release-policy",
            args.solver_release_policy,
            "--host",
            args.host,
            "--port",
            str(args.port),
            "--output",
            str(directory),
        ]
        try:
            subprocess.run(command, check=True)
        finally:
            write_tables(
                args.output,
                specs,
                args.trials,
                mode=args.mode,
                code_commit=args.code_commit,
            )


if __name__ == "__main__":
    main()
