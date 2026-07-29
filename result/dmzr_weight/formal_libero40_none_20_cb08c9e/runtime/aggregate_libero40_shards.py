#!/usr/bin/env python3
"""Atomically aggregate resumable LIBERO worker shards."""

from __future__ import annotations

import argparse
import csv
import io
import json
from datetime import datetime
from pathlib import Path


PROTOCOL_FIELDS = (
    "mode",
    "trials_per_task",
    "environment_seed",
    "model_seed_rule",
    "solver_release_policy",
    "feedback_encoding",
    "state_weight",
    "code_commit",
)


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def atomic_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    atomic_text(path, stream.getvalue())


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--expected-task", action="append", required=True)
    args = parser.parse_args()

    manifests: list[tuple[Path, dict]] = []
    for path in sorted((args.root / "shards").glob("gpu*/manifest.json")):
        manifests.append((path.parent, json.loads(path.read_text(encoding="utf-8"))))
    if not manifests:
        raise ValueError("no shard manifests found")

    reference = manifests[0][1]
    for shard, manifest in manifests[1:]:
        mismatched = [
            field for field in PROTOCOL_FIELDS if manifest.get(field) != reference.get(field)
        ]
        if mismatched:
            raise ValueError(f"protocol mismatch in {shard}: {mismatched}")

    locations: dict[str, Path] = {}
    descriptions: dict[str, str] = {}
    for shard, manifest in manifests:
        summary_path = shard / "task_summary.csv"
        if summary_path.exists():
            with summary_path.open(encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    descriptions[f"{row['suite']}:{row['task_id']}"] = row["task_description"]
        for task_key in manifest["task_keys"]:
            if task_key in locations:
                raise ValueError(f"task assigned to multiple shards: {task_key}")
            locations[task_key] = shard

    expected = list(args.expected_task)
    if set(locations) != set(expected) or len(expected) != len(set(expected)):
        raise ValueError(
            f"shard task set mismatch: expected={expected}, observed={sorted(locations)}"
        )

    target_trials = int(reference["trials_per_task"])
    task_rows: list[dict] = []
    trial_rows: list[dict] = []
    for task_key in expected:
        suite, raw_task_id = task_key.split(":", 1)
        task_id = int(raw_task_id)
        shard = locations[task_key]
        task_dir = shard / "tasks" / suite / f"task_{task_id:03d}"
        records = load_jsonl(task_dir / "episodes.jsonl")
        trial_ids = sorted(int(record["trial_id"]) for record in records)
        if trial_ids != list(range(len(trial_ids))):
            raise ValueError(f"non-contiguous trial prefix in {task_dir}: {trial_ids}")
        successes = sum(bool(record["success"]) for record in records)
        task_rows.append(
            {
                "suite": suite,
                "task_id": task_id,
                "status": "complete" if len(records) == target_trials else (
                    "running" if records else "pending"
                ),
                "trials": len(records),
                "target_trials": target_trials,
                "successes": successes,
                "failures": len(records) - successes,
                "success_rate": successes / len(records) if records else "",
                "task_description": descriptions.get(task_key, ""),
                "shard": shard.name,
            }
        )
        for record in records:
            trial_rows.append(
                {
                    "suite": suite,
                    "task_id": task_id,
                    "trial_id": int(record["trial_id"]),
                    "success": bool(record["success"]),
                    "executed_steps": int(record["executed_steps"]),
                    "elapsed_seconds": float(record["elapsed_seconds"]),
                    "environment_seed": int(record["environment_seed"]),
                    "model_seed": int(record["model_seed"]),
                    "actions_finite": bool(record["actions_finite"]),
                    "trajectory": record["trajectory"],
                }
            )

    episodes = len(trial_rows)
    successes = sum(row["successes"] for row in task_rows)
    complete_tasks = sum(row["status"] == "complete" for row in task_rows)
    summary = {
        "status": "complete" if complete_tasks == len(expected) else "running",
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "mode": reference["mode"],
        "code_commit": reference["code_commit"],
        "tasks": len(expected),
        "complete_tasks": complete_tasks,
        "trials_per_task": target_trials,
        "episodes": episodes,
        "expected_episodes": len(expected) * target_trials,
        "successes": successes,
        "success_rate": successes / episodes if episodes else None,
    }
    atomic_text(args.root / "summary.json", json.dumps(summary, indent=2) + "\n")
    atomic_csv(args.root / "task_summary.csv", task_rows)
    atomic_csv(args.root / "trials.csv", trial_rows)

    lines = [
        "# DreamZero FBFM LIBERO-40",
        "",
        f"Updated: `{summary['updated_at']}`",
        "",
        f"Mode: `{summary['mode']}` | Code: `{summary['code_commit']}`",
        "",
        "| Complete tasks | Episodes | Successes | Micro rate |",
        "| ---: | ---: | ---: | ---: |",
        (
            f"| {complete_tasks}/{len(expected)} | {episodes}/{summary['expected_episodes']} "
            f"| {successes} | "
            f"{(f'{100 * successes / episodes:.2f}%' if episodes else '-')} |"
        ),
        "",
        "Only complete 20/20 task rows are final estimates.",
        "",
    ]
    atomic_text(args.root / "live_status.md", "\n".join(lines))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
