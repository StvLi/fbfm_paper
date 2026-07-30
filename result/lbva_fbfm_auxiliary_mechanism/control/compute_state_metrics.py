#!/usr/bin/env python3
"""Compute paired RTC/FBFM state-prediction metrics from frozen rapid outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F

from wan_va.modules.utils import load_vae


CAMERAS = (
    "observation.images.cam_high",
    "observation.images.cam_left_wrist",
    "observation.images.cam_right_wrist",
)
TASKS = ("adjust_bottle", "pick_diverse_bottles")
PROMPT_DIR = re.compile(r"^(?P<prompt>.*)_(?P<stamp>\d{8}_\d{6})$")


def tensor_sha256(tensor: torch.Tensor) -> str:
    digest = hashlib.sha256()
    digest.update(str(tensor.dtype).encode("ascii"))
    digest.update(json.dumps(list(tensor.shape), separators=(",", ":")).encode("ascii"))
    digest.update(tensor.detach().contiguous().view(torch.uint8).cpu().numpy().tobytes())
    return digest.hexdigest()


def prompt_sha256(path: Path) -> str:
    match = PROMPT_DIR.fullmatch(path.name)
    if match is None:
        raise ValueError(f"unexpected debug directory name: {path.name}")
    return hashlib.sha256(match.group("prompt").encode("utf-8")).hexdigest()


def debug_dirs_by_trial(debug_root: Path, result: dict[str, Any]) -> dict[int, Path]:
    trial_by_prompt = {
        row["prompt_sha256"]: int(row["trial_id"])
        for row in result["trial_records"]
    }
    matched = {}
    for path in sorted(item for item in debug_root.iterdir() if item.is_dir()):
        trial_id = trial_by_prompt.get(prompt_sha256(path))
        if trial_id is not None:
            if trial_id in matched:
                raise ValueError(f"duplicate debug directory for trial {trial_id}")
            matched[trial_id] = path
    if set(matched) != {int(row["trial_id"]) for row in result["trial_records"]}:
        raise ValueError(f"debug/trial mapping incomplete under {debug_root}")
    return matched


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def future_outcomes(result: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    outcomes = {}
    for record in result["causal_aux_records"]:
        resolved = record.get("realized_future_from_previous_wave")
        if not resolved:
            continue
        key = (int(record["trial_id"]), int(resolved["source_wave_id"]))
        joined = [row for row in resolved["statuses"] if row["status"] == "joined"]
        if len(joined) != 1:
            raise ValueError(f"unexpected realized-future status for {key}")
        outcomes[key] = joined[0]
    return outcomes


def denormalize_latent(latent: torch.Tensor, vae: torch.nn.Module) -> torch.Tensor:
    mean = torch.tensor(
        vae.config.latents_mean, device=latent.device, dtype=latent.dtype
    ).view(1, -1, 1, 1, 1)
    std = torch.tensor(
        vae.config.latents_std, device=latent.device, dtype=latent.dtype
    ).view(1, -1, 1, 1, 1)
    return latent * std + mean


@torch.no_grad()
def decode_views(latent: torch.Tensor, vae: torch.nn.Module) -> dict[str, torch.Tensor]:
    parts = {
        CAMERAS[0]: latent[:, :, :, 8:, :],
        CAMERAS[1]: latent[:, :, :, :8, :10],
        CAMERAS[2]: latent[:, :, :, :8, 10:],
    }
    decoded = {}
    for camera, part in parts.items():
        video = vae.decode(denormalize_latent(part, vae), return_dict=False)[0]
        decoded[camera] = ((video.float() + 1.0) / 2.0).clamp(0.0, 1.0).cpu()
    return decoded


def ground_truth_views(observations: list[dict[str, np.ndarray]]) -> dict[str, torch.Tensor]:
    targets = {}
    for camera_index, camera in enumerate(CAMERAS):
        height, width = ((256, 320) if camera_index == 0 else (128, 160))
        video = torch.from_numpy(np.stack([frame[camera] for frame in observations]))
        video = video.float().permute(3, 0, 1, 2) / 255.0
        targets[camera] = F.interpolate(
            video, size=(height, width), mode="bilinear", align_corners=False
        ).unsqueeze(0)
    return targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rapid-root", type=Path, required=True)
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()

    device = torch.device(args.device)
    dtype = torch.bfloat16
    vae = load_vae(args.model_root / "vae", torch_dtype=dtype, torch_device=device)
    vae.eval()

    state_rows: list[dict[str, Any]] = []
    frame_rows: list[dict[str, Any]] = []
    integrity_rows: list[dict[str, Any]] = []

    for task in TASKS:
        method_roots = {
            "RTC": args.rapid_root / "rtc_rerun_paired_v1" / task,
            "FBFM": args.rapid_root / "formal" / "fbfm" / task,
        }
        for method, method_root in method_roots.items():
            result_path = (
                method_root / "client" / "stseed-10000" / "metrics" / task / "res.json"
            )
            result = json.loads(result_path.read_text(encoding="utf-8"))
            debug_dirs = debug_dirs_by_trial(method_root / "server_debug" / "real", result)
            outcomes = future_outcomes(result)
            source_records = {
                int(row["trial_id"]): row
                for row in result["causal_aux_records"]
                if int(row["wave_id"]) == 0
            }
            for trial_id, debug_dir in sorted(debug_dirs.items()):
                source_record = source_records[trial_id]
                frame_st_id = int(source_record["wave_frame_st_id"])
                outcome = outcomes[(trial_id, 0)]
                if outcome["source"]["branch"] != method:
                    raise RuntimeError(f"executed branch mismatch for {task}/{trial_id}/{method}")
                metrics = outcome["metrics"]
                state_rows.append({
                    "task": task,
                    "trial_id": trial_id,
                    "wave_id": 0,
                    "method": method,
                    "latent_mse_normalized_space": float(metrics["normalized_mse"]),
                    "cosine_similarity": float(metrics["cosine_similarity"]),
                    "selected_count": int(metrics["selected_count"]),
                })

                latent = torch.load(
                    debug_dir / f"latents_{frame_st_id}.pt",
                    map_location="cpu",
                    weights_only=True,
                )
                source_slot = latent[0, :, 1, :, :].reshape(-1)
                source_hash = tensor_sha256(source_slot)
                if source_hash != outcome["source"]["tensor_sha256"]:
                    raise RuntimeError(f"source hash mismatch for {task}/{trial_id}/{method}")
                full_hash = tensor_sha256(latent)
                expected_full = source_record["video_branches"][method]["video_final_sha256"]
                if full_hash != expected_full:
                    raise RuntimeError(f"full latent mismatch for {task}/{trial_id}/{method}")
                integrity_rows.append({
                    "task": task,
                    "trial_id": trial_id,
                    "wave_id": 0,
                    "method": method,
                    "prediction_sha256": source_hash,
                    "target_sha256": outcome["realized"]["tensor_sha256"],
                    "full_latent_sha256": full_hash,
                    "status": "passed",
                })

                observations = torch.load(
                    debug_dir / f"obs_data_{frame_st_id}.pt",
                    map_location="cpu",
                    weights_only=False,
                )
                ground_truth = ground_truth_views(observations)
                predicted = decode_views(latent.to(device=device, dtype=dtype), vae)
                for camera in CAMERAS:
                    if predicted[camera].shape[2] != 5:
                        raise ValueError(
                            f"expected five decoded frames, got {predicted[camera].shape}"
                        )
                    for horizon in range(1, 5):
                        mse = float((
                            predicted[camera][:, :, horizon]
                            - ground_truth[camera][:, :, horizon - 1]
                        ).square().mean().item())
                        frame_rows.append({
                            "task": task,
                            "trial_id": trial_id,
                            "wave_id": 0,
                            "method": method,
                            "horizon": horizon,
                            "camera": camera,
                            "rgb_mse_0_1": mse,
                        })

    write_csv(args.output_root / "paired_next_slot_latent_mse.csv", state_rows)
    write_csv(args.output_root / "wave0_future_frame_mse.csv", frame_rows)
    write_csv(args.output_root / "state_integrity.csv", integrity_rows)
    summary = {
        "schema_version": 1,
        "paired_probe_count": len(state_rows) // 2,
        "independent_task_trial_units": len({(row["task"], row["trial_id"]) for row in state_rows}),
        "wave0_frame_units": len({(row["task"], row["trial_id"]) for row in frame_rows}),
        "state_integrity_passed": all(row["status"] == "passed" for row in integrity_rows),
    }
    (args.output_root / "state_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
