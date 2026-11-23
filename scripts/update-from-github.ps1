[CmdletBinding()]
param(
    [string]$Remote = "origin",
    [string]$Branch = "work/sanad-phase-1-foundation"
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

if (-not (Test-Path (Join-Path $root ".git"))) {
    throw "This folder is not a Git working copy. Clone the repository once before using this updater."
}

$dirty = git status --porcelain
$blockingDirty = @($dirty | Where-Object { $_ -and ($_ -notmatch "backend/sanad\.db$") })
if ($blockingDirty) {
    Write-Host "Local changes detected. Commit or stash them before updating:" -ForegroundColor Yellow
    $blockingDirty
    exit 2
}

if ($dirty | Where-Object { $_ -match "backend/sanad\.db$" }) {
    Write-Host "Ignoring local backend/sanad.db changes; GitHub version will be used." -ForegroundColor Yellow
    git restore --staged --worktree -- backend/sanad.db
}

git fetch $Remote $Branch
$before = git rev-parse HEAD
git pull --ff-only $Remote $Branch
$after = git rev-parse HEAD

if ($before -eq $after) {
    Write-Host "Already up to date ($after)." -ForegroundColor Green
    exit 0
}

$changed = git diff --name-only $before $after
if ($changed -contains "package-lock.json" -or $changed -contains "package.json") {
    Write-Host "Frontend dependencies changed; running npm.cmd ci..." -ForegroundColor Cyan
    npm.cmd ci
}

if ($changed | Where-Object { $_ -eq "backend/requirements.txt" }) {
    $python = Join-Path $root "backend\.venv\Scripts\python.exe"
    if (Test-Path $python) {
        & $python -m pip install -r (Join-Path $root "backend\requirements.txt")
    } else {
        Write-Host "Backend requirements changed. Recreate backend\.venv or install requirements manually." -ForegroundColor Yellow
    }
}

Write-Host "Updated from $before to $after." -ForegroundColor Green
