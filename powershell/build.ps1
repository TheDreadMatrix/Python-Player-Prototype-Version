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
    --distpath games `
    --add-data "assets;assets" `
    main.py



#CREATING ROOT DIRECTORY
$desktop = [Environment]::GetFolderPath("Desktop")

$exe = ".\games\SuperMarioWorld.exe"
$dest = "$env:APPDATA\.superkartoshkaworld"

New-Item -ItemType Directory -Path $dest -Force | Out-Null

Copy-Item $exe "$dest\SuperMarioWorld.exe" -Force

# assets
Copy-Item ".\assets\config" $dest -Recurse -Force
Copy-Item ".\assets\csaves" $dest -Recurse -Force

$target = "$dest\SuperMarioWorld.exe"
$shortcut = "$desktop\SuperMarioWorld.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$sc = $WshShell.CreateShortcut($shortcut)

$sc.TargetPath = $target
$sc.WorkingDirectory = $dest
$sc.IconLocation = $target
$sc.Save()


#DELETE UNNECESSERERY FOLDERS AND FILES
Remove-Item -Recurse -Force build
Remove-Item SuperMarioWorld.spec
Write-Host "=== Build completed successfully ===" -ForegroundColor Green
Write-Host "Output: MyGame.exe" -ForegroundColor Green