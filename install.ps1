<#
.SYNOPSIS
  Coacus Universal Bootstrap Installer (Windows PowerShell)
  Verifies Python 3.10+, installs it if missing, creates a .venv,
  renders artifacts and installs Coacus into harnesses.

.PARAMETER TargetHarness
  Target harness to install into (e.g. antigravity, opencode, codex, cursor, command-code, or all). Default is 'all'.
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

# 1. Detect Python 3.10+
$PythonBin = $null
$Candidates = @("python", "py", "python3")

foreach ($cmd in $Candidates) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) {
        try {
            $ver = & $cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
            if ($ver) {
                $parts = $ver.Split('.')
                if ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 10) {
                    $PythonBin = $cmd
                    Write-Host "✔ Detected compatible Python: $PythonBin ($ver)" -ForegroundColor Green
                    break
                }
            }
        } catch { }
    }
}

# 2. Install Python if missing
if (-not $PythonBin) {
    Write-Host "⚠ No Python >= 3.10 detected on PATH." -ForegroundColor Yellow
    Write-Host "Attempting to install Python via winget / choco..." -ForegroundColor Yellow

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Using winget to install Python 3.12..." -ForegroundColor Cyan
        winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements
        # Refresh PATH in current session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $PythonBin = "python"
    } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        Write-Host "Using Chocolatey to install python3..." -ForegroundColor Cyan
        choco install python3 -y
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $PythonBin = "python"
    } else {
        Write-Error "❌ Error: Could not automatically install Python 3.10+. Please install Python manually from python.org."
        exit 1
    }
}

# 3. Create or reuse virtual environment (.venv)
$VenvDir = Join-Path $ScriptDir ".venv"
$VenvPy = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvPy)) {
    Write-Host "Creating virtual environment at $VenvDir..." -ForegroundColor Cyan
    & $PythonBin -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

# 4. Generate all Coacus artifacts
Write-Host "Rendering Coacus artifacts..." -ForegroundColor Cyan
& $VenvPy "scripts/coacus.py" generate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 5. Run installation into target harness(es)
Write-Host "Installing Coacus into harness: $TargetHarness..." -ForegroundColor Cyan
& $VenvPy "scripts/coacus_install.py" $TargetHarness --verify-after-install
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "====================================================" -ForegroundColor Green
Write-Host "✔ Coacus installation and verification completed successfully!" -ForegroundColor Green
Write-Host "Virtual environment ready at: $VenvDir" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
