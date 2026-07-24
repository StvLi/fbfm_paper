# Experiments

We evaluate FBFM in two complementary tracks that cover the two WAM generation
factorizations considered in Section 3. Comparisons are made within each track
using the same frozen base model; absolute scores are not compared across
architectures or benchmarks.

## Models, Benchmarks, and Tasks

**Models.** We instantiate FBFM on LingBot-VA and DreamZero. The LingBot-VA
track uses the official checkpoint post-trained on RoboTwin. Its released
inference implementation provides the stage-wise WAM instance, in which the
state trajectory is generated before the action trajectory. The DreamZero
track uses the LIBERO-post-trained checkpoint released through the [RLinf
DreamZero SFT
recipe](https://rlinf.readthedocs.io/zh-cn/latest/rst_source/examples/embodied/sft_dreamzero.html).
DreamZero jointly generates future states and actions and therefore provides
the joint-generation WAM instance. Together, the two tracks test whether the
same training-free feedback principle transfers across distinct WAM
factorizations rather than comparing the two base models directly.

**Benchmarks and tasks.** We evaluate the LingBot-VA track on RoboTwin and the
DreamZero track on LIBERO. Both benchmarks provide environment-side,
task-specific completion predicates. We use these native predicates without
manual relabeling: an episode is assigned \(u_{q,n}=1\) if the benchmark reports
successful completion of task \(q\), and \(u_{q,n}=0\) otherwise. For \(N_q\)
evaluation episodes, the per-task success rate is

\[
\operatorname{SR}_q=\frac{1}{N_q}\sum_{n=1}^{N_q}u_{q,n}.
\]

<!-- TODO(experiments): Enumerate the exact RoboTwin and LIBERO tasks, benchmark
versions/suites, checkpoint identifiers, episode counts, seeds, and aggregation
protocol after receiving the finalized records from the experiment team. -->

## FBFM Instantiations

<!-- Content to be developed. -->

## Baselines and Ablations

<!-- Content to be developed. -->
