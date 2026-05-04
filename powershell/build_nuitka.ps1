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

$exe = ".\SuperNuitkaWorld.exe"
$dest = "$env:APPDATA\.supernuitkaworld"

New-Item -ItemType Directory -Path $dest -Force | Out-Null

Copy-Item $exe "$dest\SuperNuitkaWorld.exe" -Force

# assets
Copy-Item ".\assets\config" $dest -Recurse -Force
Copy-Item ".\assets\csaves" $dest -Recurse -Force

$target = "$dest\SuperNuitkaWorld.exe"
$shortcut = "$desktop\SuperNuitkaWorld.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$sc = $WshShell.CreateShortcut($shortcut)

$sc.TargetPath = $target
$sc.WorkingDirectory = $dest
$sc.IconLocation = $target
$sc.Save()


Write-Host "=== Build completed successfully ===" -ForegroundColor Green
Write-Host "Output: SuperNuitkaWorld.exe" -ForegroundColor Green