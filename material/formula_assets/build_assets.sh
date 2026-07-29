#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")" && pwd)"
build_dir="$root_dir/build"
mkdir -p "$build_dir"

cd "$root_dir"

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -halt-on-error \
  -outdir="$build_dir" \
  formula_sheet.tex
cp "$build_dir/formula_sheet.pdf" "$root_dir/formula_sheet.pdf"

build_tile() {
  job_name="$1"
  macro_name="$2"
  pdflatex \
    -interaction=nonstopmode \
    -halt-on-error \
    -output-directory="$build_dir" \
    -jobname="$job_name" \
    "\\def\\AssetName{$macro_name}\\input{tile.tex}" >/dev/null
  cp "$build_dir/$job_name.pdf" "$root_dir/$job_name.pdf"
}

build_tile 01_state_slot_labels StateSlotLabels
build_tile 02_action_slot_labels ActionSlotLabels
build_tile 03_execution_transition ExecutionTransition
build_tile 04_overlap_labels OverlapLabels
build_tile 05_stage_state_field StageStateField
build_tile 06_stage_action_field StageActionField
build_tile 07_refreshed_state_context RefreshedStateContext
build_tile 08_joint_variable JointVariable
build_tile 09_joint_target_mask JointTargetMask
build_tile 10_joint_guided_field JointGuidedField
build_tile 11_cross_modal_correction CrossModalCorrection
build_tile 12_generic_flow_integral GenericFlowIntegral
build_tile 13_unified_endpoint_chain UnifiedEndpointChain
build_tile 14_measurement_lifting MeasurementLifting
build_tile 15_stage_factorization StageFactorization
build_tile 16_real_state_slot_labels RealStateSlotLabels
build_tile 17_encoded_feedback_slot_labels EncodedFeedbackSlotLabels
build_tile 18_committed_action_slot_labels CommittedActionSlotLabels
