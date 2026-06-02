param(
    [switch]$NoClean
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$ExePath = Join-Path $RepoRoot "dist\MaskingTool.exe"
$SpecPath = Join-Path $RepoRoot "packaging\MaskingTool.spec"

Set-Location $RepoRoot

python -c "import PyInstaller" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller is not installed. Run: python -m pip install -e .[test,build]"
    exit $LASTEXITCODE
}

if (-not $NoClean) {
    if (Test-Path $ExePath) {
        Remove-Item -LiteralPath $ExePath -Force
    }
}

python -m PyInstaller --noconfirm --clean $SpecPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller build failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

if (-not (Test-Path $ExePath -PathType Leaf)) {
    Write-Error "Expected executable was not created: $ExePath"
    exit 1
}

Write-Host "Created $ExePath"
