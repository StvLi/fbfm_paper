# FBFM Paper Workspace

This repository contains the editable manuscript and supporting material for:

> **FBFM: A Training-Free Asynchronous Feedback Mechanism for Flow-Matching in
> World-Action Models Execution**

## Repository layout

- `docs/Chapters/`: chapter sources, maintained in paired Markdown and LaTeX files.
- `docs/preview.tex`: entry point for compiling the complete paper draft.
- `docs/ref_paper/`: local copies of core reference papers used during writing.
- `docs/exp_result/`: experiment records awaiting integration into the manuscript.
- `docs/TODO.md`: paper-wide writing, experiment, and consistency checklist.
- `docs/handover.md`: confirmed theory-to-implementation handover items.
- `material/`: source and cropped figures used by the manuscript.
- `result/`: versioned experiment ledgers, derived tables, and implementation notes.

## Editing convention

When a chapter is changed, update its `.md` and `.tex` versions together. The
Markdown files support collaborative review; the LaTeX files are the source of
the compiled paper.

## Build

Run the following commands from the repository root:

```bash
cd docs
latexmk -pdf -interaction=nonstopmode -outdir=build preview.tex
```

The preview is generated at `docs/build/preview.pdf`. All LaTeX build products
are intentionally ignored by Git.

To remove generated files:

```bash
cd docs
latexmk -C -outdir=build preview.tex
```
