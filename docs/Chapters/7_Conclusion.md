# Conclusion

This paper studies a practical mismatch in world-action model execution:
long-horizon behavior needs continual grounding in real observations, while
existing chunk-wise refresh schemes only correct the model after a chunk has
already been generated. We proposed Feedback Flow Matching (FBFM), a
training-free inference mechanism that moves feedback into the active
flow-matching process. By expressing both committed actions and newly observed
latent states as masked pseudoinverse measurements, FBFM provides a common
correction interface for stage-wise and joint-generation WAMs.

Our experiments instantiate this idea on LingBot-VA/RoboTwin and
DreamZero/LIBERO, and further evaluate real-world observation prediction with
Wan2.2. The results show a 3.0-point task-configuration macro gain for the
stage-wise WAM, mechanism-level evidence that state feedback changes latent
prediction and propagates to action generation through the velocity field, and
modest but positive aggregate gains for the joint WAM after feedback-scale
tuning. The real-world video diagnostic
also indicates that FBFM can constrain physically meaningful visual evolution
beyond open-loop prediction. Together, these findings support FBFM as a simple
and extensible way to bridge open-loop generative execution with online
environment feedback.

Several limitations remain. The improvement on DreamZero is limited, likely
because its accelerated inference reuses model velocities and endpoint
Jacobians across multiple solver updates, which weakens the immediate effect of
new feedback. FBFM also adds Jacobian-vector-product and feedback-management
overhead at inference time; deploying it as a closed-loop robot policy requires
further engineering to recover real-time control frequency. Looking forward,
asynchronous feedback may make longer WAM chunks usable without abandoning
fine-grained correction. We also see two useful theoretical and algorithmic
directions: studying latent-space state transitions with nonlinear dynamics
tools, and replacing the current proportional gain with richer feedback
controllers, such as PID-style corrections, inside the flow-matching process.
