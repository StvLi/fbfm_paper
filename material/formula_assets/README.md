# FBFM Figure Formula Assets

These assets replace the provisional formulas and repeated zero-valued time
indices in Figures 1 and 3. They use the paper's global environment-time
indexing:

- latent-state slots: \(\hat z^1_{t+1},\ldots,\hat z^1_{t+H}\);
- action slots: \(\hat a^1_t,\ldots,\hat a^1_{t+H-1}\);
- real environment states: \(s_t,\ldots,s_{t+H}\);
- real feedback: \(z_{t+i}=E(\mathcal O(s_{t+i}))\);
- committed overlap action: \(a_{t+i}^{\mathrm{prev}}\).

The file formula_sheet.pdf is a large-font overview. The numbered PDFs are
individually cropped vector tiles intended for placement in presentation
software. Their shared LaTeX definitions are in asset_macros.tex.

The compact slot labels deliberately omit the solver-evaluation index \(k\).
The full correction formulas retain \(t\), \(k\), and the corresponding flow
time \(\tau_k^Q\).

The expanded one-line integral uses continuous-time shorthand such as
\(\mathbf W_t^Q(\tau)\), \(\mathbf Y_t^Q(\tau)\), and
\(\mathcal K_t^Q(\tau)\). Each denotes the latest discrete snapshot available
at the solver evaluation corresponding to flow time \(\tau\).

Run build_assets.sh from this directory to rebuild the sheet and all formula
tiles.
