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

[Languages]
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "ja"; MessagesFile: "compiler:Languages\Japanese.isl"

[CustomMessages]
; --- Textos en Español ---
es.HwTitle=Aceleración de Hardware
es.HwSubTitle=Seleccione el motor de inferencia
es.HwDesc=Por favor seleccione si desea utilizar la GPU (NVIDIA) o solamente la CPU para el análisis emocional.
es.HwGPU=Modo GPU (NVIDIA RTX / GTX)
es.HwCPU=Modo CPU (Máxima compatibilidad)
es.RunGPU=Instalar componentes IA (Modo GPU)
es.RunCPU=Instalar componentes IA (Modo CPU)

; --- Textos en Inglés ---
en.HwTitle=Hardware Acceleration
en.HwSubTitle=Select the inference engine
en.HwDesc=Please select whether you want to use the GPU (NVIDIA) or only the CPU for emotional analysis.
en.HwGPU=GPU Mode (NVIDIA RTX / GTX)
en.HwCPU=CPU Mode (Maximum compatibility)
en.RunGPU=Install AI components (GPU Mode)
en.RunCPU=Install AI components (CPU Mode)

; --- Textos en Japonés ---
ja.HwTitle=ハードウェア・アクセラレーション
ja.HwSubTitle=推論エンジンの選択
ja.HwDesc=感情分析にGPU（NVIDIA）を使用するか、CPUのみを使用するかを選択してください。
ja.HwGPU=GPUモード (NVIDIA RTX / GTX)
ja.HwCPU=CPUモード (最大限の互換性)
ja.RunGPU=AIコンポーネントのインストール (GPUモード)
ja.RunCPU=AIコンポーネントのインストール (CPUモード)

[Run]
Filename: "{app}\install_env.bat"; Parameters: "GPU"; WorkingDir: "{app}"; Flags: postinstall runascurrentuser waituntilterminated; Description: "{cm:RunGPU}"; Check: IsGPUMode
Filename: "{app}\install_env.bat"; Parameters: "CPU"; WorkingDir: "{app}"; Flags: postinstall runascurrentuser waituntilterminated; Description: "{cm:RunCPU}"; Check: IsCPUMode

[Code]
// 1. Variables globales
var
  SelectHardwarePage: TInputOptionWizardPage;

// 2. Inicialización de la interfaz del instalador
procedure InitializeWizard;
begin
  SelectHardwarePage := CreateInputOptionPage(wpSelectDir,
    CustomMessage('HwTitle'), CustomMessage('HwSubTitle'),
    CustomMessage('HwDesc'),
    True, False);
  SelectHardwarePage.Add(CustomMessage('HwGPU'));
  SelectHardwarePage.Add(CustomMessage('HwCPU'));
  SelectHardwarePage.SelectedValueIndex := 1;
end;

// 3. Funciones de verificación de Hardware
function IsGPUMode: Boolean;
begin
  Result := (SelectHardwarePage.SelectedValueIndex = 0);
end;

function IsCPUMode: Boolean;
begin
  Result := (SelectHardwarePage.SelectedValueIndex = 1);
end;

// 4. Lógica de finalización (Generación del JSON multiidioma)
procedure CurStepChanged(CurStep: TSetupStep);
var
  JsonPath: String;
  JsonContent: String;
  LangCode: String;
  AiModel: String;
begin
  // Ejecutar esto solo en el paso final post-instalación
  if CurStep = ssPostInstall then
  begin
    JsonPath := ExpandConstant('{app}\config.json');
    LangCode := ExpandConstant('{language}');

    // Lógica para asignar el modelo de IA dependiendo del idioma
    if LangCode = 'es' then
    begin
      AiModel := 'spanish';
    end
    else
    begin
      AiModel := 'english';
    end;

    // Solo crear el JSON si NO existe (para proteger configuraciones previas al actualizar)
    if not FileExists(JsonPath) then
    begin
      // Construir el JSON inyectando las variables LangCode y AiModel
      JsonContent := '{' + #13#10 +
        '    "current_profile": "Default",' + #13#10 +
        '    "bounce_enabled": true,' + #13#10 +
        '    "bounce_amplitude": 10,' + #13#10 +
        '    "bounce_speed": 0.3,' + #13#10 +
        '    "shadow_enabled": true,' + #13#10 +
        '    "is_muted": false,' + #13#10 +
        '    "background_color": "rgba(0, 0, 0, 100)",' + #13#10 +
        '    "microphone_index": null,' + #13#10 +
        '    "enable_hotkeys": true,' + #13#10 +
        '    "hotkeys": {' + #13#10 +
        '        "mute_toggle": "m",' + #13#10 +
        '        "ai_mode": "x",' + #13#10 +
        '        "neutral": "1",' + #13#10 +
        '        "disgust": "2",' + #13#10 +
        '        "fear": "3",' + #13#10 +
        '        "happiness": "4",' + #13#10 +
        '        "sadness": "5",' + #13#10 +
        '        "anger": "6",' + #13#10 +
        '        "surprise": "7"' + #13#10 +
        '    },' + #13#10 +
        '    "mic_sensitivity": 1.0,' + #13#10 +
        '    "audio_threshold": 0.02,' + #13#10 +
        '    "check_updates": true,' + #13#10 +
        '    "language": "' + LangCode + '",' + #13#10 +
        '    "theme": "colorblind",' + #13#10 +
        '    "always_on_top": true,' + #13#10 +
        '    "tutorial_completed": false,' + #13#10 +
        '    "settings_window_size": [' + #13#10 +
        '        700,' + #13#10 +
        '        600' + #13#10 +
        '    ],' + #13#10 +
        '    "ai_model": "' + AiModel + '"' + #13#10 +
        '}';

      // Guardar el string en el archivo config.json
      SaveStringToFile(JsonPath, JsonContent, False);
    end;
  end;
end;