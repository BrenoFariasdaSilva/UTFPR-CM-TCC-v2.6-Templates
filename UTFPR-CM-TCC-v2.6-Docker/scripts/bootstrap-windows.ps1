# Bootstrap Python from Windows Package Manager when necessary. No permanent execution-policy change.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$python = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -c "import sys; assert sys.version_info >= (3,9)" 2>$null
    if ($LASTEXITCODE -eq 0) { $python = 'py' }
}
if (-not $python -and (Get-Command python -ErrorAction SilentlyContinue)) {
    & python -c "import sys; assert sys.version_info >= (3,9)" 2>$null
    if ($LASTEXITCODE -eq 0) { $python = 'python' }
}
if (-not $python) {
    Write-Host 'Python 3.9+ is required. Installing via Windows Package Manager.'
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'winget is missing; update App Installer from Microsoft Store.' }
    & winget install --id Python.Python.3.14 --exact --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw 'Python installation failed.' }
    $candidates = @("$env:LOCALAPPDATA\Programs\Python\Python314\python.exe", "$env:ProgramFiles\Python314\python.exe")
    foreach ($candidate in $candidates) { if (Test-Path $candidate) { $python = $candidate; break } }
    if (-not $python) { throw 'Python was installed but is not accessible yet. Reopen Windows Terminal and retry.' }
}
if ($python -eq 'py') { & py -3 'scripts/compile.py' compile @args }
else { & $python 'scripts/compile.py' compile @args }
exit $LASTEXITCODE
