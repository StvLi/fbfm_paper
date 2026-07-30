# Figure and Repository Audit

## Figure checks

- All three figures were exported as vector PDF, editable-text SVG, and
  600-dpi RGB PNG without alpha channels.
- At the paper draft's approximately 158.75 mm text width, the PNG effective
  resolution is 597.6-605.6 dpi. All metadata checks passed.
- PDF font inspection reports embedded, subsetted Unicode TrueType fonts for
  every figure.
- Each vector PDF was rendered independently with Poppler and visually checked
  for clipped labels, overlap, broken glyphs, and unreadable legends. No
  rendering defect remains in the final files.
- FBFM blue (`#0072B2`), RTC orange (`#D55E00`), and repeat-floor gray
  (`#6B7280`) each exceed 3:1 contrast against white.
- The palette audit flags small pairwise grayscale lightness separation. The
  figures therefore never rely on hue alone: RTC uses dashed lines and square
  markers, FBFM uses solid lines and circles, and the repeat floor is gray,
  square-marked, and directly labeled (solid in Figure 1c and dashed in Figure
  S2). Paired comparisons are also identified through grouped bars or labeled
  x-axis conditions.
- Bands are explicitly documented as unit minima and maxima, not confidence
  intervals.
- Figure 1a is the exception: its single bar reports the mean paired
  `RTC - FBFM` difference, and its error bar is explicitly defined as the
  two-sided 95% Student-t interval over four independent task-by-trial units.
  The zero baseline is shown because the estimate is encoded by bar length.
- Figure 1 uses equal-sized plotting areas and a common vertical position for
  the zero reference. The negative confidence bound remains visible in panel
  a; panels b-c therefore reserve the same proportional lower margin without
  plotting or labeling negative values.

These checks establish the properties tested here; they do not claim
compliance with an unspecified journal or conference production profile.

## Source-repository read-only audit

The user repository was checked with optional Git locks disabled.

| Check | Before work | After work |
|---|---|---|
| Repository | `C:\Users\zhang\Documents\GitHub\fbfm_paper` | same |
| HEAD | `c1eb1342afeda715fe89f6f545949b6f850bc07d` | `c1eb1342afeda715fe89f6f545949b6f850bc07d` |
| Porcelain status | clean | clean |
| Target commit in local object store | absent | absent |

No checkout, fetch, commit, branch change, file creation, or result copy was
performed in that repository during figure generation. The specified target
commit was obtained in an isolated mirror. Since `docs/preview.pdf` is ignored
and not tracked at that commit, its tracked TeX and chapter sources were
compiled in an isolated working copy. The reconstructed context PDF is not
duplicated in this repository package.
