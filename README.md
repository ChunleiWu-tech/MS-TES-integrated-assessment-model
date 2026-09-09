# MS-TES integrated assessment model

TES-EES-V2.2.0-20260909

Composition-specific, complete-duty evidence determines which molten salts can be compared. Charge, delivery, capacity and pumping constraints determine whether material enhancement changes the storage requirement. Nanoparticle fluids and stationary scaffold composites retain their distinct evidence and operating domains.

## Reproduce the analysis

Extract both source ZIPs into one directory. Keep upstream_reproducible_code and postprocess_reproducible_code as siblings, with RUN_ALL.ps1 and RECOMPUTE_NUMERICAL_AUDIT.py beside them. Install 64-bit Python 3.12 and a licensed local Arial font. Run `powershell -File .\RUN_ALL.ps1`. The first run installs pinned dependencies. Later runs may use `-SkipSetup`. If script policy blocks this command, use the documented Python entry points or an approved local execution procedure.

The full workflow runs 41 upstream stages with 20,000 Monte Carlo draws per duty, 11 post-processing stages and an additional numerical audit. It reconstructs six main figures and seventeen supplementary figures as vector PDFs and 600 dpi PNGs. Generated outputs are replaced on rerun; do not store personal files in output folders. Source archives exclude virtual environments, generated results and proprietary fonts.

## Evidence and validation

Decision provenance includes 994 composition-duty outcomes, 216 engineering criterion assessments, 216 score-interval records and experimental-condition links. All 720,000 primary utility values are reconstructed. The evidence indices are declared assessment assumptions, not measured corrosion rates, lifetimes or failure probabilities. Formal qualification gates remain separate from continuous ranking.

An independent Solar Salt calorimetry source is compared with the unchanged property model over 250–400 °C. Model and observed enthalpy increments are 232.50 and 223.85 kJ kg⁻¹, respectively, giving +3.86% energy error and −3.72% fixed-energy mass error. The nine supported measurements yield 36 dependent interval diagnostics, all retained. Its scope is the specific-energy estimate and material-mass consequence for Solar Salt over the tested interval. The three-chloride masking calculation is retrospective. The 162 chronological cases test numerical consistency within the stated lossless, constant-power model.
