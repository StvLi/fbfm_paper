#!/usr/bin/env python3
import json
import os
import time

BASE = "/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs"
CANONICAL = {
    "FBFM": os.path.join(BASE, "feedback_multinode_80cells_clean30_random50_10_a116e48"),
    "NONE": os.path.join(BASE, "base_none_remaining33_clean_random_10_a116e48"),
}
ACCEL = os.path.join(BASE, "formal_accel_12gpu_20260728_a116e48", "runs")

TARGETS = [
    ("FBFM", "demo_clean", "shake_bottle_horizontally", 700),
    ("FBFM", "demo_clean", "put_object_cabinet", 700),
    ("FBFM", "demo_clean", "place_cans_plasticbox", 800),
    ("FBFM", "demo_clean", "handover_block", 800),
    ("FBFM", "demo_clean", "stack_blocks_two", 800),
    ("FBFM", "demo_clean", "place_bread_basket", 700),
    ("FBFM", "demo_clean", "place_object_basket", 700),
    ("FBFM", "demo_randomized", "shake_bottle", 700),
    ("FBFM", "demo_randomized", "put_object_cabinet", 700),
    ("FBFM", "demo_randomized", "place_cans_plasticbox", 800),
    ("FBFM", "demo_randomized", "stack_blocks_two", 800),
    ("FBFM", "demo_randomized", "handover_block", 800),
    ("NONE", "demo_randomized", "put_object_cabinet", 700),
    ("NONE", "demo_randomized", "stack_blocks_two", 800),
    ("NONE", "demo_randomized", "place_object_scale", 400),
]


def result_path(root, config, task):
    return os.path.join(root, config, task, "client", "stseed-10000", "metrics", task, "res.json")


def read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return int(float(data.get("succ_num", 0))), int(float(data.get("total_num", 0)))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
        return 0, 0


rows = []
for mode, config, task, max_steps in TARGETS:
    canonical_path = result_path(CANONICAL[mode], config, task)
    accel_path = result_path(os.path.join(ACCEL, mode), config, task)
    canonical = read(canonical_path)
    accel = read(accel_path)
    if canonical[1] >= 10:
        source, chosen = "canonical", canonical
        path = canonical_path
    elif os.path.exists(accel_path) or os.path.exists(os.path.join(ACCEL, mode, config, task, ".running")):
        source, chosen = "accel", accel
        path = accel_path
    else:
        source, chosen = "canonical-partial", canonical
        path = canonical_path
    running = os.path.exists(os.path.join(ACCEL, mode, config, task, ".running"))
    failed = os.path.exists(os.path.join(ACCEL, mode, config, task, ".failed"))
    age = int(time.time() - os.path.getmtime(path)) if os.path.exists(path) else -1
    rows.append((mode, config, task, max_steps, chosen[0], chosen[1], source, running, failed, age))

complete = sum(total >= 10 for _, _, _, _, _, total, _, _, _, _ in rows)
episodes = sum(min(total, 10) for _, _, _, _, _, total, _, _, _, _ in rows)
success = sum(succ for _, _, _, _, succ, _, _, _, _, _ in rows)
running = sum(is_running for _, _, _, _, _, _, _, is_running, _, _ in rows)
failed = sum(is_failed for _, _, _, _, _, _, _, _, is_failed, _ in rows)
print(f"SUMMARY\tcomplete={complete}/15\tepisodes={episodes}/150\tsuccess={success}\trunning={running}\tfailed={failed}")
for row in rows:
    mode, config, task, max_steps, succ, total, source, is_running, is_failed, age = row
    print(
        f"ROW\t{mode}\t{config}\t{task}\t{max_steps}\t{succ}/{total}\t"
        f"{source}\trunning={int(is_running)}\tfailed={int(is_failed)}\tage_s={age}"
    )
