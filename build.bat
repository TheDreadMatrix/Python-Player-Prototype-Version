@echo off
setlocal

echo === Building project with PyInstaller ===

REM Clean previous builds
if exist build (
    rmdir /s /q build
)

if exist dist (
    rmdir /s /q dist
)

if exist main.spec (
    del /f /q main.spec
)

echo Running PyInstaller...

pyinstaller ^
    --onefile ^
    --noconsole ^
    --name MyGame ^
    --icon=icon.ico ^
    --distpath . ^
    --add-data "icon.ico;." ^
    --add-data "assets;assets" ^
    --add-data "shaders;shaders" ^
    --add-data "soundtracks;soundtracks" ^
    main.py

REM Copy to Desktop
set "DESKTOP=%USERPROFILE%\Desktop"

copy /Y "MyGame.exe" "%DESKTOP%\MyGame.exe"

REM Cleanup
if exist build (
    rmdir /s /q build
)

if exist MyGame.spec (
    del /f /q MyGame.spec
)

echo === Build completed successfully ===
echo Output: MyGame.exe

pause