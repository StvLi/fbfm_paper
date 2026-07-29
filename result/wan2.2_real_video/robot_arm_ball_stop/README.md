# Real-Video Robot-Arm Ball-Stopping Experiment

## Status

Completed on 2026-07-29. This package records a matched-seed comparison between
Wan2.2 Base and visual-only FBFM on a real RealSense D435i recording. It is a
diagnostic result rather than evidence of a positive FBFM outcome: at the
requested default gain `kp=1`, the FBFM video develops severe high-frequency
colour and texture artifacts from approximately 0.25 s into the prediction.

## Experimental question

Given the same final context frame, text prompt, initial noise, and Wan2.2
configuration, compare:

1. `Wan2.2 Base`: native image-to-video prediction with no observation
   feedback.
2. `FBFM Ours`: the same solve with the 120 measured future RGB frames encoded
   causally into 30 Wan latent slots and released across solver boundaries.

This experiment concerns observation/state prediction only. It contains no
action variable, action prediction, or robot command.

## Source and preprocessing

The source was the ROS2 SQLite bag `20260729_005218.db3` recorded from a
RealSense D435i. The raw bag is intentionally omitted from Git because it is
1,719,549,952 bytes.

```text
SHA-256: 9b94b74546fb6d5e66b340312d1d46cbc5d913667afda484e534695cc6706a5e
Topic: /device_0/sensor_1/Color_0/image/data
Message type: sensor_msgs/msg/Image
Serialization: CDR
Encoding: rgb8
Source geometry: 1280 x 720
```

The colour stream was sampled by bag timestamps to 24 fps. Eight rows were
cropped from both the top and bottom, producing the native Wan landscape size
of 1280 x 704. The first seven seconds contain 168 frames. The source contains
one approximately 335 ms acquisition gap at 0.46--0.80 s, inside the displayed
context; nearest-neighbour resampling consequently reused seven source frames.
See [`artifacts/preprocessing.json`](artifacts/preprocessing.json) for the
complete sampling record.

The temporal split is:

| Segment | Normalized frames | Count | Role |
| --- | ---: | ---: | --- |
| Displayed context | 0--47 | 48 | First 2 s of the comparison videos |
| Wan anchor | 47 | 1 | Actual TI2V image condition |
| Prediction/reference | 47--167 | 121 | Anchor plus 120 future frames, spanning 5 s |
| FBFM observations | 48--167 | 120 | Four consecutive frames per latent slot, slots 1--30 |

Wan2.2-TI2V-5B is image-conditioned, so the model itself receives frame 47,
not the complete 48-frame context clip. The complete two-second clip is
prepended only in the `with_context` presentation videos.

## Prompt

Base and FBFM use exactly the same prompt:

> Fixed high-angle RealSense video of a robotic arm positioned at the right
> edge of a white laboratory table. An orange miniature basketball and a
> black-and-white miniature soccer ball roll rapidly from left to right across
> the table toward the robot. As the balls approach, the robotic gripper moves
> inward and intercepts and stops the black-and-white soccer ball near its
> fingers, while the orange ball continues past and exits the scene. Realistic
> rigid-body physics, fixed camera, natural laboratory lighting.

## Configuration

| Parameter | Base | FBFM Ours |
| --- | ---: | ---: |
| Checkpoint | Wan2.2-TI2V-5B | Wan2.2-TI2V-5B |
| Output | 121 frames, 24 fps, 1280 x 704 | Same |
| Seed | 0 | 0 |
| Solver steps | 50 | 50 |
| Shift | 5.0 | 5.0 |
| CFG scale | 5.0 | 5.0 |
| State weight | 1.0 | 1.0 |
| Proportional gain `kp` | 1.0 | 1.0 |
| Guidance cap `beta` | 10.0 | 10.0 |
| Feedback slots | 0 | 30, slots 1--30 |

The explicit feedback release schedule was:

```text
1,3,4,6,8,9,11,12,14,16,17,19,20,22,24,25,27,29,30,32,33,35,37,38,40,41,43,45,46,48
```

