#!/usr/bin/env python3
"""Aggregate and plot the frozen rapid experiment's numeric mechanism evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


TASKS = ("adjust_bottle", "pick_diverse_bottles")
METHODS = ("RTC", "FBFM")
METHOD_COLORS = {"RTC": "#D55E00", "FBFM": "#0072B2"}
SIGNAL_COLOR = "#009E73"
FLOOR_COLOR = "#6B6B6B"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mean(values: Iterable[float]) -> float:
    sequence = list(values)
    if not sequence:
        raise ValueError("cannot average an empty sequence")
    return math.fsum(sequence) / len(sequence)


def exact_sign_test_two_sided(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    tail = min(wins, losses)
    probability = sum(math.comb(n, k) for k in range(tail + 1)) / (2**n)
    return min(1.0, 2.0 * probability)


def enumerated_bootstrap_interval(values: list[float]) -> list[float]:
    if len(values) != 4:
        raise ValueError("the frozen rapid profile must contain exactly four units")
    boot = sorted(mean(sample) for sample in itertools.product(values, repeat=4))
    return [boot[6], boot[249]]


def save_figure(fig: plt.Figure, output_stem: Path) -> None:
    fig.savefig(output_stem.with_suffix(".png"), dpi=240, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def style_axis(axis: plt.Axes) -> None:
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(axis="y", color="#D9D9D9", linewidth=0.6, alpha=0.75)
    axis.tick_params(labelsize=8)


def result_paths(rapid_root: Path) -> dict[tuple[str, str], Path]:
    paths: dict[tuple[str, str], Path] = {}
    for task in TASKS:
        roots = {
            "RTC": rapid_root / "rtc_rerun_paired_v1" / task,
            "FBFM": rapid_root / "formal" / "fbfm" / task,
        }
        for method, root in roots.items():
            paths[(task, method)] = (
                root / "client" / "stseed-10000" / "metrics" / task / "res.json"
            )
    return paths


def cachecut_paths(rapid_root: Path) -> dict[str, Path]:
    return {
        task: rapid_root / "formal" / "fbfm_cachecut" / task / "client"
        / "stseed-10000" / "metrics" / task / "res.json"
        for task in TASKS
    }


def strict_state_analysis(
    aggregate: Path, figures: Path
) -> tuple[dict[str, Any], dict[tuple[str, int, str], float]]:
    source_path = aggregate / "paired_next_slot_latent_mse.csv"
    rows = read_csv(source_path)
    if len(rows) != 8:
        raise ValueError("strict state table must contain 4 units x 2 methods")
    values: dict[tuple[str, int, str], float] = {}
    cosines: dict[tuple[str, int, str], float] = {}
    counts = set()
    for row in rows:
        key = (row["task"], int(row["trial_id"]), row["method"])
        if key in values:
            raise ValueError(f"duplicate strict state key: {key}")
        values[key] = float(row["latent_mse_normalized_space"])
        cosines[key] = float(row["cosine_similarity"])
        counts.add(int(row["selected_count"]))
    if counts != {23040}:
        raise ValueError(f"unexpected latent vector lengths: {counts}")

    units = sorted({(task, trial) for task, trial, _ in values})
    if len(units) != 4:
        raise ValueError("expected exactly four independent state units")
    pair_rows = []
    mse_differences = []
    cosine_differences = []
    for task, trial in units:
        rtc = values[(task, trial, "RTC")]
        fbfm = values[(task, trial, "FBFM")]
        rtc_cos = cosines[(task, trial, "RTC")]
        fbfm_cos = cosines[(task, trial, "FBFM")]
        mse_improvement = rtc - fbfm
        cosine_improvement = fbfm_cos - rtc_cos
        mse_differences.append(mse_improvement)
        cosine_differences.append(cosine_improvement)
        pair_rows.append({
            "task": task,
            "trial_id": trial,
            "rtc_latent_mse": rtc,
            "fbfm_latent_mse": fbfm,
            "absolute_mse_reduction": mse_improvement,
            "relative_mse_reduction": mse_improvement / rtc,
            "rtc_cosine_similarity": rtc_cos,
            "fbfm_cosine_similarity": fbfm_cos,
            "cosine_improvement": cosine_improvement,
            "fbfm_mse_lower": int(fbfm < rtc),
        })
    write_csv(aggregate / "state_pair_differences.csv", pair_rows)

    rtc_mean = mean(values[(task, trial, "RTC")] for task, trial in units)
    fbfm_mean = mean(values[(task, trial, "FBFM")] for task, trial in units)
    wins = sum(diff > 0 for diff in mse_differences)
    losses = sum(diff < 0 for diff in mse_differences)
    state_summary = {
        "independent_units": len(units),
        "selected_latent_values_per_record": next(iter(counts)),
        "rtc_mean_normalized_latent_mse": rtc_mean,
        "fbfm_mean_normalized_latent_mse": fbfm_mean,
        "absolute_mean_mse_reduction": rtc_mean - fbfm_mean,
        "relative_mean_mse_reduction": (rtc_mean - fbfm_mean) / rtc_mean,
        "fbfm_lower_mse_units": wins,
        "fbfm_higher_mse_units": losses,
        "paired_sign_test_two_sided_p": exact_sign_test_two_sided(wins, losses),
        "mean_paired_mse_reduction": mean(mse_differences),
        "enumerated_unit_bootstrap_95pct_interval": enumerated_bootstrap_interval(
            mse_differences
        ),
        "rtc_mean_cosine_similarity": mean(
            cosines[(task, trial, "RTC")] for task, trial in units
        ),
        "fbfm_mean_cosine_similarity": mean(
            cosines[(task, trial, "FBFM")] for task, trial in units
        ),
        "mean_cosine_improvement": mean(cosine_differences),
        "fbfm_higher_cosine_units": sum(diff > 0 for diff in cosine_differences),
    }

    fig, axis = plt.subplots(figsize=(4.5, 3.25))
    for index, (task, trial) in enumerate(units):
        y = [values[(task, trial, method)] for method in METHODS]
        axis.plot([0, 1], y, color="#999999", linewidth=1.0, alpha=0.85, zorder=1)
        axis.scatter([0, 1], y, color=[METHOD_COLORS[m] for m in METHODS], s=28, zorder=2)
        axis.text(1.035, y[1], f"{task.replace('_', ' ')} / {trial}", fontsize=6.5, va="center")
    axis.set_xlim(-0.2, 1.85)
    axis.set_xticks([0, 1], METHODS)
    axis.set_ylabel("Next-state latent MSE", fontsize=9)
    axis.set_title("Paired wave-0 state prediction", fontsize=10)
    style_axis(axis)
    save_figure(fig, figures / "state_mse_paired")
    return state_summary, values


def one_step_wave_analysis(
    rapid_root: Path,
    aggregate: Path,
    figures: Path,
    strict_values: dict[tuple[str, int, str], float],
) -> dict[str, Any]:
    raw_rows: list[dict[str, Any]] = []
    source_files = result_paths(rapid_root)
    for (task, method), path in source_files.items():
        result = read_json(path)
        if result["task_name"] != task or result["method"] != method:
            raise ValueError(f"result identity mismatch: {path}")
        for record in result["causal_aux_records"]:
            resolved = record.get("realized_future_from_previous_wave")
            if not resolved:
                continue
            joined = [status for status in resolved["statuses"] if status["status"] == "joined"]
            if len(joined) != 1 or joined[0]["source"]["branch"] != method:
                raise ValueError("one-step future join is incomplete or belongs to another branch")
            metrics = joined[0]["metrics"]
            raw_rows.append({
                "task": task,
                "trial_id": int(record["trial_id"]),
                "method": method,
                "source_wave_id": int(resolved["source_wave_id"]),
                "realized_wave_id": int(resolved["realized_wave_id"]),
                "latent_mse_normalized_space": float(metrics["normalized_mse"]),
                "cosine_similarity": float(metrics["cosine_similarity"]),
                "selected_count": int(metrics["selected_count"]),
                "strictly_paired_initial_history": int(resolved["source_wave_id"] == 0),
            })
    write_csv(aggregate / "one_step_latent_by_wave.csv", raw_rows)

    keyed = {
        (row["task"], row["trial_id"], row["source_wave_id"], row["method"]): row
        for row in raw_rows
    }
    unit_waves = sorted({(task, trial, wave) for task, trial, wave, _ in keyed})
    if any((task, trial, wave, method) not in keyed for task, trial, wave in unit_waves for method in METHODS):
        raise ValueError("RTC/FBFM one-step wave keys are not fully paired")
    for key, strict in strict_values.items():
        task, trial, method = key
        online = keyed[(task, trial, 0, method)]["latent_mse_normalized_space"]
        if abs(online - strict) > 1e-12:
            raise ValueError("wave-0 online trend disagrees with strict state table")

    summary_rows = []
    waves = sorted({wave for _, _, wave in unit_waves})
    for wave in waves:
        wave_units = [(task, trial) for task, trial, current in unit_waves if current == wave]
        for method in METHODS:
            mse_values = [
                keyed[(task, trial, wave, method)]["latent_mse_normalized_space"]
                for task, trial in wave_units
            ]
            cosine_values = [
                keyed[(task, trial, wave, method)]["cosine_similarity"]
                for task, trial in wave_units
            ]
            summary_rows.append({
                "source_wave_id": wave,
                "method": method,
                "unit_count": len(wave_units),
                "mean_latent_mse": mean(mse_values),
                "min_latent_mse": min(mse_values),
                "max_latent_mse": max(mse_values),
                "mean_cosine_similarity": mean(cosine_values),
            })
    write_csv(aggregate / "one_step_latent_wave_summary.csv", summary_rows)

    direction_count = sum(
        keyed[(task, trial, wave, "FBFM")]["latent_mse_normalized_space"]
        < keyed[(task, trial, wave, "RTC")]["latent_mse_normalized_space"]
        for task, trial, wave in unit_waves
    )
    differences = [
        keyed[(task, trial, wave, "RTC")]["latent_mse_normalized_space"]
        - keyed[(task, trial, wave, "FBFM")]["latent_mse_normalized_space"]
        for task, trial, wave in unit_waves
    ]
    trend_summary = {
        "paired_unit_waves": len(unit_waves),
        "source_wave_range": [min(waves), max(waves)],
        "strictly_paired_wave0_units": sum(wave == 0 for _, _, wave in unit_waves),
        "post_wave0_scope": "descriptive own-trajectory one-step prediction; histories have diverged",
        "fbfm_lower_mse_unit_waves": direction_count,
        "rtc_lower_mse_unit_waves": len(unit_waves) - direction_count,
        "mean_rtc_minus_fbfm_mse_all_unit_waves": mean(differences),
    }

    fig, axis = plt.subplots(figsize=(5.3, 3.25))
    for method in METHODS:
        method_rows = [row for row in summary_rows if row["method"] == method]
        x = np.array([row["source_wave_id"] for row in method_rows])
        y = np.array([row["mean_latent_mse"] for row in method_rows])
        low = np.array([row["min_latent_mse"] for row in method_rows])
        high = np.array([row["max_latent_mse"] for row in method_rows])
        axis.plot(x, y, marker="o", markersize=3, linewidth=1.5, label=method, color=METHOD_COLORS[method])
        axis.fill_between(x, low, high, color=METHOD_COLORS[method], alpha=0.08, linewidth=0)
    axis.axvline(0.5, color="#555555", linewidth=0.8, linestyle="--")
    axis.text(0.65, 0.96, "wave > 0: own trajectories", transform=axis.get_xaxis_transform(), fontsize=7, va="top")
    axis.set_xlabel("Source wave", fontsize=9)
    axis.set_ylabel("One-step latent MSE", fontsize=9)
    axis.set_title("One-step prediction over rollout waves", fontsize=10)
    axis.legend(frameon=False, fontsize=8, ncol=2)
    style_axis(axis)
    save_figure(fig, figures / "one_step_latent_trend")
    return trend_summary


def rgb_sensitivity_analysis(aggregate: Path, figures: Path) -> dict[str, Any]:
    source_rows = read_csv(aggregate / "wave0_future_frame_mse.csv")
    if len(source_rows) != 96:
        raise ValueError("RGB sensitivity table must contain 96 camera-frame rows")
    grouped: dict[tuple[str, int, str, int], list[float]] = defaultdict(list)
    for row in source_rows:
        grouped[(
            row["task"], int(row["trial_id"]), row["method"], int(row["horizon"])
        )].append(float(row["rgb_mse_0_1"]))
    if any(len(values) != 3 for values in grouped.values()):
        raise ValueError("each RGB unit/horizon must contain exactly three cameras")
    unit_rows = [
        {
            "task": key[0],
            "trial_id": key[1],
            "method": key[2],
            "horizon_frame": key[3],
            "equal_camera_mean_rgb_mse": mean(values),
        }
        for key, values in sorted(grouped.items())
    ]
    write_csv(aggregate / "rgb_horizon_unit_means.csv", unit_rows)

    summary_rows = []
    for horizon in range(1, 5):
        for method in METHODS:
            values = [
                row["equal_camera_mean_rgb_mse"]
                for row in unit_rows
                if row["horizon_frame"] == horizon and row["method"] == method
            ]
            summary_rows.append({
                "horizon_frame": horizon,
                "method": method,
                "independent_units": len(values),
                "mean_equal_camera_rgb_mse": mean(values),
                "min_unit_rgb_mse": min(values),
                "max_unit_rgb_mse": max(values),
            })
    write_csv(aggregate / "rgb_horizon_summary.csv", summary_rows)
    keyed = {
        (row["task"], row["trial_id"], row["method"], row["horizon_frame"]): row[
            "equal_camera_mean_rgb_mse"
        ]
        for row in unit_rows
    }
    unit_horizons = sorted({(task, trial, horizon) for task, trial, _, horizon in keyed})
    fbfm_lower = sum(
        keyed[(task, trial, "FBFM", horizon)] < keyed[(task, trial, "RTC", horizon)]
        for task, trial, horizon in unit_horizons
    )
    sensitivity_summary = {
        "independent_units": 4,
        "frames_per_next_state_slot": 4,
        "cameras_per_frame": 3,
        "unit_horizons": len(unit_horizons),
        "fbfm_lower_rgb_mse_unit_horizons": fbfm_lower,
        "fbfm_higher_or_equal_rgb_mse_unit_horizons": len(unit_horizons) - fbfm_lower,
        "interpretation": "decoded RGB sensitivity check; not the cache representation metric",
    }

    fig, axis = plt.subplots(figsize=(4.7, 3.2))
    for method in METHODS:
        method_rows = [row for row in summary_rows if row["method"] == method]
        axis.plot(
            [row["horizon_frame"] for row in method_rows],
            [row["mean_equal_camera_rgb_mse"] for row in method_rows],
            marker="o", markersize=4, linewidth=1.5, label=method, color=METHOD_COLORS[method],
        )
    axis.set_xticks([1, 2, 3, 4])
    axis.set_xlabel("Frame within next state slot", fontsize=9)
    axis.set_ylabel("Decoded RGB MSE", fontsize=9)
    axis.set_title("RGB reconstruction sensitivity check", fontsize=10)
    axis.legend(frameon=False, fontsize=8, ncol=2)
    style_axis(axis)
    save_figure(fig, figures / "rgb_frame_horizon_sensitivity")
    return sensitivity_summary


def action_analysis(rapid_root: Path, aggregate: Path, figures: Path) -> dict[str, Any]:
    probe_rows: list[dict[str, Any]] = []
    curve_raw: list[dict[str, Any]] = []
    for task, path in cachecut_paths(rapid_root).items():
        result = read_json(path)
        if result["task_name"] != task or result["method"] != "FBFM-CacheCut":
            raise ValueError(f"CacheCut identity mismatch: {path}")
        for record in result["causal_aux_records"]:
            if not record["probe_enabled"]:
                continue
            if record["D_cut"] != record["D_repeat"]:
                raise ValueError("D_cut no longer equals its selected-branch repeat floor")
            signal = float(record["D_action"]["normalized_rms"])
            floor = float(record["D_repeat"]["normalized_rms"])
            velocity = record["velocity_differences"]
            repeat_velocity = record["repeat_velocity_differences"]
            if len(velocity) != 51 or len(repeat_velocity) != 51:
                raise ValueError("expected 51 paired action denoising solver steps")
            if int(record["D_action"]["selected_count"]) != 256:
                raise ValueError("unexpected fresh action mask size")
            probe_rows.append({
                "task": task,
                "trial_id": int(record["trial_id"]),
                "wave_id": int(record["wave_id"]),
                "branch_action_step": int(record["branch_action_step"]),
                "fresh_action_values": int(record["D_action"]["selected_count"]),
                "cache_branch_action_rms": signal,
                "repeat_floor_action_rms": floor,
                "signal_to_repeat_ratio": signal / floor,
                "rtc_cache_conditioned_action_sha256": record["action_branches"]["RTC"]["action_sha256"],
                "fbfm_cache_conditioned_action_sha256": record["action_branches"]["FBFM"]["action_sha256"],
                "invariant_status": "passed",
            })
            for step, (signal_step, floor_step) in enumerate(zip(velocity, repeat_velocity)):
                curve_raw.append({
                    "task": task,
                    "trial_id": int(record["trial_id"]),
                    "wave_id": int(record["wave_id"]),
                    "denoising_solver_step": step,
                    "cache_branch_velocity_rms": float(signal_step["normalized_rms"]),
                    "repeat_floor_velocity_rms": float(floor_step["normalized_rms"]),
                })
    if len(probe_rows) != 8 or len(curve_raw) != 8 * 51:
        raise ValueError("the frozen action mechanism profile must contain 8 x 51 rows")
    write_csv(aggregate / "action_probe_metrics.csv", probe_rows)
    write_csv(aggregate / "action_denoising_probe_raw.csv", curve_raw)

    unit_probe_rows: list[dict[str, Any]] = []
    units = sorted({(row["task"], row["trial_id"]) for row in probe_rows})
    if len(units) != 4:
        raise ValueError("expected four independent CacheCut units")
    for task, trial in units:
        records = [row for row in probe_rows if row["task"] == task and row["trial_id"] == trial]
        if len(records) != 2:
            raise ValueError("each CacheCut unit must contain two repeated probes")
        signal = mean(row["cache_branch_action_rms"] for row in records)
        floor = mean(row["repeat_floor_action_rms"] for row in records)
        unit_probe_rows.append({
            "task": task,
            "trial_id": trial,
            "probe_count": 2,
            "mean_cache_branch_action_rms": signal,
            "mean_repeat_floor_action_rms": floor,
            "signal_to_repeat_ratio": signal / floor,
        })
    write_csv(aggregate / "action_unit_cluster_means.csv", unit_probe_rows)

    unit_curves: dict[tuple[str, int, int], tuple[float, float]] = {}
    for task, trial in units:
        for step in range(51):
            records = [
                row for row in curve_raw
                if row["task"] == task and row["trial_id"] == trial
                and row["denoising_solver_step"] == step
            ]
            if len(records) != 2:
                raise ValueError("unit-cluster denoising curve has missing repeated probes")
            unit_curves[(task, trial, step)] = (
                mean(row["cache_branch_velocity_rms"] for row in records),
                mean(row["repeat_floor_velocity_rms"] for row in records),
            )
    curve_summary = []
    for step in range(51):
        signal_values = [unit_curves[(task, trial, step)][0] for task, trial in units]
        floor_values = [unit_curves[(task, trial, step)][1] for task, trial in units]
        curve_summary.append({
            "denoising_solver_step": step,
            "independent_units": len(units),
            "mean_cache_branch_velocity_rms": mean(signal_values),
            "min_cache_branch_velocity_rms": min(signal_values),
            "max_cache_branch_velocity_rms": max(signal_values),
            "mean_repeat_floor_velocity_rms": mean(floor_values),
            "min_repeat_floor_velocity_rms": min(floor_values),
            "max_repeat_floor_velocity_rms": max(floor_values),
        })
    write_csv(aggregate / "action_denoising_curve.csv", curve_summary)

    signal_mean = mean(row["mean_cache_branch_action_rms"] for row in unit_probe_rows)
    floor_mean = mean(row["mean_repeat_floor_action_rms"] for row in unit_probe_rows)
    x = np.arange(51, dtype=float)
    signal_curve = np.array([row["mean_cache_branch_velocity_rms"] for row in curve_summary])
    floor_curve = np.array([row["mean_repeat_floor_velocity_rms"] for row in curve_summary])
    signal_auc = float(np.trapz(signal_curve, x))
    floor_auc = float(np.trapz(floor_curve, x))
    action_summary = {
        "independent_task_trial_units": len(units),
        "repeated_probes": len(probe_rows),
        "probes_per_unit": 2,
        "fresh_action_values_per_probe": 256,
        "mean_cache_branch_final_action_rms": signal_mean,
        "mean_repeat_floor_final_action_rms": floor_mean,
        "final_action_signal_to_repeat_ratio_of_means": signal_mean / floor_mean,
        "unit_ratio_range": [
            min(row["signal_to_repeat_ratio"] for row in unit_probe_rows),
            max(row["signal_to_repeat_ratio"] for row in unit_probe_rows),
        ],
        "denoising_solver_steps": 51,
        "cache_branch_velocity_curve_auc": signal_auc,
        "repeat_floor_velocity_curve_auc": floor_auc,
        "velocity_curve_auc_ratio": signal_auc / floor_auc,
        "mean_signal_above_mean_floor_steps": int(np.sum(signal_curve > floor_curve)),
        "peak_mean_cache_branch_velocity_rms": float(np.max(signal_curve)),
        "peak_mean_cache_branch_velocity_step": int(np.argmax(signal_curve)),
    }

    fig, axis = plt.subplots(figsize=(5.2, 3.25))
    axis.plot(x, signal_curve, color=SIGNAL_COLOR, linewidth=1.6, label="RTC vs FBFM cache")
    axis.plot(x, floor_curve, color=FLOOR_COLOR, linewidth=1.4, label="same-branch repeat floor")
    axis.set_xlabel("Action denoising solver step", fontsize=9)
    axis.set_ylabel("Velocity prediction RMS", fontsize=9)
    axis.set_title("Controlled cache intervention during action inference", fontsize=10)
    axis.legend(frameon=False, fontsize=8)
    style_axis(axis)
    save_figure(fig, figures / "action_denoising_curve")
    return action_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rapid-root", type=Path, required=True)
    parser.add_argument("--numeric-root", type=Path, required=True)
    args = parser.parse_args()
    aggregate = args.numeric_root / "aggregate"
    figures = args.numeric_root / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    state_integrity = read_csv(aggregate / "state_integrity.csv")
    if len(state_integrity) != 8 or any(row["status"] != "passed" for row in state_integrity):
        raise ValueError("strict state tensor integrity did not pass")
    state, strict_values = strict_state_analysis(aggregate, figures)
    trend = one_step_wave_analysis(args.rapid_root, aggregate, figures, strict_values)
    rgb = rgb_sensitivity_analysis(aggregate, figures)
    action = action_analysis(args.rapid_root, aggregate, figures)

    inputs = [
        aggregate / "paired_next_slot_latent_mse.csv",
        aggregate / "wave0_future_frame_mse.csv",
        aggregate / "state_integrity.csv",
        *result_paths(args.rapid_root).values(),
        *cachecut_paths(args.rapid_root).values(),
    ]
    summary = {
        "schema_version": 1,
        "claim_limit": (
            "Four independent task-by-trial units; wave-0 state comparison is strict. "
            "Later-wave trends are descriptive and RGB is a sensitivity check."
        ),
        "state": state,
        "one_step_trend": trend,
        "rgb_sensitivity": rgb,
        "action": action,
        "input_sha256": {str(path.relative_to(args.rapid_root)): file_sha256(path) for path in inputs},
    }
    summary_path = aggregate / "numeric_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path = args.numeric_root / "artifact_manifest.json"
    artifacts = sorted(
        path for path in args.numeric_root.rglob("*")
        if path.is_file() and path != manifest_path
    )
    manifest = {
        "schema_version": 1,
        "status": "complete",
        "artifact_count": len(artifacts),
        "artifacts": [
            {
                "path": str(path.relative_to(args.numeric_root)),
                "size_bytes": path.stat().st_size,
                "sha256": file_sha256(path),
            }
            for path in artifacts
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    written_manifest = read_json(manifest_path)
    for entry in written_manifest["artifacts"]:
        artifact = args.numeric_root / entry["path"]
        if artifact.stat().st_size != entry["size_bytes"]:
            raise RuntimeError(f"artifact size changed after manifest creation: {artifact}")
        if file_sha256(artifact) != entry["sha256"]:
            raise RuntimeError(f"artifact hash changed after manifest creation: {artifact}")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
