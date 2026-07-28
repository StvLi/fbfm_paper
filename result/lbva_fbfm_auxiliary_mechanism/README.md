# LingBot-VA FBFM Auxiliary Mechanism Results

This package records a compact, frozen RoboTwin analysis of two links in the
FBFM mechanism:

1. `feedback -> encoded next-state prediction`
2. `predicted state/cache -> fresh action computation`

It reuses the completed rapid LingBot-VA outputs. No additional RoboTwin
rollout was generated for this analysis.

## Headline results

| Evidence | RTC / repeat reference | FBFM / cache intervention | Result |
| --- | ---: | ---: | --- |
| Wave-0 next-state latent MSE | 0.682834 | 0.675149 | FBFM lower by 1.13%; 4/4 paired units |
| Wave-0 latent cosine similarity | 0.524866 | 0.530125 | FBFM higher in 4/4 paired units |
| Final fresh-action normalized RMS | 0.001205 repeat floor | 0.008900 cache-branch difference | 7.39x the repeat floor |
| Action denoising velocity AUC | 0.354747 repeat floor | 0.894198 cache-branch difference | 2.52x; signal higher at 51/51 steps |

The decoded RGB sensitivity check does not support a pixel-level improvement:
FBFM has lower RGB MSE in only 6/16 unit-frame comparisons. The defensible
claim is therefore limited to the encoded latent representation. The four-unit
sample and equal 75% episode success rates also preclude a population-wide or
success-mediation claim.

## Package layout

| Path | Contents |
| --- | --- |
| `NUMERIC_MECHANISM_EXPERIMENT.md` | Complete protocol, tables, interpretation, limitations, and paper-ready statement |
| `aggregate/` | Strict paired state metrics, descriptive trends, action-probe rows, and structured summary |
| `figures/` | PNG and PDF paper figures |
| `control/` | Reproducible state extraction and offline aggregation scripts |
| `artifact_manifest.json` | Original 25-artifact size and SHA-256 manifest |
| `SHA256SUMS` | Repository-package checksums, including this README and the original manifest |

## Provenance

- Rapid profile: 2 tasks x 2 trials x 3 methods
- Independent units: 4 `task x trial` pairs
- Cache-intervention probes: 8, clustered as two probes per unit
- Method revision: `5b6868cdf981dd7a019bcba7186c1b540e3d1cee`
- Protocol SHA-256: `27beb50db0ecd281a866fa8adce63ff1aa48ae21d3ff7f50e9b6ddc9e0c9e26f`
- Source package: `rapid_paper_2x2/numeric_mechanism_v1`

The raw videos, checkpoints, simulator state, and multi-megabyte server result
files remain in the experiment workspace. Their exact source hashes are listed
in `aggregate/numeric_summary.json`.

## Integrity

`artifact_manifest.json` was verified against every copied source artifact
before packaging. Run the repository-level check from this directory with:

```bash
sha256sum --check SHA256SUMS
```
