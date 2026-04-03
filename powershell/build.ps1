$ErrorActionPreference = "Stop"

Write-Host "=== Building project with PyInstaller ===" -ForegroundColor Yellow

# Clean previous builds
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "MyGame.spec") {
    Remove-Item -Force "MyGame.spec"
}

Write-Host "Running PyInstaller..." -ForegroundColor Green

pyinstaller `
    --onefile `
    --noconsole `
    --name MyGame `
    --icon=icon.ico `
    --distpath . `
    --add-data "icon.ico;." `
    --add-data "assets;assets" `
    --add-data "shaders;shaders" `
    --add-data "soundtracks;soundtracks" `
    main.py

$desktop = [Environment]::GetFolderPath("Desktop")

Copy-Item "MyGame.exe" "$desktop\MyGame.exe" -Force

#CREATING ROOT DIRECTORY
$dest = "$env:APPDATA\.kartoshkaData"
$src = ".\data"

New-Item -ItemType Directory -Path $dest -Force

Copy-Item $src $dest -Recurse -Force


#DELETE UNNECESSERERY FOLDERS AND FILES
Remove-Item -Recurse -Force build
Remove-Item MyGame.spec
Write-Host "=== Build completed successfully ===" -ForegroundColor Green
Write-Host "Output: MyGame.exe" -ForegroundColor Green