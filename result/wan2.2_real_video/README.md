# Wan2.2 Real-Video Experiments

This branch-local result package stores FBFM state-prediction experiments on
real videos using Wan2.2-TI2V-5B. It is kept separate from the simulator and
robot-policy result packages because the experiment evaluates visual state
prediction only; no action is predicted or executed by Wan2.2.

| Experiment | Scene | Conditions | Included state |
| --- | --- | --- | --- |
| [`robot_arm_ball_stop/`](robot_arm_ball_stop/) | RealSense D435i view of a robot-arm ball-stopping task | 2 s displayed context, 5 s prediction, Base versus 30-slot FBFM | Complete, including videos, frame extracts, audit logs, metadata, and runtime snapshot |

## Storage policy

The 1.7 GiB ROS2 SQLite bag is not stored in ordinary Git. The experiment
package records its exact filename, byte size, SHA-256 digest, topic, message
format, and sampling metadata. The complete normalized seven-second RGB clip
derived from the bag is versioned, together with all inputs used for inference.

Every versioned file in an experiment package is covered by its `SHA256SUMS`
manifest. Model checkpoints are not versioned.
