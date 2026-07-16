[Setup]
AppName=AIterEgo
AppVersion=1.1.0
AppPublisher=JJaroll
DefaultDirName={autopf}\AIterEgo
DefaultGroupName=AIterEgo
UninstallDisplayIcon={app}\assets\app_icon.ico
SetupIconFile=assets\app_icon.ico
OutputDir=Output
OutputBaseFilename=AIterEgo_Windows_WebInstaller
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el Escritorio"; GroupDescription: "Accesos directos adicionales:"

[Files]
; Copiar código fuente y herramientas del Web Installer
Source: "*.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "install_env.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "python-embed.zip"; DestDir: "{app}"; Flags: ignoreversion

; Copiar carpetas de recursos
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "avatars\*"; DestDir: "{app}\avatars"; Flags: ignoreversion recursesubdirs

[Icons]
; Crear accesos directos en el Menú Inicio y Escritorio usando el Python Portable
Name: "{group}\AIterEgo"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\main.py"""; IconFilename: "{app}\assets\app_icon.ico"
Name: "{group}\Uninstall AIterEgo"; Filename: "{uninstallexe}"
Name: "{autodesktop}\AIterEgo"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\main.py"""; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon

[Run]
; Ejecutar el .bat automáticamente al terminar la instalación
Filename: "{app}\install_env.bat"; Description: "Descargar componentes de Inteligencia Artificial (Requiere Internet)"; Flags: postinstall runascurrentuser shellexec waituntilterminated