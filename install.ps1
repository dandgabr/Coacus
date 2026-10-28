<#
.SYNOPSIS
  Coacus Universal Bootstrap Installer (Windows PowerShell)
  Verifies Python 3.12+, installs it if missing, creates a .venv,
  renders artifacts and installs Coacus into harnesses.

.PARAMETER TargetHarness
  Target harness to install into (e.g. antigravity, opencode, codex, cursor, command-code, claude-code, claude-desktop, or all). Default is 'all'.
#>

[CmdletBinding()]
param (
    [string]$TargetHarness = "all"
)

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Coacus Universal Bootstrap Installer (Windows)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 1. Detect Python 3.12+
$PythonBin = $null
$PythonArgs = @()
$Candidates = @(
    @{ Command = "python"; Arguments = @() },
    @{ Command = "python3"; Arguments = @() },
    @{ Command = "py"; Arguments = @("-3") },
    @{ Command = "py"; Arguments = @("-3.14") },
    @{ Command = "py"; Arguments = @("-3.13") },
    @{ Command = "py"; Arguments = @("-3.12") }
)

function Find-CompatiblePython {
    foreach ($candidate in $Candidates) {
        $cmd = $candidate.Command
        $candidateArgs = $candidate.Arguments
        $found = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($found) {
            try {
                $ver = & $cmd @candidateArgs -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
                if ($ver) {
                    $parts = $ver.Split('.')
                    if ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 12) {
                        $script:PythonBin = $cmd
                        $script:PythonArgs = $candidateArgs
                        Write-Host "[OK] Detected compatible Python: $PythonBin ($ver)" -ForegroundColor Green
                        return $true
                    }
                }
            } catch { }
        }
    }
    return $false
}

# 2. Install Python if missing
if (-not (Find-CompatiblePython)) {
    Write-Host "[WARN] No Python >= 3.12 detected on PATH." -ForegroundColor Yellow
    Write-Host "Attempting to install Python via winget / choco..." -ForegroundColor Yellow

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Using winget to install Python 3.12..." -ForegroundColor Cyan
        winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-Host "Using Chocolatey to install python3..." -ForegroundColor Cyan
        choco install python3 -y
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        Write-Error "[ERROR] Could not automatically install Python 3.12+. Please install Python manually from python.org."
        exit 1
    }
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    if (-not (Find-CompatiblePython)) {
        Write-Error "[ERROR] No Python 3.12+ was found after installation. Install it manually and retry."
        exit 1
    }
}

& $PythonBin @PythonArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Error "Python 3.12+ is required for the language gate."; exit 1 }

# 3. Create or reuse virtual environment (.venv)
$VenvDir = Join-Path $ScriptDir ".venv"
$VenvPy = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvPy)) {
    Write-Host "Creating virtual environment at $VenvDir..." -ForegroundColor Cyan
    & $PythonBin @PythonArgs -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& $VenvPy -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Error "Existing .venv requires Python 3.12+. Recreate it with a compatible interpreter."; exit 1 }

Write-Host "Installing language-gate dependencies..." -ForegroundColor Cyan
& $VenvPy -m pip install --disable-pip-version-check "lingua-language-detector==2.2.0" "wordfreq==3.1.1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 4. Generate all Coacus artifacts
Write-Host "Rendering Coacus artifacts..." -ForegroundColor Cyan
& $VenvPy "scripts/coacus.py" generate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 5. Run installation into target harness(es)
Write-Host "Installing Coacus into harness: $TargetHarness..." -ForegroundColor Cyan
& $VenvPy "scripts/coacus_install.py" $TargetHarness --verify-after-install
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "====================================================" -ForegroundColor Green
Write-Host "[OK] Coacus installation and verification completed successfully!" -ForegroundColor Green
Write-Host "Virtual environment ready at: $VenvDir" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
