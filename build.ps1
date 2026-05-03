$ErrorActionPreference = "Stop"

Write-Host "=== Building project with PyInstaller ===" -ForegroundColor Yellow

# Clean previous builds
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "SuperMarioWorld.spec") {
    Remove-Item -Force "SuperMarioWorld.spec"
}

Write-Host "Running PyInstaller..." -ForegroundColor Green

pyinstaller `
    --onefile `
    --noconsole `
    --name SuperMarioWorld `
    --icon=icon.ico `
    --version-file version.txt `
    --distpath . `
    --add-data "assets;assets" `
    main.py

$desktop = [Environment]::GetFolderPath("Desktop")

Copy-Item "SuperMarioWorld.exe" "$desktop\SuperMarioWorld.exe" -Force

#CREATING ROOT DIRECTORY
$dest = "$env:APPDATA\.supermarioworld"
$src = ".\assets\data"

New-Item -ItemType Directory -Path $dest -Force

Copy-Item $src $dest -Recurse -Force


#DELETE UNNECESSERERY FOLDERS AND FILES
Remove-Item -Recurse -Force build
Remove-Item SuperMarioWorld.spec
Write-Host "=== Build completed successfully ===" -ForegroundColor Green
Write-Host "Output: MyGame.exe" -ForegroundColor Green