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
; Archivos fuente y scripts de entorno
Source: "*.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "install_env.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "python-embed.zip"; DestDir: "{app}"; Flags: ignoreversion

; Assets y avatares con recursión para mantener la estructura de subcarpetas
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "avatars\*"; DestDir: "{app}\avatars"; Flags: ignoreversion recursesubdirs

[Icons]
; Acceso directo en el menú de inicio
Name: "{group}\AIterEgo"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\app_icon.ico"

; Acceso directo en el escritorio
Name: "{autodesktop}\AIterEgo"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\install_env.bat"; Parameters: "GPU"; WorkingDir: "{app}"; Flags: postinstall runascurrentuser waituntilterminated; Description: "Instalar componentes IA (Modo GPU)"; Check: IsGPUMode
Filename: "{app}\install_env.bat"; Parameters: "CPU"; WorkingDir: "{app}"; Flags: postinstall runascurrentuser waituntilterminated; Description: "Instalar componentes IA (Modo CPU)"; Check: IsCPUMode
[Code]
var
  SelectHardwarePage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  SelectHardwarePage := CreateInputOptionPage(wpSelectDir,
    'Aceleración de Hardware', 'Seleccione el motor de inferencia',
    'Por favor seleccione si desea utilizar la GPU (NVIDIA) o solamente la CPU para el análisis emocional.',
    True, False);
  SelectHardwarePage.Add('Modo GPU (NVIDIA RTX / GTX)');
  SelectHardwarePage.Add('Modo CPU (Máxima compatibilidad)');
  SelectHardwarePage.SelectedValueIndex := 1;
end;

// Funciones auxiliares para la directiva Check
function IsGPUMode: Boolean;
begin
  Result := (SelectHardwarePage.SelectedValueIndex = 0);
end;

function IsCPUMode: Boolean;
begin
  Result := (SelectHardwarePage.SelectedValueIndex = 1);
end;