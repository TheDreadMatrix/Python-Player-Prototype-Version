SUPER MANTIS WORLD 91 - DaemonDuck16


main.py


games/ <- output directory for exe

The command prompt build

# Main

pyinstaller `
    --onedir `
    --noconsole `
    --name WhatADaemonWorld `
    --icon=assets/icon.ico `
    --version-file version.txt `
    --distpath games `
    --add-data "assets;assets" `
    --add-binary "soloud_x64.dll;." `
    main.py


# Overworld editor

pyinstaller `
    --onedir `
    --noconsole `
    --name DaemonOverworldEditor `
    --icon=assets/icon.ico `
    --version-file version.txt `
    --distpath games `
    --add-data "assets;assets" `
    --add-binary "soloud_x64.dll;." `
    overworld_main.py