[Setup]
AppName=AIterEgo
AppVersion=1.1.0
AppPublisher=JJaroll
DefaultDirName={autopf}\AIterEgo
DefaultGroupName=AIterEgo
UninstallDisplayIcon={app}\AIterEgo.exe
SetupIconFile=assets\app_icon.ico
OutputDir=Output
OutputBaseFilename=setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\AIterEgo\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\AIterEgo"; Filename: "{app}\AIterEgo.exe"
Name: "{group}\Uninstall AIterEgo"; Filename: "{uninstallexe}"
Name: "{autodesktop}\AIterEgo"; Filename: "{app}\AIterEgo.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el Escritorio"; GroupDescription: "Accesos directos adicionales:"

[Run]
Filename: "{app}\AIterEgo.exe"; Description: "Iniciar AIterEgo"; Flags: nowait postinstall skipifsilent
