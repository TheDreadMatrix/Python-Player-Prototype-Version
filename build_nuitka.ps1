$ErrorActionPreference = "Stop"

Write-Host "=== Building project with Nuitka ===" -ForegroundColor Yellow

# Clean previous builds
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "SuperNuitkaWorld.exe") {
    Remove-Item -Force "SuperNuitkaWorld.exe"
}

Write-Host "Running Nuitka..." -ForegroundColor Green

python -m nuitka `
    --onefile `
    --windows-console-mode=disable `
    --output-filename=SuperNuitkaWorld.exe `
    --windows-icon-from-ico=icon.ico `
    --include-data-dir=assets=assets `
    main.py

$desktop = [Environment]::GetFolderPath("Desktop")

Copy-Item "SuperNuitkaWorld.exe" "$desktop\SuperNuitkaWorld.exe" -Force

# CREATING ROOT DIRECTORY
$dest = "$env:APPDATA\.supernuitkaaworld"
$srcConfig = ".\assets\config"
$srcCsaves = ".\assets\csaves"

New-Item -ItemType Directory -Path $dest -Force | Out-Null

Copy-Item $srcConfig $dest -Recurse -Force
Copy-Item $srcCsaves $dest -Recurse -Force

Write-Host "=== Build completed successfully ===" -ForegroundColor Green
Write-Host "Output: SuperNuitkaWorld.exe" -ForegroundColor Green