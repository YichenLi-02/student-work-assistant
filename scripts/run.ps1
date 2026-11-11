# Install the locked dependencies, build the frontend, then serve everything on :8000.
param([switch]$SetupOnly)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root 'src\backend'
$frontend = Join-Path $root 'src\frontend'
$python = Join-Path $backend '.venv\Scripts\python.exe'

function Invoke-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed (exit $LASTEXITCODE): $Executable $($Arguments -join ' ')"
    }
}

# Checking the executable also recovers a partially created virtual environment.
if (-not (Test-Path -LiteralPath $python)) {
    Invoke-Checked -Executable 'python' -Arguments @('-m', 'venv', (Join-Path $backend '.venv'))
}
# Always check dependencies: an interrupted install must be repairable on the next run.
Invoke-Checked -Executable $python -Arguments @(
    '-m', 'pip', 'install', '--disable-pip-version-check',
    '-r', (Join-Path $backend 'requirements-dev.txt'),
    '-c', (Join-Path $backend 'requirements.lock')
)

Push-Location $frontend
try {
    Invoke-Checked -Executable 'npm.cmd' -Arguments @('ci', '--no-audit', '--no-fund')
    Invoke-Checked -Executable 'npm.cmd' -Arguments @('run', 'build')
}
finally { Pop-Location }

if ($SetupOnly) {
    Write-Output 'Setup complete. Run without -SetupOnly to start the application.'
    return
}
Push-Location $backend
try {
    Invoke-Checked -Executable $python -Arguments @(
        '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'
    )
}
finally { Pop-Location }
