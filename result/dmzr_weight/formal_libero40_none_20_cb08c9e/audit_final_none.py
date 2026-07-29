#!/usr/bin/env python3
"""Independently audit and report the completed DreamZero NONE LIBERO-40 run."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SUITES = ("libero_spatial", "libero_object", "libero_goal", "libero_10")
EXPECTED_COMMIT = "cb08c9e552730d26cc446885e79a3e270a270d0c"
EXPECTED_TRIALS = tuple(range(20))


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    atomic_text(path, stream.getvalue())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.run_root.resolve()

    expected_keys = [(suite, task_id) for suite in SUITES for task_id in range(10)]
    expected_key_set = set(expected_keys)
    manifest_paths = sorted((root / "shards").glob("gpu*/manifest.json"))
    check(len(manifest_paths) == 8, f"expected 8 manifests, found {len(manifest_paths)}")

    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in manifest_paths]
    assigned: list[tuple[str, int]] = []
    for path, manifest in zip(manifest_paths, manifests):
        check(manifest.get("benchmark") == "LIBERO", f"benchmark mismatch: {path}")
        check(manifest.get("mode") == "NONE", f"mode mismatch: {path}")
        check(manifest.get("code_commit") == EXPECTED_COMMIT, f"commit mismatch: {path}")
        check(manifest.get("trials_per_task") == 20, f"trial count mismatch: {path}")
        check(manifest.get("expected_episodes") == 100, f"episode count mismatch: {path}")
        check(manifest.get("tasks") == 5, f"task count mismatch: {path}")
        check(manifest.get("environment_seed") == 0, f"environment seed mismatch: {path}")
        check(manifest.get("model_seed_rule") == "fixed", f"model seed rule mismatch: {path}")
        check(manifest.get("solver_release_policy") == "uniform", f"solver policy mismatch: {path}")
        check(
            manifest.get("max_steps_by_suite") == {suite: 480 for suite in SUITES},
            f"horizon mismatch: {path}",
        )
        for raw_key in manifest["task_keys"]:
            suite, raw_task_id = raw_key.split(":", 1)
            assigned.append((suite, int(raw_task_id)))
    check(len(assigned) == 40, f"expected 40 assigned tasks, found {len(assigned)}")
    check(len(set(assigned)) == 40, "duplicate task assignment in manifests")
    check(set(assigned) == expected_key_set, "manifest task coverage mismatch")

    records: list[dict[str, Any]] = []
    task_rows: list[dict[str, Any]] = []
    ledger_digest = hashlib.sha256()
    trajectory_missing: list[str] = []
    trajectory_empty: list[str] = []

    for suite, task_id in expected_keys:
        candidates = list(
            (root / "shards").glob(
                f"gpu*/tasks/{suite}/task_{task_id:03d}/episodes.jsonl"
            )
        )
        check(len(candidates) == 1, f"expected one ledger for {suite}:{task_id}, found {len(candidates)}")
        path = candidates[0]
        raw_lines = path.read_bytes().splitlines()
        check(len(raw_lines) == 20, f"expected 20 rows in {path}, found {len(raw_lines)}")
        ledger_digest.update(str(path.relative_to(root)).encode("ascii"))
        ledger_digest.update(b"\0")
        task_records: list[dict[str, Any]] = []
        for line_number, raw_line in enumerate(raw_lines, 1):
            ledger_digest.update(raw_line)
            ledger_digest.update(b"\n")
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON in {path}:{line_number}: {error}") from error
            check(record.get("suite") == suite, f"suite mismatch in {path}:{line_number}")
            check(record.get("task_id") == task_id, f"task mismatch in {path}:{line_number}")
            check(record.get("status") == "ok", f"non-ok status in {path}:{line_number}")
            check(record.get("mode") == "NONE", f"non-NONE mode in {path}:{line_number}")
            check(record.get("actions_finite") is True, f"non-finite action in {path}:{line_number}")
            check(type(record.get("success")) is bool, f"invalid success flag in {path}:{line_number}")
            check(record.get("environment_seed") == 0, f"environment seed mismatch in {path}:{line_number}")
            check(record.get("model_seed") == 0, f"model seed mismatch in {path}:{line_number}")
            check(0 < int(record.get("executed_steps", 0)) <= 480, f"invalid steps in {path}:{line_number}")
            check(float(record.get("elapsed_seconds", 0)) > 0, f"invalid elapsed time in {path}:{line_number}")
            protocol = record.get("protocol", {})
            check(protocol.get("max_steps") == 480, f"protocol horizon mismatch in {path}:{line_number}")
            check(protocol.get("model_seed_rule") == "fixed", f"protocol model seed mismatch in {path}:{line_number}")
            check(protocol.get("solver_release_policy") == "uniform", f"protocol solver mismatch in {path}:{line_number}")
            trajectory = Path(record["trajectory"])
            if not trajectory.is_file():
                trajectory_missing.append(str(trajectory))
            elif trajectory.stat().st_size == 0:
                trajectory_empty.append(str(trajectory))
            record["_ledger"] = str(path.relative_to(root))
            task_records.append(record)
            records.append(record)
        trial_ids = [int(record["trial_id"]) for record in task_records]
        check(trial_ids == list(EXPECTED_TRIALS), f"trial IDs mismatch in {path}: {trial_ids}")
        descriptions = {str(record["task_description"]) for record in task_records}
        check(len(descriptions) == 1, f"description mismatch in {path}")
        successes = sum(record["success"] for record in task_records)
        task_rows.append(
            {
                "suite": suite,
                "task_id": task_id,
                "successes": successes,
                "trials": 20,
                "failures": 20 - successes,
                "success_rate": f"{successes / 20:.6f}",
                "success_rate_percent": f"{successes * 5:.2f}",
                "task_description": descriptions.pop(),
                "shard": path.parts[-5],
            }
        )

    check(not trajectory_missing, f"missing trajectories: {trajectory_missing[:10]}")
    check(not trajectory_empty, f"empty trajectories: {trajectory_empty[:10]}")
    identity_counts = Counter(
        (record["suite"], int(record["task_id"]), int(record["trial_id"]))
        for record in records
    )
    check(len(records) == 800, f"expected 800 records, found {len(records)}")
    check(len(identity_counts) == 800, f"expected 800 unique identities, found {len(identity_counts)}")
    check(all(count == 1 for count in identity_counts.values()), "duplicate trial identity")

    overall_successes = sum(record["success"] for record in records)
    suite_successes: dict[str, int] = defaultdict(int)
    suite_trials: dict[str, int] = defaultdict(int)
    for record in records:
        suite = str(record["suite"])
        suite_trials[suite] += 1
        suite_successes[suite] += bool(record["success"])

    suite_rows: list[dict[str, Any]] = []
    for suite in SUITES:
        successes = suite_successes[suite]
        trials = suite_trials[suite]
        suite_rows.append(
            {
                "suite": suite,
                "tasks": 10,
                "successes": successes,
                "trials": trials,
                "failures": trials - successes,
                "success_rate": f"{successes / trials:.6f}",
                "success_rate_percent": f"{100 * successes / trials:.3f}",
            }
        )
    overall_rows = [
        {
            "mode": "NONE",
            "tasks": 40,
            "successes": overall_successes,
            "trials": 800,
            "failures": 800 - overall_successes,
            "success_rate": f"{overall_successes / 800:.6f}",
            "success_rate_percent": f"{100 * overall_successes / 800:.3f}",
            "code_commit": EXPECTED_COMMIT,
        }
    ]

    summary_path = root / "summary.json"
    aggregate_task_path = root / "task_summary.csv"
    aggregate_trials_path = root / "trials.csv"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    check(summary.get("status") == "complete", "atomic summary is not complete")
    check(summary.get("episodes") == 800, "atomic summary episode mismatch")
    check(summary.get("successes") == overall_successes, "atomic summary success mismatch")
    check(summary.get("complete_tasks") == 40, "atomic summary task mismatch")
    check(summary.get("mode") == "NONE", "atomic summary mode mismatch")
    check(summary.get("code_commit") == EXPECTED_COMMIT, "atomic summary commit mismatch")

    aggregate_tasks = load_csv(aggregate_task_path)
    aggregate_trials = load_csv(aggregate_trials_path)
    check(len(aggregate_tasks) == 40, "task_summary.csv row count mismatch")
    check(all(row["status"] == "complete" and row["trials"] == "20" for row in aggregate_tasks), "task_summary.csv completion mismatch")
    check(sum(int(row["successes"]) for row in aggregate_tasks) == overall_successes, "task_summary.csv success mismatch")
    check(len(aggregate_trials) == 800, "trials.csv row count mismatch")
    check(sum(row["success"] == "True" for row in aggregate_trials) == overall_successes, "trials.csv success mismatch")
    check(all(row["actions_finite"] == "True" for row in aggregate_trials), "trials.csv finite-action mismatch")

    audit = {
        "audit_status": "passed",
        "audited_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "run_root": str(root),
        "mode": "NONE",
        "code_commit": EXPECTED_COMMIT,
        "manifests": 8,
        "task_assignments": 40,
        "unique_task_assignments": 40,
        "tasks": 40,
        "trials_per_task": 20,
        "episodes": 800,
        "unique_trial_identities": 800,
        "duplicates": 0,
        "missing_trials": 0,
        "malformed_json_rows": 0,
        "non_ok_rows": 0,
        "non_none_rows": 0,
        "non_finite_action_rows": 0,
        "missing_trajectories": 0,
        "empty_trajectories": 0,
        "successes": overall_successes,
        "failures": 800 - overall_successes,
        "success_rate": overall_successes / 800,
        "source_hashes": {
            "ordered_episode_ledgers_sha256": ledger_digest.hexdigest(),
            "summary_json_sha256": sha256_file(summary_path),
            "task_summary_csv_sha256": sha256_file(aggregate_task_path),
            "trials_csv_sha256": sha256_file(aggregate_trials_path),
        },
        "manifest_feedback_encoding": sorted({manifest["feedback_encoding"] for manifest in manifests}),
        "episode_feedback_encoding": sorted({record["protocol"]["feedback_encoding"] for record in records}),
        "feedback_encoding_note": "Feedback encoding and state weight are inert in NONE mode.",
    }

    atomic_csv(root / "final_task_summary.csv", task_rows)
    atomic_csv(root / "final_suite_summary.csv", suite_rows)
    atomic_csv(root / "final_overall_summary.csv", overall_rows)
    atomic_json(root / "final_audit.json", audit)

    report_lines = [
        "# DreamZero NONE LIBERO-40 Final Report",
        "",
        f"Audited: `{audit['audited_at']}`",
        "",
        f"Code: `{EXPECTED_COMMIT}` | Mode: `NONE`",
        "",
        "## Overall",
        "",
        "| Tasks | Trials | Successes | Failures | Success rate |",
        "| ---: | ---: | ---: | ---: | ---: |",
        f"| 40 | 800 | {overall_successes} | {800 - overall_successes} | {100 * overall_successes / 800:.3f}% |",
        "",
        "## Suites",
        "",
        "| Suite | Tasks | Successes | Trials | Success rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    report_lines.extend(
        f"| `{row['suite']}` | 10 | {row['successes']} | {row['trials']} | {row['success_rate_percent']}% |"
        for row in suite_rows
    )
    report_lines.extend(
        [
            "",
            "## Tasks",
            "",
            "| Suite | Task | Successes | Trials | Success rate | Description |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    report_lines.extend(
        f"| `{row['suite']}` | {row['task_id']} | {row['successes']} | 20 | {row['success_rate_percent']}% | {row['task_description']} |"
        for row in task_rows
    )
    report_lines.extend(
        [
            "",
            "## Integrity",
            "",
            "- 800 records and 800 unique `(suite, task_id, trial_id)` identities.",
            "- Exactly 40 tasks with contiguous trial IDs 0-19.",
            "- No duplicate or missing trials; no malformed JSON rows.",
            "- Every record has `status=ok`, `mode=NONE`, and `actions_finite=true`.",
            "- All 800 trajectory files exist and are non-empty.",
            "- Atomic `summary.json`, `task_summary.csv`, and `trials.csv` agree with the independent ledger audit.",
            "",
        ]
    )
    atomic_text(root / "FINAL_REPORT.md", "\n".join(report_lines))

    artifacts = [
        root / "summary.json",
        root / "task_summary.csv",
        root / "trials.csv",
        root / "final_audit.json",
        root / "final_task_summary.csv",
        root / "final_suite_summary.csv",
        root / "final_overall_summary.csv",
        root / "FINAL_REPORT.md",
    ]
    hash_lines = [f"{sha256_file(path)}  {path.name}" for path in artifacts]
    atomic_text(root / "FINAL_SHA256SUMS.txt", "\n".join(hash_lines) + "\n")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
