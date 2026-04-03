
$desktop = [Environment]::GetFolderPath("Desktop")

Copy-Item "MyGame.exe" "$desktop\MyGame.exe" -Force

$dest = "$env:APPDATA\.kartoshkaData"
$src = ".\data"

New-Item -ItemType Directory -Path $dest -Force

Copy-Item $src $dest -Recurse -Force

Write-Host "Output: MyGame.exe" -ForegroundColor Green