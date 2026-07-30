#!/usr/bin/env python3
import fcntl
import glob
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone

BASE = "/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs"
CANONICAL = os.path.join(BASE, "feedback_multinode_80cells_clean30_random50_10_a116e48")
MAIN = os.path.join(BASE, "formal_accel_12gpu_20260728_a116e48", "runs", "FBFM")
SHARDS = os.path.join(BASE, "formal_under900_shards_20260729_a116e48")
LOCK = os.path.join(BASE, "formal_accel_12gpu_20260728_a116e48", ".promotion.lock")
COMMIT = "a116e48d9c8956c7ee66360ae68007bc146abcc3"

TARGETS = [
    ("demo_clean", "put_object_cabinet"),
    ("demo_clean", "handover_block"),
    ("demo_clean", "place_bread_basket"),
    ("demo_clean", "place_object_basket"),
    ("demo_randomized", "put_object_cabinet"),
    ("demo_randomized", "stack_blocks_two"),
    ("demo_randomized", "handover_block"),
]
ALL_TARGETS = TARGETS + [("demo_clean", "stack_blocks_two")]


def result_path(root, config, task, stseed="stseed-10000"):
    return os.path.join(root, config, task, "client", stseed, "metrics", task, "res.json")


def read(path, config, task):
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    assert d["constraint_mode"] == "FBFM", path
    assert d["task_config"] == config, path
    assert d["task"] == task, path
    assert d["code_commit"] == COMMIT, path
    assert len(d.get("episodes", [])) == int(float(d["total_num"])), path
    return d


def canonical_complete(config, task):
    d = read(result_path(CANONICAL, config, task), config, task)
    return d is not None and int(float(d["total_num"])) == 10


def collect(config, task):
    paths = [result_path(MAIN, config, task)]
    paths.extend(glob.glob(os.path.join(
        SHARDS, "runs", "FBFM", config, task, "eval-seed-*", "client",
        "stseed-*", "metrics", task, "res.json"
    )))
    by_seed = {}
    templates = []
    sources = []
    for path in paths:
        d = read(path, config, task)
        if d is None:
            continue
        templates.append(d)
        sources.append({
            "path": path,
            "initial_eval_seed": int(d["initial_eval_seed"]),
            "total_num": int(float(d["total_num"])),
        })
        for episode in d["episodes"]:
            seed = int(episode["seed"])
            normalized = {
                "seed": seed,
                "instruction": str(episode["instruction"]),
                "success": bool(episode["success"]),
            }
            old = by_seed.get(seed)
            if old is not None:
                assert old == normalized, (config, task, seed, old, normalized)
            else:
                by_seed[seed] = normalized
    return by_seed, templates, sources


def promote(config, task, by_seed, templates, sources):
    selected_seeds = sorted(by_seed)[:10]
    selected = [by_seed[seed] for seed in selected_seeds]
    template = templates[0]
    episodes = [dict(episode_index=i, **episode) for i, episode in enumerate(selected)]
    succ = sum(int(episode["success"]) for episode in episodes)
    result = {
        "succ_num": float(succ),
        "total_num": 10.0,
        "succ_rate": float(succ / 10.0),
        "task": task,
        "task_config": config,
        "constraint_mode": "FBFM",
        "initial_eval_seed": 10000,
        "accepted_seeds": selected_seeds,
        "episodes": episodes,
        "code_commit": COMMIT,
        "checkpoint": template["checkpoint"],
        "video_guidance_scale": float(template["video_guidance_scale"]),
        "action_guidance_scale": float(template["action_guidance_scale"]),
        "sharded_evaluation": True,
    }

    merge_parent = os.path.join(SHARDS, "merged_work")
    os.makedirs(merge_parent, exist_ok=True)
    temp_root = tempfile.mkdtemp(prefix=f"{config}.{task}.", dir=merge_parent)
    out = result_path(temp_root, "", task).replace(os.sep + os.sep, os.sep)
    # result_path expects config/task; build the canonical task-relative layout directly.
    out = os.path.join(temp_root, "client", "stseed-10000", "metrics", task, "res.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "FBFM",
        "config": config,
        "task": task,
        "selected_seeds": selected_seeds,
        "sources": sources,
    }
    with open(os.path.join(temp_root, "merge_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    os.makedirs(os.path.dirname(LOCK), exist_ok=True)
    with open(LOCK, "a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        if canonical_complete(config, task):
            shutil.rmtree(temp_root)
            return False
        canonical_root = os.path.join(CANONICAL, config, task)
        if os.path.exists(canonical_root):
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive = f"{canonical_root}.interrupted.{stamp}.under900-shard-merge"
            os.replace(canonical_root, archive)
        os.makedirs(os.path.dirname(canonical_root), exist_ok=True)
        os.replace(temp_root, canonical_root)
        with open(os.path.join(SHARDS, "promotions.tsv"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()}\tFBFM\t{config}\t{task}\t{succ}/10\tshard_merge\n")
    return True


for config, task in TARGETS:
    if canonical_complete(config, task):
        continue
    by_seed, templates, sources = collect(config, task)
    print(f"CELL\t{config}\t{task}\tunique={len(by_seed)}")
    if len(by_seed) >= 10:
        changed = promote(config, task, by_seed, templates, sources)
        if changed:
            print(f"PROMOTED\t{config}\t{task}")

remaining = sum(not canonical_complete(config, task) for config, task in ALL_TARGETS)
print(f"REMAINING\t{remaining}")
