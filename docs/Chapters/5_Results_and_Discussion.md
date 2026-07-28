# Results and Discussion

## LingBot-VA on RoboTwin

We compare the frozen LingBot-VA checkpoint with no inference-time feedback
(Base) against the same checkpoint equipped with FBFM (Ours). The final summary
uses the same selected 42-task set for both methods and reports only the
aggregate success rate under RoboTwin's clean and randomized configurations.
Task-level successes and trial counts are reserved for Appendix D.

| Method | Clean SR (%) | Randomized SR (%) |
| --- | ---: | ---: |
| LingBot-VA (Base, NONE) | -- | -- |
| LingBot-VA + FBFM (Ours) | -- | -- |

<!-- TODO(results): Fill only after all 42 tasks have matched Base/FBFM records
under both configurations. Do not use the non-matched pooled snapshot rates. -->

## DreamZero on LIBERO

We similarly compare the frozen DreamZero checkpoint with and without FBFM on
the four standard LIBERO suites used in this study. LIBERO-90 is excluded. The
two rows will be filled only from matched evaluations using the same checkpoint,
task set, reset IDs, episode horizon, and delayed pseudo-asynchronous overlap
protocol. Results from DreamZero's native synchronous rollout are not used in
this comparison. Full per-task records are maintained in Appendix D.

| Method | Spatial SR (%) | Object SR (%) | Goal SR (%) | LIBERO-10 SR (%) |
| --- | ---: | ---: | ---: | ---: |
| DreamZero (Base, NONE) | -- | -- | -- | -- |
| DreamZero + FBFM (Ours) | -- | -- | -- | -- |

<!-- TODO(results): Fill both rows only after the matched delayed
pseudo-asynchronous evaluation is complete. Keep native synchronous results and
preliminary single-task diagnostics out of this table. -->