The FBFM audit contains 30 accepted feedback updates, constraint version 30,
and 49 guided solver steps. The Base audit contains no feedback update. Both
runs report deterministic CUDA algorithms and the same seed.

## Main artifacts

| File | Description |
| --- | --- |
| [`artifacts/reference_base_fbfm_keyframes.jpg`](artifacts/reference_base_fbfm_keyframes.jpg) | Paper-ready grid at 0, 0.25, 0.5, 1, 2, 3, 4, and 5 s |
| [`artifacts/reference_base_fbfm_future.mp4`](artifacts/reference_base_fbfm_future.mp4) | Reference / Base / Ours triptych for the five-second future |
| [`artifacts/reference_base_fbfm_with_context.mp4`](artifacts/reference_base_fbfm_with_context.mp4) | Triptych with the common two-second context prepended |
| [`artifacts/normalized_first_7s_24fps_1280x704.mp4`](artifacts/normalized_first_7s_24fps_1280x704.mp4) | Complete normalized real-video reference |
| [`artifacts/input_context_2s.mp4`](artifacts/input_context_2s.mp4) | Displayed context clip |
| [`artifacts/reference_future_121f.mp4`](artifacts/reference_future_121f.mp4) | Aligned five-second reference future including the anchor |
| [`artifacts/base_future.mp4`](artifacts/base_future.mp4) | Raw Wan2.2 Base generation |
| [`artifacts/fbfm_ours_future.mp4`](artifacts/fbfm_ours_future.mp4) | Raw 30-slot FBFM generation |
| [`artifacts/base_with_context.mp4`](artifacts/base_with_context.mp4) | Base with context |
| [`artifacts/fbfm_ours_with_context.mp4`](artifacts/fbfm_ours_with_context.mp4) | FBFM with context |
| [`artifacts/keyframes/`](artifacts/keyframes/) | 24 full-resolution PNGs, eight for each method/reference |
| [`artifacts/base_future.json`](artifacts/base_future.json) | Base solver audit |
| [`artifacts/fbfm_ours_future.json`](artifacts/fbfm_ours_future.json) | Per-step FBFM feedback/guidance audit |
| [`artifacts/experiment_summary.json`](artifacts/experiment_summary.json) | Configuration, metrics, audit summary, and original workspace paths |

The paths embedded in `experiment_summary.json` and `preprocessing.json` are
the original workstation paths retained for provenance. Use the relative links
in this document when reading the branch package.

## Observed result

The Base video keeps the robot and table geometrically coherent and produces a
plausible ball interaction, although its trajectories and terminal state do
not exactly match the recorded future. FBFM at `kp=1` preserves the broad
layout but introduces dense, temporally unstable, colourful high-frequency
artifacts over the table and moving objects shortly after feedback begins.

Full-frame metrics against the reference were:

| Metric | Base | FBFM Ours |
| --- | ---: | ---: |
| MAE | 9.6261 | 9.2731 |
| PSNR (dB) | 20.0618 | 23.1021 |
| Temporal-gradient MAE | 2.8468 | 5.4817 |

The static background dominates the full-frame MAE and PSNR, so their modest
improvement does not reflect perceptual quality. The approximately 1.93x worse
temporal-gradient error is consistent with the visible flickering artifacts.
This run should therefore be retained as evidence that unscaled state-only
feedback at `kp=1` is unstable for this scene, not as a headline positive
comparison.

## Reproducibility snapshot

[`runtime_snapshot/`](runtime_snapshot/) contains the exact inference,
feedback, Wan attention/checkpointing modifications, preprocessing,
postprocessing, and test files used for this run. They were copied from a
Wan2.2 worktree at upstream revision:

```text
42bf4cfaa384bc21833865abc2f9e6c0e67233dc
```

The runtime environment was Python 3.10.20, PyTorch 2.9.0+cu129, CUDA 12.9,
NumPy 1.26.4, OpenCV 4.11.0, Pillow 12.2.0, and ImageIO 2.37.4. Model weights
are not included. The FBFM state-feedback test suite completed with 10 tests
passing; Ruff and whitespace checks also passed.
