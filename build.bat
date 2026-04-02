$ErrorActionPreference = "Stop"

Write-Host "=== Building project with PyInstaller ==="

# Clean previous builds
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "main.spec") {
    Remove-Item -Force "main.spec"
}

Write-Host "Running PyInstaller..."

pyinstaller `
    --onefile `
    --noconsole `
    --name MyGame `
    --icon=icon.ico `
    --add-data "icon.ico;." `
    --add-data "assets;assets" `
    --add-data "shaders;shaders" `
    --add-data "data;data" `
    --add-data "soundtracks;soundtracks" `
    main.py

$desktop = [Environment]::GetFolderPath("Desktop")

Copy-Item "dist\MyGame.exe" "$desktop\MyGame.exe" -Force

Remove-Item -Recurse -Force build
Remove-Item MyGame.spec
Write-Host "=== Build completed successfully ==="
Write-Host "Output: dist/main.exe"