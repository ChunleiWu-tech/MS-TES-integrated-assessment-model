param([switch]$SkipSetup)
$ErrorActionPreference = 'Stop'
$modelRoot = $PSScriptRoot
$modelPython = Join-Path $modelRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $modelPython)) {
    if ($SkipSetup) { throw 'The local .venv is missing. Run without -SkipSetup.' }
    py -3.12 -m venv (Join-Path $modelRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Install 64-bit Python 3.12 first.' }
}
if (-not $SkipSetup) {
    & $modelPython -m pip install -r (Join-Path $modelRoot 'upstream_reproducible_code\requirements-lock.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
}
& $modelPython -X utf8 -u (Join-Path $modelRoot 'upstream_reproducible_code\src\run_pipeline.py') --mode full
if ($LASTEXITCODE -ne 0) { throw 'Upstream workflow failed; inspect its outputs\qc.' }
& $modelPython -X utf8 -u (Join-Path $modelRoot 'postprocess_reproducible_code\src\run_pipeline.py') --upstream-root (Join-Path $modelRoot 'upstream_reproducible_code')
if ($LASTEXITCODE -ne 0) { throw 'Postprocessing failed; inspect its outputs\qc.' }
& $modelPython -X utf8 -u (Join-Path $modelRoot 'RECOMPUTE_NUMERICAL_AUDIT.py') --project-root $modelRoot --output (Join-Path $modelRoot 'recomputed_numerical_audit')
if ($LASTEXITCODE -ne 0) { throw 'Targeted numerical audit failed; inspect recomputed_numerical_audit.' }
Write-Output 'Full 20,000-draw model and postprocessing completed. Final figures are in postprocess_reproducible_code\outputs.'
