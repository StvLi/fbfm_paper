#!/usr/bin/env python
"""Build publication-ready FBFM auxiliary-mechanism figures and tables.

The script consumes only frozen artifacts copied into data/source, writes only
inside this visualization package, and does not launch inference.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
from PIL import Image, PngImagePlugin
from scipy.stats import binomtest, spearmanr, t


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"
STYLE = ROOT / "scripts" / "publication.mplstyle"

DERIVED.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

plt.style.use(STYLE)
mpl.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.titleweight": "bold",
        "axes.titlesize": 8,
        "font.size": 8,
        "legend.fontsize": 6.6,
        "svg.hashsalt": "fbfm-aux-visualization-v1",
    }
)

FBFM = "#0072B2"
RTC = "#D55E00"
REPEAT = "#6B7280"
GRID = "#D1D5DB"
UNIT = "#9CA3AF"
BLACK = "#111827"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unit_label(task: str, trial_id: int) -> str:
    short = {
        "adjust_bottle": "Adjust",
        "pick_diverse_bottles": "Pick",
    }[task]
    return f"{short} / T{int(trial_id)}"


def save_figure(fig: plt.Figure, stem: str, title: str) -> None:
    common = {"facecolor": "white", "bbox_inches": "tight", "pad_inches": 0.03}
    fig.savefig(
        FIGURES / f"{stem}.pdf",
        metadata={
            "Title": title,
            "Author": "FBFM experiment analysis",
            "Subject": "Frozen LingBot-VA auxiliary-mechanism results",
            "Keywords": "FBFM, RTC, state feedback, cache intervention",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
        **common,
    )
    png_path = FIGURES / f"{stem}.png"
    png_metadata = {
        "Title": title,
        "Description": "Generated from frozen auxiliary-mechanism artifacts.",
        "Software": f"Matplotlib {mpl.__version__}",
    }
    fig.savefig(
        png_path,
        dpi=600,
        metadata=png_metadata,
        **common,
    )
    # Matplotlib emits RGBA PNGs even with an opaque white background. Convert
    # to explicit RGB for publication workflows that reject alpha channels.
    with Image.open(png_path) as raster:
        rgba = raster.convert("RGBA")
        rgb = Image.new("RGB", rgba.size, "white")
        rgb.paste(rgba, mask=rgba.getchannel("A"))
        png_info = PngImagePlugin.PngInfo()
        for key, value in png_metadata.items():
            png_info.add_text(key, value)
        rgb.save(png_path, dpi=(600, 600), pnginfo=png_info, optimize=True)
    svg_path = FIGURES / f"{stem}.svg"
    fig.savefig(
        svg_path,
        metadata={"Title": title, "Description": "FBFM auxiliary experiment", "Date": None},
        **common,
    )
    # Matplotlib writes path data with trailing spaces on continuation lines.
    # Normalize those generated lines so repository whitespace checks pass and
    # the SVG remains byte-stable across rebuilds.
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    plt.close(fig)


def add_panel_title(ax: plt.Axes, letter: str, title: str, *, y: float | None = None) -> None:
    ax.set_title(f"{letter}  {title}", loc="left", pad=5, y=y)


def exact_spearman_permutation_p(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    observed = float(spearmanr(x, y).statistic)
    permuted = []
    for permutation in itertools.permutations(y.tolist()):
        permuted.append(float(spearmanr(x, permutation).statistic))
    exact_p = float(np.mean(np.abs(permuted) >= abs(observed) - 1e-12))
    return observed, exact_p


state_long = pd.read_csv(SOURCE / "paired_next_slot_latent_mse.csv")
state_pair = pd.read_csv(SOURCE / "state_pair_differences.csv")
one_step = pd.read_csv(SOURCE / "one_step_latent_by_wave.csv")
one_step_summary = pd.read_csv(SOURCE / "one_step_latent_wave_summary.csv")
action_probe = pd.read_csv(SOURCE / "action_probe_metrics.csv")
action_unit = pd.read_csv(SOURCE / "action_unit_cluster_means.csv")
solver_curve = pd.read_csv(SOURCE / "action_denoising_curve.csv")
rgb_unit = pd.read_csv(SOURCE / "rgb_horizon_unit_means.csv")
rgb_summary = pd.read_csv(SOURCE / "rgb_horizon_summary.csv")
with (SOURCE / "numeric_summary.json").open(encoding="utf-8") as handle:
    frozen_summary = json.load(handle)


# Integrity checks: independent units are task-by-trial pairs; probes are not
# treated as independent samples.
state_units = set(zip(state_pair["task"], state_pair["trial_id"], strict=True))
action_units = set(zip(action_unit["task"], action_unit["trial_id"], strict=True))
assert state_units == action_units and len(state_units) == 4
assert len(state_long) == 8 and set(state_long["method"]) == {"RTC", "FBFM"}
assert len(action_probe) == 8 and action_probe["invariant_status"].eq("passed").all()
assert action_probe["fresh_action_values"].eq(256).all()
assert action_unit["probe_count"].eq(2).all()
assert len(solver_curve) == 51 and solver_curve["independent_units"].eq(4).all()
assert state_long["selected_count"].eq(23040).all()

for frame in (state_long, state_pair, action_unit, rgb_unit):
    frame["unit"] = [
        unit_label(task, trial)
        for task, trial in zip(frame["task"], frame["trial_id"], strict=True)
    ]


# Tidy derived state tables.
cache_state_error = state_long.rename(
    columns={
        "latent_mse_normalized_space": "next_state_latent_mse",
        "selected_count": "latent_value_count",
    }
)[
    [
        "unit",
        "task",
        "trial_id",
        "wave_id",
        "method",
        "next_state_latent_mse",
        "cosine_similarity",
        "latent_value_count",
    ]
].copy()
cache_state_error["strict_paired_initial_condition"] = 1
cache_state_error["independent_unit"] = "task_x_trial"
cache_state_error.to_csv(DERIVED / "cache_state_error.csv", index=False)

cache_state_pair_effect = state_pair[
    [
        "unit",
        "task",
        "trial_id",
        "rtc_latent_mse",
        "fbfm_latent_mse",
        "absolute_mse_reduction",
        "relative_mse_reduction",
        "rtc_cosine_similarity",
        "fbfm_cosine_similarity",
        "cosine_improvement",
        "fbfm_mse_lower",
    ]
].copy()
cache_state_pair_effect.to_csv(DERIVED / "cache_state_pair_effect.csv", index=False)


# Tidy derived cache-to-action intervention tables.
cache_action_effect = action_unit.melt(
    id_vars=["unit", "task", "trial_id", "probe_count"],
    value_vars=["mean_repeat_floor_action_rms", "mean_cache_branch_action_rms"],
    var_name="condition",
    value_name="normalized_fresh_action_rms",
)
cache_action_effect["condition"] = cache_action_effect["condition"].map(
    {
        "mean_repeat_floor_action_rms": "same_cache_repeat_floor",
        "mean_cache_branch_action_rms": "rtc_vs_fbfm_cache_switch",
    }
)
cache_action_effect["independent_unit"] = "task_x_trial"
cache_action_effect.to_csv(DERIVED / "cache_action_effect.csv", index=False)

cache_action_unit = action_unit.copy()
cache_action_unit["action_signal_above_repeat_floor"] = (
    cache_action_unit["mean_cache_branch_action_rms"]
    - cache_action_unit["mean_repeat_floor_action_rms"]
)
cache_action_unit.to_csv(DERIVED / "cache_action_unit.csv", index=False)

solver_long = pd.concat(
    [
        solver_curve[
            [
                "denoising_solver_step",
                "independent_units",
                "mean_cache_branch_velocity_rms",
                "min_cache_branch_velocity_rms",
                "max_cache_branch_velocity_rms",
            ]
        ].rename(
            columns={
                "mean_cache_branch_velocity_rms": "mean_velocity_rms",
                "min_cache_branch_velocity_rms": "min_unit_velocity_rms",
                "max_cache_branch_velocity_rms": "max_unit_velocity_rms",
            }
        ).assign(condition="rtc_vs_fbfm_cache_switch"),
        solver_curve[
            [
                "denoising_solver_step",
                "independent_units",
                "mean_repeat_floor_velocity_rms",
                "min_repeat_floor_velocity_rms",
                "max_repeat_floor_velocity_rms",
            ]
        ].rename(
            columns={
                "mean_repeat_floor_velocity_rms": "mean_velocity_rms",
                "min_repeat_floor_velocity_rms": "min_unit_velocity_rms",
                "max_repeat_floor_velocity_rms": "max_unit_velocity_rms",
            }
        ).assign(condition="same_cache_repeat_floor"),
    ],
    ignore_index=True,
)
solver_long.to_csv(DERIVED / "solver_trajectory.csv", index=False)


# The state-action association is exploratory only: n=4 is too small for a
# stable association estimate or a mediation claim.
association = cache_state_pair_effect.merge(
    cache_action_unit,
    on=["unit", "task", "trial_id"],
    validate="one_to_one",
)
association.to_csv(DERIVED / "state_action_association.csv", index=False)


# Reconstruct the normalized per-action-channel diagnostics from the frozen
# CacheCut JSON records, then average two probes within each independent unit.
channel_rows: list[dict[str, object]] = []
for source_json in ("cachecut_adjust_res.json", "cachecut_pick_res.json"):
    with (SOURCE / source_json).open(encoding="utf-8") as handle:
        record_file = json.load(handle)
    for record in record_file["causal_aux_records"]:
        if not record.get("probe_enabled", False):
            continue
        for condition, key in (
            ("rtc_vs_fbfm_cache_switch", "D_action"),
            ("same_cache_repeat_floor", "D_repeat"),
        ):
            for channel in record[key]["per_channel"]:
                channel_rows.append(
                    {
                        "unit": unit_label(record["task_name"], record["trial_id"]),
                        "task": record["task_name"],
                        "trial_id": record["trial_id"],
                        "wave_id": record["wave_id"],
                        "condition": condition,
                        "normalized_action_channel": int(channel["channel"]),
                        "channel_value_count": int(channel["count"]),
                        "channel_rms": float(channel["rms"]),
                    }
                )

action_channel_probe = pd.DataFrame(channel_rows)
assert len(action_channel_probe) == 8 * 2 * 16
assert action_channel_probe["channel_value_count"].eq(16).all()
action_channel_probe.to_csv(DERIVED / "action_channel_probe.csv", index=False)

action_channel_unit = (
    action_channel_probe.groupby(
        ["unit", "task", "trial_id", "condition", "normalized_action_channel"],
        as_index=False,
    )
    .agg(probe_count=("wave_id", "size"), channel_rms=("channel_rms", "mean"))
)
assert action_channel_unit["probe_count"].eq(2).all()
action_channel_unit.to_csv(DERIVED / "action_channel_unit.csv", index=False)

action_channel_summary = (
    action_channel_unit.groupby(["condition", "normalized_action_channel"], as_index=False)
    .agg(
        independent_units=("unit", "size"),
        mean_channel_rms=("channel_rms", "mean"),
        min_unit_channel_rms=("channel_rms", "min"),
        max_unit_channel_rms=("channel_rms", "max"),
    )
)
assert action_channel_summary["independent_units"].eq(4).all()
action_channel_summary.to_csv(DERIVED / "action_channel_summary.csv", index=False)


# Copy tidy sensitivity/trend tables with explicit claim-boundary columns.
one_step_tidy = one_step.rename(
    columns={"latent_mse_normalized_space": "one_step_latent_mse"}
).copy()
one_step_tidy["comparison_scope"] = np.where(
    one_step_tidy["strictly_paired_initial_history"].eq(1),
    "strict_paired_initial_condition",
    "descriptive_own_trajectory",
)
one_step_tidy.to_csv(DERIVED / "one_step_latent_trend.csv", index=False)

rgb_unit.to_csv(DERIVED / "rgb_horizon_unit.csv", index=False)
rgb_summary.to_csv(DERIVED / "rgb_horizon_summary.csv", index=False)


# Recompute every headline value from the copied source tables.
state_means = state_long.groupby("method")["latent_mse_normalized_space"].mean()
rtc_state = float(state_means["RTC"])
fbfm_state = float(state_means["FBFM"])
state_abs = rtc_state - fbfm_state
state_rel = state_abs / rtc_state
paired_state_differences = state_pair["absolute_mse_reduction"].to_numpy()
state_difference_sd = float(np.std(paired_state_differences, ddof=1))
state_difference_se = state_difference_sd / np.sqrt(len(paired_state_differences))
state_difference_t_critical = float(t.ppf(0.975, len(paired_state_differences) - 1))
state_difference_ci_low = state_abs - state_difference_t_critical * state_difference_se
state_difference_ci_high = state_abs + state_difference_t_critical * state_difference_se
sign_p = float(binomtest(4, 4, p=0.5, alternative="two-sided").pvalue)

action_signal = float(action_unit["mean_cache_branch_action_rms"].mean())
repeat_floor = float(action_unit["mean_repeat_floor_action_rms"].mean())
action_ratio = action_signal / repeat_floor

auc_signal = float(
    np.trapz(
        solver_curve["mean_cache_branch_velocity_rms"],
        solver_curve["denoising_solver_step"],
    )
)
auc_repeat = float(
    np.trapz(
        solver_curve["mean_repeat_floor_velocity_rms"],
        solver_curve["denoising_solver_step"],
    )
)
auc_ratio = auc_signal / auc_repeat
mean_above_floor_steps = int(
    (
        solver_curve["mean_cache_branch_velocity_rms"]
        > solver_curve["mean_repeat_floor_velocity_rms"]
    ).sum()
)

paired_one_step = one_step.pivot_table(
    index=["task", "trial_id", "source_wave_id"],
    columns="method",
    values="latent_mse_normalized_space",
)
one_step_fbfm_lower = int((paired_one_step["FBFM"] < paired_one_step["RTC"]).sum())
one_step_rows = int(len(paired_one_step))

rgb_pair = rgb_unit.pivot_table(
    index=["task", "trial_id", "horizon_frame"],
    columns="method",
    values="equal_camera_mean_rgb_mse",
)
rgb_fbfm_lower = int((rgb_pair["FBFM"] < rgb_pair["RTC"]).sum())

rho, rho_exact_p = exact_spearman_permutation_p(
    association["relative_mse_reduction"].to_numpy(),
    association["action_signal_above_repeat_floor"].to_numpy(),
)

channel_pair = action_channel_summary.pivot(
    index="normalized_action_channel", columns="condition", values="mean_channel_rms"
)
channel_signal_above = int(
    (
        channel_pair["rtc_vs_fbfm_cache_switch"]
        > channel_pair["same_cache_repeat_floor"]
    ).sum()
)

assert np.isclose(state_abs, frozen_summary["state"]["absolute_mean_mse_reduction"])
assert np.isclose(action_ratio, frozen_summary["action"]["final_action_signal_to_repeat_ratio_of_means"])
assert np.isclose(auc_ratio, frozen_summary["action"]["velocity_curve_auc_ratio"])
assert mean_above_floor_steps == 51
assert one_step_fbfm_lower == 34 and one_step_rows == 44
assert rgb_fbfm_lower == 6 and len(rgb_pair) == 16

summary_rows = [
    ("independent_task_trial_units", 4, "count", "task_x_trial", "Primary independent units"),
    ("strict_next_state_rtc_mean_mse", rtc_state, "normalized_latent_MSE", "4 units", "Strict wave-0 paired start"),
    ("strict_next_state_fbfm_mean_mse", fbfm_state, "normalized_latent_MSE", "4 units", "Strict wave-0 paired start"),
    ("strict_next_state_absolute_mse_reduction", state_abs, "normalized_latent_MSE", "4 paired units", "RTC minus FBFM"),
    ("strict_next_state_relative_mse_reduction", state_rel, "fraction", "4 paired units", "Ratio of mean reduction to RTC mean"),
    ("strict_next_state_difference_sd", state_difference_sd, "normalized_latent_MSE", "4 paired units", "Sample SD of paired RTC-minus-FBFM differences"),
    ("strict_next_state_difference_95pct_t_ci_low", state_difference_ci_low, "normalized_latent_MSE", "4 paired units", "Lower bound of two-sided 95% t interval for the mean paired difference"),
    ("strict_next_state_difference_95pct_t_ci_high", state_difference_ci_high, "normalized_latent_MSE", "4 paired units", "Upper bound of two-sided 95% t interval for the mean paired difference"),
    ("strict_next_state_fbfm_lower_units", 4, "count", "4 paired units", "Direction count"),
    ("paired_sign_test_two_sided_p", sign_p, "p_value", "4 paired units", "Exact sign test; descriptive small-n evidence"),
    ("cache_switch_mean_fresh_action_rms", action_signal, "normalized_action_RMS", "4 units; 2 probes averaged within unit", "RTC versus FBFM cache branch"),
    ("same_cache_repeat_mean_fresh_action_rms", repeat_floor, "normalized_action_RMS", "4 units; 2 probes averaged within unit", "Numerical repeat floor"),
    ("cache_switch_to_repeat_ratio_of_means", action_ratio, "ratio", "4 units", "Not a task-success multiplier"),
    ("cache_switch_solver_curve_auc", auc_signal, "RMS_x_solver_step", "4 units; 51 steps", "Mean unit-clustered curve"),
    ("repeat_floor_solver_curve_auc", auc_repeat, "RMS_x_solver_step", "4 units; 51 steps", "Mean unit-clustered curve"),
    ("solver_curve_auc_ratio", auc_ratio, "ratio", "4 units; 51 steps", "Cache switch divided by repeat floor"),
    ("solver_steps_mean_signal_above_floor", mean_above_floor_steps, "count", "51 solver steps", "Mean curves only"),
    ("one_step_fbfm_lower_unit_waves", one_step_fbfm_lower, "count", f"{one_step_rows} matched unit-waves", "Only wave 0 is strict paired-start evidence"),
    ("rgb_fbfm_lower_unit_frames", rgb_fbfm_lower, "count", "16 unit-frames", "Negative decoded-RGB sensitivity check"),
    ("state_action_spearman_rho", rho, "rank_correlation", "4 units", "Exploratory only"),
    ("state_action_spearman_exact_permutation_p", rho_exact_p, "p_value", "4 units; 24 permutations", "Exploratory only"),
    ("action_channels_mean_signal_above_floor", channel_signal_above, "count", "16 normalized channels", "Two probes clustered within each of 4 units"),
]
statistical_summary = pd.DataFrame(
    summary_rows, columns=["metric", "estimate", "unit", "sample_definition", "interpretation"]
)
statistical_summary.to_csv(DERIVED / "statistical_summary.csv", index=False)


# Figure 1: compact main-paper mechanism figure.
fig, axes = plt.subplots(1, 3, figsize=(6.25, 2.25), constrained_layout=True)

# Panel a: mean paired state difference only; raw units remain in the source
# and appendix diagnostic tables but are intentionally not drawn here.
ax = axes[0]
ax.axhline(0, color=BLACK, lw=0.7, zorder=1)
bar_x = 0.0
ax.bar(
    [bar_x],
    [state_abs],
    width=0.52,
    color=FBFM,
    edgecolor=BLACK,
    linewidth=0.6,
    zorder=2,
)
ax.errorbar(
    [bar_x],
    [state_abs],
    yerr=[[state_abs - state_difference_ci_low], [state_difference_ci_high - state_abs]],
    fmt="none",
    ecolor=BLACK,
    elinewidth=1.0,
    capsize=4,
    capthick=1.0,
    zorder=3,
)
ax.set_xticks([bar_x], ["Paired RTC - FBFM"])
ax.set_xlim(-0.82, 0.82)
ax.set_ylabel("Normalized next-state latent MSE difference", fontsize=7)
panel_a_ymin = state_difference_ci_low * 1.35
panel_a_ymax = state_difference_ci_high * 1.18
ax.set_ylim(panel_a_ymin, panel_a_ymax)
zero_axis_fraction = -panel_a_ymin / (panel_a_ymax - panel_a_ymin)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.text(
    0.54,
    0.97,
    "mean = 0.00769",
    color=FBFM,
    ha="left",
    va="top",
    transform=ax.transAxes,
    fontsize=6.8,
)
add_panel_title(ax, "a", "Encoded next-state improvement", y=1.02)

# Panel b: controlled cache intervention on final fresh action.
ax = axes[1]
pivot_action = cache_action_effect.pivot(index="unit", columns="condition", values="normalized_fresh_action_rms")
xpos = np.arange(len(pivot_action))
bar_width = 0.34
ax.bar(
    xpos - bar_width / 2,
    pivot_action["same_cache_repeat_floor"],
    width=bar_width,
    color=REPEAT,
    edgecolor=BLACK,
    linewidth=0.4,
    label="Repeat floor",
    zorder=2,
)
ax.bar(
    xpos + bar_width / 2,
    pivot_action["rtc_vs_fbfm_cache_switch"],
    width=bar_width,
    color=FBFM,
    edgecolor=BLACK,
    linewidth=0.4,
    label="Cache switch",
    zorder=2,
)
unit_tick_labels = [label.replace(" / ", "\n") for label in pivot_action.index]
ax.set_xticks(xpos, unit_tick_labels)
ax.set_xlim(-0.55, len(pivot_action) - 0.45)
panel_b_ymax = float(pivot_action.max().max()) * 1.19
panel_b_ymin = -zero_axis_fraction * panel_b_ymax / (1 - zero_axis_fraction)
ax.set_ylim(panel_b_ymin, panel_b_ymax)
ax.set_yticks(np.arange(0, 0.0141, 0.002))
ax.axhline(0, color=BLACK, lw=0.7, zorder=1)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.set_ylabel(r"Normalized fresh-action RMS ($\times 10^{-3}$)", fontsize=7)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda value, _: f"{value * 1e3:g}"))
ax.legend(loc="upper left", alignment="left", handlelength=1.6)
ax.text(0.05, 0.69, "7.39x ratio of means", color=FBFM, ha="left", va="top", transform=ax.transAxes, fontsize=6.8)
add_panel_title(ax, "b", "Cache changes the action", y=1.02)

# Panel c: difference persists across all 51 action solver steps.
ax = axes[2]
x = solver_curve["denoising_solver_step"].to_numpy()
signal_mean = solver_curve["mean_cache_branch_velocity_rms"].to_numpy()
signal_min = solver_curve["min_cache_branch_velocity_rms"].to_numpy()
signal_max = solver_curve["max_cache_branch_velocity_rms"].to_numpy()
floor_mean = solver_curve["mean_repeat_floor_velocity_rms"].to_numpy()
floor_min = solver_curve["min_repeat_floor_velocity_rms"].to_numpy()
floor_max = solver_curve["max_repeat_floor_velocity_rms"].to_numpy()
ax.fill_between(x, signal_min, signal_max, color=FBFM, alpha=0.11, linewidth=0)
ax.fill_between(x, floor_min, floor_max, color=REPEAT, alpha=0.11, linewidth=0)
ax.plot(x, signal_mean, color=FBFM, ls="-", marker="o", markevery=10, ms=2.7, label="Cache switch")
ax.plot(x, floor_mean, color=REPEAT, ls="-", marker="s", markevery=10, ms=2.5, label="Repeat floor")
ax.set_xlabel("Action solver step")
ax.set_ylabel("Normalized velocity RMS", fontsize=7)
ax.set_xlim(0, 50)
panel_c_ymax = max(signal_max.max(), floor_max.max()) * 1.10
panel_c_ymin = -zero_axis_fraction * panel_c_ymax / (1 - zero_axis_fraction)
ax.set_ylim(panel_c_ymin, panel_c_ymax)
ax.set_yticks(np.arange(0, 0.121, 0.02))
ax.axhline(0, color=BLACK, lw=0.7, zorder=1)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.legend(loc="upper left", handlelength=2.4, alignment="left")
ax.text(
    0.24,
    0.75,
    "AUC 2.52x\nmean above floor: 51/51",
    color=FBFM,
    ha="left",
    va="center",
    transform=ax.transAxes,
    fontsize=6.8,
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.86, "pad": 1.2},
)
add_panel_title(ax, "c", "Effect spans the action solve", y=1.02)

save_figure(fig, "fig1_aux_mechanism_main", "FBFM auxiliary mechanism: state consistency and cache-to-action effect")


# Figure S1: diagnostics and claim boundaries.
fig, axes = plt.subplots(2, 2, figsize=(6.25, 4.85), constrained_layout=True)

# Panel a: unit-wise strict state effect.
ax = axes[0, 0]
forest = state_pair.sort_values(["task", "trial_id"]).reset_index(drop=True)
y = np.arange(len(forest))[::-1]
ax.axvline(0, color=BLACK, lw=0.7)
for yy, value in zip(y, forest["absolute_mse_reduction"], strict=True):
    ax.plot([0, value], [yy, yy], color=FBFM, alpha=0.65, lw=1.4)
ax.scatter(forest["absolute_mse_reduction"], y, color=FBFM, s=26, marker="o", zorder=3)
ax.set_yticks(y, forest["unit"])
ax.set_xlabel("RTC - FBFM normalized latent MSE")
ax.set_xlim(-0.001, float(forest["absolute_mse_reduction"].max()) * 1.18)
ax.text(0.98, 0.05, "Positive favors FBFM", ha="right", color=FBFM, transform=ax.transAxes, fontsize=6.6)
add_panel_title(ax, "a", "All strict pairs favor FBFM")

# Panel b: one-step error across source waves with at least 3 units available.
ax = axes[0, 1]
trend = one_step_summary[one_step_summary["source_wave_id"].le(6)].copy()
for method, color, linestyle, marker in (
    ("RTC", RTC, "--", "s"),
    ("FBFM", FBFM, "-", "o"),
):
    rows = trend[trend["method"].eq(method)]
    xx = rows["source_wave_id"].to_numpy()
    ax.fill_between(xx, rows["min_latent_mse"].to_numpy(), rows["max_latent_mse"].to_numpy(), color=color, alpha=0.10, linewidth=0)
    ax.plot(xx, rows["mean_latent_mse"], color=color, ls=linestyle, marker=marker, ms=3.2, label=method)
ax.axvline(0, color=BLACK, lw=0.7, alpha=0.7)
ax.set_xlabel("Source wave (one-step prediction)")
ax.set_ylabel("Next-wave latent MSE (normalized)")
ax.set_xticks(range(7))
ax.legend(loc="upper left")
ax.text(0.98, 0.04, "wave 0: paired start\nwaves 1-6: own trajectories\nn = 4,4,4,4,4,4,3", ha="right", va="bottom", transform=ax.transAxes, fontsize=6.3)
add_panel_title(ax, "b", "Descriptive one-step trend")

# Panel c: decoded RGB sensitivity check.
ax = axes[1, 0]
for method, color, linestyle, marker in (
    ("RTC", RTC, "--", "s"),
    ("FBFM", FBFM, "-", "o"),
):
    rows = rgb_summary[rgb_summary["method"].eq(method)]
    xx = rows["horizon_frame"].to_numpy()
    ax.fill_between(xx, rows["min_unit_rgb_mse"].to_numpy(), rows["max_unit_rgb_mse"].to_numpy(), color=color, alpha=0.10, linewidth=0)
    ax.plot(xx, rows["mean_equal_camera_rgb_mse"], color=color, ls=linestyle, marker=marker, ms=3.4, label=method)
ax.set_xlabel("Decoded frame within next-state slot")
ax.set_ylabel("Equal-camera RGB MSE")
ax.set_xticks([1, 2, 3, 4])
ax.legend(loc="upper left")
ax.text(
    0.98,
    0.95,
    "FBFM lower in 6/16 unit-frames",
    color=BLACK,
    ha="right",
    va="top",
    transform=ax.transAxes,
    fontsize=6.6,
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.86, "pad": 1.0},
)
add_panel_title(ax, "c", "Negative RGB sensitivity check")

# Panel d: exploratory association, no fitted line at n=4.
ax = axes[1, 1]
marker_map = {"adjust_bottle": "o", "pick_diverse_bottles": "^"}
for _, row in association.iterrows():
    xval = row["relative_mse_reduction"] * 100
    yval = row["action_signal_above_repeat_floor"]
    ax.scatter(xval, yval, color=FBFM, marker=marker_map[row["task"]], s=30, edgecolor="white", linewidth=0.5, zorder=3)
    ax.annotate(f"T{int(row['trial_id'])}", (xval, yval), xytext=(3, 2), textcoords="offset points", fontsize=6)
ax.set_xlabel("Unit-level latent MSE reduction (%)")
ax.set_ylabel("Action signal above floor (RMS)")
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, -3))
ax.yaxis.set_major_formatter(formatter)
legend_handles = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor=FBFM, markeredgecolor="white", label="adjust_bottle"),
    Line2D([0], [0], marker="^", color="none", markerfacecolor=FBFM, markeredgecolor="white", label="pick_diverse_bottles"),
]
ax.legend(handles=legend_handles, loc="upper left", handletextpad=0.3)
ax.text(0.98, 0.05, f"Spearman rho = {rho:.2f}\nexact permutation p = {rho_exact_p:.2f}\nexploratory, n = 4", ha="right", va="bottom", transform=ax.transAxes, fontsize=6.3)
add_panel_title(ax, "d", "State-action association is unresolved")

save_figure(fig, "figS1_aux_diagnostics", "FBFM auxiliary diagnostic and sensitivity analyses")


# Figure S2: normalized action-channel breakdown.
fig, ax = plt.subplots(figsize=(6.25, 2.35), constrained_layout=True)
channel_order = sorted(action_channel_summary["normalized_action_channel"].unique())
xpos = np.arange(len(channel_order))
for condition, color, linestyle, marker, label in (
    ("rtc_vs_fbfm_cache_switch", FBFM, "-", "o", "RTC-FBFM cache switch"),
    ("same_cache_repeat_floor", REPEAT, "--", "s", "Same-cache repeat floor"),
):
    rows = (
        action_channel_summary[action_channel_summary["condition"].eq(condition)]
        .set_index("normalized_action_channel")
        .loc[channel_order]
    )
    ax.fill_between(xpos, rows["min_unit_channel_rms"].to_numpy(), rows["max_unit_channel_rms"].to_numpy(), color=color, alpha=0.10, linewidth=0)
    ax.plot(xpos, rows["mean_channel_rms"], color=color, ls=linestyle, marker=marker, ms=3.1, label=label)
ax.set_xticks(xpos, [str(value) for value in channel_order])
ax.set_xlabel("Normalized fresh-action channel ID")
ax.set_ylabel("Per-channel action RMS")
ax.set_ylim(bottom=0)
ax.legend(loc="upper right", ncol=2, handlelength=2.4)
ax.text(
    0.01,
    0.95,
    f"Cache-switch mean exceeds repeat floor\nin {channel_signal_above}/16 channels",
    va="top",
    transform=ax.transAxes,
    fontsize=6.8,
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.86, "pad": 1.0},
)
add_panel_title(ax, "", "Action effect is distributed across normalized channels")
save_figure(fig, "figS2_action_channels", "FBFM cache intervention by normalized action channel")


# Machine-readable provenance and output manifest.
source_manifest = {
    path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
    for path in sorted(SOURCE.iterdir())
    if path.is_file()
}
derived_manifest = {
    str(path.relative_to(ROOT)).replace("\\", "/"): {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    for path in sorted([*DERIVED.glob("*"), *FIGURES.glob("*")])
    if path.is_file()
}
authored_paths = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / "docs" / "AUXILIARY_EXPERIMENT_RESULTS_AND_ANALYSIS.md",
    ROOT / "scripts" / "build_visualization.py",
    ROOT / "scripts" / "publication.mplstyle",
]
authored_manifest = {
    str(path.relative_to(ROOT)).replace("\\", "/"): {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    for path in authored_paths
    if path.is_file()
}
provenance = {
    "schema_version": 1,
    "paper_context": {
        "repository": "https://github.com/StvLi/fbfm_paper",
        "commit": "ebba5a7e456f58036e3715115f20d5d7b8fb166a",
        "preview_pdf_note": "docs/preview.pdf is gitignored; recompiled outside the repository from tracked preview.tex and chapter sources",
    },
    "experiment_scope": {
        "added_rollouts": 0,
        "independent_unit": "task_x_trial",
        "independent_units": 4,
        "cache_probes": 8,
        "probes_per_unit": 2,
        "strict_state_comparison": "wave_0_next_state",
        "claim_boundary": "computation-level feedback-to-state and cache-to-action arrows only",
    },
    "software": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "matplotlib": mpl.__version__,
    },
    "source_files": source_manifest,
    "generated_files": derived_manifest,
    "authored_and_context_files": authored_manifest,
}
with (ROOT / "provenance.json").open("w", encoding="utf-8", newline="\n") as handle:
    json.dump(provenance, handle, indent=2, sort_keys=True)
    handle.write("\n")

print(json.dumps({"status": "ok", "figures": 3, "derived_tables": len(list(DERIVED.glob('*'))), "headline": {"state_relative_reduction": state_rel, "action_ratio": action_ratio, "solver_auc_ratio": auc_ratio, "state_action_rho": rho, "state_action_exact_p": rho_exact_p}}, indent=2))
