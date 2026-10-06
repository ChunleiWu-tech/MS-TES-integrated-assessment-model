# MS-TES integrated assessment model

Current source release: **TES-EES-SCIENTIFIC-V5-PRESENTATION-V9-20261006**.
Scientific model V5 was evaluated on 4 October 2026; presentation V9 updates Figures 6–8 on 6 October 2026. The two source archives below are byte-identical to those in the verified local V9 integrated delivery.

The analysis connects exact-composition evidence and complete operating windows to engineering qualification, system constraints and cost constrained measurement planning. The current development uses existing data and published measurements.

## Download the current sources

| Component | Archive | Contents |
| --- | --- | --- |
| Upstream | [TES_MT_upstream_source_only.zip](TES_MT_upstream_source_only.zip) | Model code, configuration, curated inputs, source records and pinned dependencies |
| Postprocessing | [TES_MT_postprocess_source_only.zip](TES_MT_postprocess_source_only.zip) | Figure code, configuration, input records and pinned dependencies |

Verify the downloads with `python VERIFY_SOURCES.py`. Exact archive hashes are in [SHA256SUMS.txt](SHA256SUMS.txt). Extract both archives into one directory, keeping `upstream_reproducible_code` and `postprocess_reproducible_code` as siblings:

```text
python -m zipfile -e TES_MT_upstream_source_only.zip .
python -m zipfile -e TES_MT_postprocess_source_only.zip .
```

## Reproduce the calculations

Use 64-bit Python 3.12 and the pinned upstream dependencies, which also include the postprocessing requirements. In a Python virtual environment:

```text
python -m pip install -r upstream_reproducible_code/requirements-lock.txt
python upstream_reproducible_code/src/run_pipeline.py --mode full
```

The full upstream entry point contains 51 stages and uses 20,000 Monte Carlo worlds per duty. Generated outputs and environments are excluded from these source archives.

## Reproduce the publication figures

The postprocessing entry point has 16 stages. Its publication-figure stage also requires the sibling `EES_Submission_Package/Analysis_Scripts` directory and the `Active_Learning_Upgrade` companion, including their supporting data. These companions are supplied in the integrated submission delivery; the two source-only downloads do not contain all inputs for rebuilding all publication figures. The final presentation contains eight main and 31 supplementary figures.

With these integrated companions available, run:

```text
python postprocess_reproducible_code/src/run_pipeline.py --upstream-root ../upstream_reproducible_code
```

The recorded figure configuration uses a locally installed Arial font. Proprietary font files are not distributed. Preserve the extracted folder structure when using the integrated delivery.

## Scientific scope

The upstream extension includes positive nonincreasing density inference, identical fitting and calibration groups at nominal 90% and 95%, five source-allocation sensitivities, 72 policy comparisons under a common worst-case criterion, 1,026 ordinal-cost settings and hypothetical observation-error stress. Charging and release transfer are assessed separately using published device endpoints.

Density error improves in two of five allocations and worsens in three. Physically admissible predictions and source coverage are assessed separately from precision. Correlation-generated targets are identified as generated values. Exact robust policies outperform the exact point-policy worst-case value in five of 72 small instances; generated-process comparisons retain settings where robust planning performs worse. The device endpoints are dependent observations from two same-group publications. Predicted properties and generated certificate outcomes do not establish measured engineering qualification.

## Version and citation

Use [CITATION.cff](CITATION.cff) and report the release identifier and Git commit used. No release-specific DOI has been assigned to this V9 source publication. The [existing Zenodo record](https://doi.org/10.5281/zenodo.22673249) provides reference data and an earlier model; it is not presented as the archive of this V9 release. Third-party inputs retain their source-specific licences.

The previous source publication and its original instructions are preserved in [archive/TES-EES-V2.2.0-20260909](archive/TES-EES-V2.2.0-20260909). Use the current archives above for the V9 integrated delivery.
