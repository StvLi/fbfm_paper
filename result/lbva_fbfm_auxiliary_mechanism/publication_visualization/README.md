# FBFM Auxiliary Visualization Deliverable

This directory contains a self-contained, reproducible visualization and
manuscript-analysis package for the completed LingBot-VA auxiliary mechanism
experiment. The figures were designed against the paper text at commit
`ebba5a7e456f58036e3715115f20d5d7b8fb166a` and are stored with the frozen
tables from which they were generated.

## Headline result

- Encoded next-state latent MSE: RTC 0.682834, FBFM 0.675149, a 1.125% mean
  reduction with the favorable direction in 4/4 paired task-by-trial units.
- Controlled cache switch: normalized fresh-action RMS 0.008900 versus a
  same-cache repeat floor of 0.001205, a 7.386x ratio of means.
- Action solver trajectory: cache-switch mean above the repeat floor in 51/51
  solver steps, with a 2.521x AUC ratio.
- Claim boundary: four independent units, negative decoded-RGB sensitivity,
  unresolved state-action association, and equal 3/4 episode success across
  RTC, FBFM, and FBFM-CacheCut.

## Key files

- `docs/AUXILIARY_EXPERIMENT_RESULTS_AND_ANALYSIS.md`: paper-ready experiment
  description, results, captions, interpretation, and limitations.
- `figures/fig1_aux_mechanism_main.{pdf,png,svg}`: recommended main figure.
- `figures/figS1_aux_diagnostics.{pdf,png,svg}`: trends, RGB sensitivity, and
  exploratory association.
- `figures/figS2_action_channels.{pdf,png,svg}`: normalized action-channel
  breakdown.
- `scripts/build_visualization.py`: full data transformation, checking, and
  plotting pipeline.
- `data/source`: immutable copies of the frozen auxiliary result tables and
  CacheCut records.
- `data/derived`: tidy analysis tables and machine-readable statistics.
- `provenance.json`: SHA-256 and software provenance.
- `audit/`: rendered-figure, metadata, palette, and historical read-only
  source-context checks.

## Rebuild

```bash
python -m pip install -r requirements.txt
python scripts/build_visualization.py
```

No rollout, checkpoint loading, or GPU is required.
