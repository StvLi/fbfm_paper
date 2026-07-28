#!/usr/bin/env python3
"""Validate complete live chunks against the cb08c9e stride-3 protocol."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


EXPECTED_CONTEXT_VERSIONS = [0, 0, 1, 1, 1, 2, 2, 2]
EXPECTED_TARGET_UPDATES = [0, 0, 1, 0, 0, 1, 0, 0]
EXPECTED_FEEDBACK_OFFSETS = [[], [], [3], [], [], [6], [], []]
EXPECTED_FEEDBACK_SLOTS = [[], [], [0], [], [], [0], [], []]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit", type=Path)
    parser.add_argument("--minimum-complete-chunks", type=int, default=1)
    args = parser.parse_args()

    records = [
        json.loads(line)
        for line in args.audit.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    errors = [
        record
        for record in records
        if "error" in str(record.get("event", "")).lower()
    ]
    if errors:
        raise AssertionError(f"server error records found: {errors[-3:]}")

    chunks: list[dict] = []
    current: dict | None = None
    for record in records:
        if record.get("event") == "chunk_begin":
            current = {"begin": record, "steps": []}
            chunks.append(current)
        elif record.get("event") == "solver_step" and current is not None:
            current["steps"].append(record)

    async_chunks = [chunk for chunk in chunks if chunk["begin"].get("pseudo_async")]
    if any(len(chunk["steps"]) > 8 for chunk in async_chunks):
        raise AssertionError("an async chunk contains more than eight native DiT evaluations")
    complete = [chunk for chunk in async_chunks if len(chunk["steps"]) == 8]
    if len(complete) < args.minimum_complete_chunks:
        raise AssertionError(f"too few complete async chunks: {len(complete)}")

    state_action_corrections: list[float] = []
    for index, chunk in enumerate(complete):
        steps = chunk["steps"]
        for step in steps:
            for key, value in step.items():
                if isinstance(value, float) and not math.isfinite(value):
                    raise AssertionError(f"chunk {index}: non-finite {key}")
            if step.get("mode") != "FBFM":
                raise AssertionError(f"chunk {index}: mode is not FBFM")
            if step.get("action_mask_nonzero") != 56 or not step.get("guided"):
                raise AssertionError(f"chunk {index}: invalid action guidance")

        actual_versions = [step.get("context_version") for step in steps]
        actual_updates = [step.get("state_target_updates") for step in steps]
        actual_offsets = [step.get("feedback_action_offsets") for step in steps]
        actual_slots = [step.get("feedback_state_slots") for step in steps]
        if actual_versions != EXPECTED_CONTEXT_VERSIONS:
            raise AssertionError(
                f"chunk {index}: context versions {actual_versions} do not match stride-3"
            )
        if actual_updates != EXPECTED_TARGET_UPDATES:
            raise AssertionError(f"chunk {index}: state target updates {actual_updates}")
        if actual_offsets != EXPECTED_FEEDBACK_OFFSETS:
            raise AssertionError(f"chunk {index}: feedback offsets {actual_offsets}")
        if actual_slots != EXPECTED_FEEDBACK_SLOTS:
            raise AssertionError(f"chunk {index}: feedback slots {actual_slots}")
        if [int(step.get("state_mask_nonzero", 0) > 0) for step in steps] != [
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
        ]:
            raise AssertionError(f"chunk {index}: invalid active state-mask cadence")
        state_action_corrections.extend(
            float(step["action_correction_norm"])
            for step in steps
            if step.get("state_mask_nonzero", 0) > 0
        )

    if not any(value > 0 for value in state_action_corrections):
        raise AssertionError("state feedback produced no action-coordinate correction")

    print(
        json.dumps(
            {
                "status": "ok",
                "protocol": "cb08c9e_stride3_l1mass",
                "complete_async_chunks": len(complete),
                "solver_steps_checked": len(complete) * 8,
                "server_errors": 0,
                "max_state_to_action_correction": max(state_action_corrections),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
