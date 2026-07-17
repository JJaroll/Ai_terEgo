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
Source: "*.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "install_env.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "python-embed.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "avatars\*"; DestDir: "{app}\avatars"; Flags: ignoreversion recursesubdirs

[Icons]
; NOTA: Apuntamos al Python del venv creado por el .bat para asegurar que use las librerías instaladas
Name: "{group}\AIterEgo"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; IconFilename: "{app}\assets\app_icon.ico"
Name: "{group}\Uninstall AIterEgo"; Filename: "{uninstallexe}"
Name: "{autodesktop}\AIterEgo"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon

[Run]
; Ejecutar el .bat dependiendo de la selección del usuario
Filename: "{app}\install_env.bat"; Parameters: "GPU"; Flags: postinstall runascurrentuser shellexec waituntilterminated; Description: "Instalar componentes IA (Modo GPU)"; Check: SelectHardwarePage.SelectedValueIndex = 0
Filename: "{app}\install_env.bat"; Parameters: "CPU"; Flags: postinstall runascurrentuser shellexec waituntilterminated; Description: "Instalar componentes IA (Modo CPU)"; Check: SelectHardwarePage.SelectedValueIndex = 1

[Code]
var
  SelectHardwarePage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  // Página personalizada para elegir Hardware (se muestra después de elegir ruta)
  SelectHardwarePage := CreateInputOptionPage(wpSelectDir,
    'Aceleración de Hardware', 'Seleccione el motor de inferencia',
    'Por favor seleccione si desea utilizar la GPU (NVIDIA) o solamente la CPU para el análisis emocional.',
    True, False);
  SelectHardwarePage.Add('Modo GPU (NVIDIA RTX / GTX)');
  SelectHardwarePage.Add('Modo CPU (Máxima compatibilidad)');
  SelectHardwarePage.SelectedValueIndex := 1; // CPU por defecto
end;