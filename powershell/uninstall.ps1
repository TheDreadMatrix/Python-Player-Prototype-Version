$path = "$env:APPDATA\.kartoshkaData"

if (Test-Path $path) {
    Remove-Item $path -Recurse -Force
    Write-Host "Folder removed: $path"
} else {
    Write-Host "Folder not found: $path"
}