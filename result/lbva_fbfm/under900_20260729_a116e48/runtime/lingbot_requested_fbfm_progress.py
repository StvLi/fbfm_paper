#!/usr/bin/env python3
import glob
import json
import os

BASE = "/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs"
CANONICAL = os.path.join(BASE, "feedback_multinode_80cells_clean30_random50_10_a116e48")
MAIN = os.path.join(BASE, "formal_accel_12gpu_20260728_a116e48", "runs", "FBFM")
SHARDS = os.path.join(BASE, "formal_under900_shards_20260729_a116e48", "runs", "FBFM")
TASKS = [
    "handover_block",
    "place_cans_plasticbox",
    "stack_blocks_two",
    "open_laptop",
    "place_bread_basket",
    "place_can_basket",
    "place_object_basket",
    "put_object_cabinet",
    "shake_bottle",
    "shake_bottle_horizontally",
    "dump_bin_bigbin",
    "handover_mic",
    "place_dual_shoes",
    "place_bread_skillet",
]


def path(root, config, task, stseed="stseed-10000"):
    return os.path.join(root, config, task, "client", stseed, "metrics", task, "res.json")


def read(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


for config in ("demo_clean", "demo_randomized"):
    for task in TASKS:
        canonical = read(path(CANONICAL, config, task))
        if canonical is not None and int(float(canonical.get("total_num", 0))) == 10:
            succ = int(float(canonical["succ_num"]))
            print(config, task, succ, 10, "complete", sep="\t")
            continue

        candidates = []
        main = read(path(MAIN, config, task))
        if main is not None:
            candidates.append(main)
        for filename in glob.glob(os.path.join(
            SHARDS, config, task, "eval-seed-*", "client", "stseed-*", "metrics", task, "res.json"
        )):
            d = read(filename)
            if d is not None:
                candidates.append(d)
        if not candidates and canonical is not None:
            candidates.append(canonical)

        by_seed = {}
        for d in candidates:
            for episode in d.get("episodes", []):
                seed = int(episode["seed"])
                success = bool(episode["success"])
                if seed in by_seed:
                    assert by_seed[seed] == success
                by_seed[seed] = success
        selected = [by_seed[seed] for seed in sorted(by_seed)[:10]]
        print(config, task, sum(selected), len(selected), "partial" if selected else "not_measured", sep="\t")
