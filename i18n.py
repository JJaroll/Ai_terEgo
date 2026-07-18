"""
(AI)terEgo - Internationalization (i18n)
-----------------------------------------
Sistema de traducciones de la interfaz: Español, Inglés y Japonés.
"""

__author__ = "JJaroll"
__version__ = "1.2.0"
__maintainer__ = "JJaroll"
__status__ = "Production"

from PyQt6.QtCore import QObject, pyqtSignal

LANGUAGES = {
    "es": "Español",
    "en": "English",
    "ja": "日本語",
}

DEFAULT_LANGUAGE = "es"

# Cada entrada: clave -> (español, inglés, japonés)
_STRINGS = {
    # --- Genéricos ---
    "common.close": ("Cerrar", "Close", "閉じる"),
    "common.cancel": ("Cancelar", "Cancel", "キャンセル"),
    "common.success": ("Éxito", "Success", "成功"),
    "common.error": ("Error", "Error", "エラー"),

    # --- Ventana de Configuración ---
    "settings.window_title": ("Configuración - (AI)terEgo", "Settings - (AI)terEgo", "設定 - (AI)terEgo"),
    "tab.audio": ("🎙️ Audio", "🎙️ Audio", "🎙️ 音声"),
    "tab.appearance": ("🎨 Apariencia", "🎨 Appearance", "🎨 外観"),
    "tab.avatar": ("👕 Avatar", "👕 Avatar", "👕 アバター"),
    "tab.hotkeys": ("⌨️ Atajos", "⌨️ Hotkeys", "⌨️ ショートカット"),
    "tab.system": ("💻 Sistema", "💻 System", "💻 システム"),
    "tab.about": ("ℹ️ Sobre", "ℹ️ About", "ℹ️ 情報"),

    # --- Audio ---
    "audio.device": ("Dispositivo:", "Device:", "デバイス:"),
    "audio.sensitivity": ("Sensibilidad:", "Sensitivity:", "感度:"),
    "audio.threshold": ("Umbral:", "Threshold:", "しきい値:"),
    "audio.test": ("Prueba de Audio:", "Audio Test:", "音声テスト:"),

    # --- Apariencia ---
    "appearance.bg_group": ("Color de Fondo", "Background Color", "背景色"),
    "appearance.bg.transparent": ("Transparente", "Transparent", "透明"),
    "appearance.bg.green": ("Verde (Chroma)", "Green (Chroma)", "緑(クロマキー)"),
    "appearance.bg.blue": ("Azul (Chroma)", "Blue (Chroma)", "青(クロマキー)"),
    "appearance.bg.semi": ("Semitransparente (Oscuro)", "Semi-transparent (Dark)", "半透明(暗)"),
    "appearance.bg.custom": ("Seleccionar Color:", "Select Color:", "色を選択:"),
    "appearance.pick_color": ("Elegir Color", "Choose Color", "色を選ぶ"),
    "appearance.color_dialog_title": ("Seleccionar Color de Fondo", "Select Background Color", "背景色を選択"),
    "appearance.shadow": ("Activar Sombra Suave", "Enable Soft Shadow", "ソフトシャドウを有効化"),
    "appearance.bounce_group": ("Animación de Rebote", "Bounce Animation", "バウンスアニメーション"),
    "appearance.bounce_enable": ("Activar Rebote", "Enable Bounce", "バウンスを有効化"),
    "appearance.bounce_force": ("Fuerza:", "Strength:", "強さ:"),
    "appearance.bounce_speed": ("Velocidad:", "Speed:", "速度:"),
    "appearance.theme_group": ("Tema", "Theme", "テーマ"),
    "theme.dark": ("Oscuro", "Dark", "ダーク"),
    "theme.light": ("Claro", "Light", "ライト"),
    "theme.high_contrast": ("Alto Contraste", "High Contrast", "ハイコントラスト"),
    "theme.colorblind": ("Daltónico", "Colorblind-friendly", "色覚サポート"),

    # --- Avatar ---
    "avatar.title": ("Gestión de Avatares", "Avatar Management", "アバター管理"),
    "avatar.hint": (
        "💡 Tip: Haz clic derecho en un avatar para cambiarle el nombre o eliminarlo.",
        "💡 Tip: Right-click an avatar to rename or delete it.",
        "💡 ヒント: アバターを右クリックすると名前の変更や削除ができます。",
    ),
    "avatar.rename": ("✏️ Cambiar Nombre", "✏️ Rename", "✏️ 名前を変更"),
    "avatar.edit_images": ("🖼️ Editar Imágenes", "🖼️ Edit Images", "🖼️ 画像を編集"),
    "avatar.delete_skin": ("🗑️ Eliminar Skin", "🗑️ Delete Skin", "🗑️ スキンを削除"),
    "avatar.create_new_count": (
        "+  Crear Nuevo Skin ({count}/{limit})",
        "+  Create New Skin ({count}/{limit})",
        "+  新しいスキンを作成 ({count}/{limit})",
    ),
    "avatar.limit_reached": (
        "⚠️ Límite de Skins Alcanzado ({count}/{limit})",
        "⚠️ Skin Limit Reached ({count}/{limit})",
        "⚠️ スキン数の上限に達しました ({count}/{limit})",
    ),
    "avatar.limit_tooltip": (
        "Has alcanzado el máximo de 12 skins. Elimina carpetas en 'avatars/' para crear más.",
        "You've reached the maximum of 12 skins. Delete folders in 'avatars/' to create more.",
        "スキンの上限(12個)に達しました。'avatars/'内のフォルダを削除すると追加作成できます。",
    ),
    "avatar.import": ("📥 Importar", "📥 Import", "📥 インポート"),
    "avatar.export": ("📤 Exportar", "📤 Export", "📤 エクスポート"),
    "avatar.rename_title": ("Renombrar Skin", "Rename Skin", "スキン名の変更"),
    "avatar.rename_label": ("Nuevo nombre para '{name}':", "New name for '{name}':", "'{name}' の新しい名前:"),
    "avatar.rename_success": ("Renombrado a '{name}'", "Renamed to '{name}'", "'{name}' に変更しました"),
    "avatar.delete_title": ("Eliminar Skin", "Delete Skin", "スキンを削除"),
    "avatar.delete_confirm": (
        "¿Estás seguro de que deseas eliminar permanentemente el skin '{name}'?\n\nEsta acción NO se puede deshacer.",
        "Are you sure you want to permanently delete the skin '{name}'?\n\nThis action CANNOT be undone.",
        "スキン '{name}' を完全に削除してもよろしいですか?\n\nこの操作は元に戻せません。",
    ),
    "avatar.deleted_title": ("Eliminado", "Deleted", "削除しました"),
    "avatar.deleted_msg": ("El skin '{name}' ha sido eliminado.", "The skin '{name}' has been deleted.", "スキン '{name}' を削除しました。"),

    # --- Atajos ---
    "hotkeys.description": (
        "Configura las teclas para activar emociones rápidamente.",
        "Configure keys to quickly trigger emotions.",
        "感情をすばやく切り替えるキーを設定します。",
    ),
    "hotkeys.col_action": ("Acción", "Action", "操作"),
    "hotkeys.col_key": ("Tecla Actual", "Current Key", "現在のキー"),
    "hotkeys.change_btn": ("✏️ Cambiar", "✏️ Change", "✏️ 変更"),
    "hotkeys.mute_toggle": ("🔇 Silenciar / Activar Micrófono", "🔇 Mute / Unmute Microphone", "🔇 マイクのミュート切替"),
    "hotkeys.ai_mode": ("🤖 Activar Modo Automático (IA)", "🤖 Enable Automatic Mode (AI)", "🤖 自動モード(AI)を有効化"),
    "hotkeys.neutral": ("😐 Emoción: Neutral", "😐 Emotion: Neutral", "😐 感情: ニュートラル"),
    "hotkeys.disgust": ("🤢 Emoción: Asco", "🤢 Emotion: Disgust", "🤢 感情: 嫌悪"),
    "hotkeys.fear": ("😨 Emoción: Miedo", "😨 Emotion: Fear", "😨 感情: 恐怖"),
    "hotkeys.happiness": ("😄 Emoción: Felicidad", "😄 Emotion: Happiness", "😄 感情: 喜び"),
    "hotkeys.sadness": ("😢 Emoción: Tristeza", "😢 Emotion: Sadness", "😢 感情: 悲しみ"),
    "hotkeys.anger": ("😡 Emoción: Enojo", "😡 Emotion: Anger", "😡 感情: 怒り"),
    "hotkeys.surprise": ("😲 Emoción: Sorpresa", "😲 Emotion: Surprise", "😲 感情: 驚き"),
    "hotkey_dialog.title": ("Grabando...", "Recording...", "記録中..."),
    "hotkey_dialog.label": ("Presiona una tecla ahora...", "Press a key now...", "今すぐキーを押してください..."),

    # --- Sistema ---
    "system.ai_group": ("Configuración de IA", "AI Configuration", "AI設定"),
    "system.voice_model": ("Modelo de Voz:", "Voice Model:", "音声モデル:"),
    "system.model_note": (
        "Nota: Cambiar el modelo puede requerir una descarga adicional (300MB - 1.2GB).",
        "Note: Changing the model may require an additional download (300MB - 1.2GB).",
        "注意: モデルを変更すると追加のダウンロードが必要になる場合があります(300MB〜1.2GB)。",
    ),
    "system.model_path": ("Ruta del Modelo:", "Model Path:", "モデルのパス:"),
    "system.model_not_downloaded": ("⚠️ Modelo no descargado", "⚠️ Model not downloaded", "⚠️ モデルが未ダウンロードです"),
    "system.loading_path": ("Cargando ruta...", "Loading path...", "パスを読み込み中..."),
    "system.open_in_explorer": ("Abrir en Explorador", "Open in File Explorer", "エクスプローラーで開く"),
    "system.emotions_supported": ("Emociones Soportadas:", "Supported Emotions:", "対応している感情:"),
    "system.emotions_label": ("Emociones: {emotions}", "Emotions: {emotions}", "感情: {emotions}"),
    "system.project_location": ("Ubicación del Proyecto", "Project Location", "プロジェクトの場所"),
    "system.open_folder": ("Abrir Carpeta", "Open Folder", "フォルダを開く"),
    "system.storage_group": ("Almacenamiento", "Storage", "ストレージ"),
    "system.check_updates": (
        "Buscar actualizaciones automáticamente al iniciar",
        "Automatically check for updates on startup",
        "起動時に自動的に更新を確認する",
    ),
    "system.calc_disabled": ("(Cálculo desactivado en App)", "(Calculation disabled in App)", "(アプリ内では計算が無効です)"),
    "system.hidden_perf": ("(Oculto por rendimiento)", "(Hidden for performance)", "(パフォーマンスのため非表示)"),
    "system.total_size": ("Peso Total (aprox):", "Total Size (approx):", "合計サイズ(概算):"),
    "system.files_count": ("Archivos:", "Files:", "ファイル数:"),
    "system.calc_status": ("Estado:", "Status:", "状態:"),
    "system.calc_error": ("Error de cálculo", "Calculation error", "計算エラー"),
    "system.env_group": ("Entorno de Ejecución", "Runtime Environment", "実行環境"),
    "system.os_label": ("Sistema Operativo:", "Operating System:", "オペレーティングシステム:"),
    "system.arch_label": ("Arquitectura:", "Architecture:", "アーキテクチャ:"),
    "system.python_version_label": ("Versión de Python:", "Python Version:", "Pythonのバージョン:"),
    "system.language_group": ("Idioma", "Language", "言語"),
    "system.language_label": ("Idioma de la aplicación:", "Application Language:", "アプリの言語:"),
    "system.window_group": ("Comportamiento de Ventana", "Window Behavior", "ウィンドウの動作"),
    "system.always_on_top": (
        "Mantener siempre visible (encima de otras ventanas)",
        "Always keep on top (above other windows)",
        "常に最前面に表示する(他のウィンドウの上に)",
    ),

    # --- Sobre ---
    "about.version": ("Versión {version}", "Version {version}", "バージョン {version}"),
    "about.version_unknown": ("Versión: Desconocida", "Version: Unknown", "バージョン: 不明"),
    "about.description": (
        "Un avatar virtual inteligente que reacciona a tu voz y emociones en tiempo real utilizando Inteligencia Artificial.",
        "A smart virtual avatar that reacts to your voice and emotions in real time using Artificial Intelligence.",
        "AIを使ってあなたの声や感情にリアルタイムで反応するスマートなバーチャルアバターです。",
    ),
    "about.developed_by": ("Desarrollado por <b>JJaroll</b>", "Developed by <b>JJaroll</b>", "開発者: <b>JJaroll</b>"),
    "about.powered_by": ("Powered by Python, PyQt6 & PyTorch", "Powered by Python, PyQt6 & PyTorch", "Powered by Python, PyQt6 & PyTorch"),
    "about.license": ("Distribuido bajo Licencia MIT", "Distributed under the MIT License", "MITライセンスの下で配布"),
    "about.support_kofi": ("☕ Apóyame en Ko-fi", "☕ Support me on Ko-fi", "☕ Ko-fiで応援する"),
    "about.view_github": ("  Ver en GitHub", "  View on GitHub", "  GitHubで見る"),
    "about.report_bug": ("🐛 Reportar un Problema", "🐛 Report an Issue", "🐛 問題を報告"),

    # --- Actualizaciones ---
    "update.badge_default": ("⬇️  Actualización Disponible", "⬇️  Update Available", "⬇️  アップデートあり"),
    "update.badge_found": ("⬇️  Actualización v{version} Disponible", "⬇️  Update v{version} Available", "⬇️  アップデート v{version} が利用可能"),
    "update.tray_title": ("Actualización Disponible", "Update Available", "アップデートがあります"),
    "update.tray_msg": ("La versión {version} está lista para descargar.", "Version {version} is ready to download.", "バージョン {version} がダウンロード可能です。"),
    "update.dialog_text": ("¡Nueva versión disponible!", "New version available!", "新しいバージョンがあります!"),
    "update.dialog_info": ("¿Quieres ir a la página de descarga ahora?", "Do you want to go to the download page now?", "今すぐダウンロードページを開きますか?"),

    # --- Bandeja del sistema ---
    "tray.toggle_visibility": ("Mostrar / Ocultar", "Show / Hide", "表示 / 非表示"),
    "tray.mute_mic": ("Silenciar Micrófono", "Mute Microphone", "マイクをミュート"),
    "tray.ai_mode": ("Modo IA activado", "AI Mode Enabled", "AIモード有効"),
    "tray.quit": ("Salir (Quit)", "Quit", "終了"),

    # --- Tooltips ventana principal ---
    "tooltip.mute": ("Silenciar / Activar Micrófono", "Mute / Unmute Microphone", "マイクのミュート切替"),
    "tooltip.flip": ("Voltear Avatar (Espejo)", "Flip Avatar (Mirror)", "アバターを反転(ミラー)"),
    "tooltip.settings": ("Abrir Configuración", "Open Settings", "設定を開く"),
    "tooltip.more_emotions": ("Ver más emociones", "Show more emotions", "他の感情を表示"),
    "tooltip.less_emotions": ("Menos emociones", "Fewer emotions", "感情を減らす"),
    "tooltip.ai_mode": ("Modo Automático", "Automatic Mode", "自動モード"),
    "tooltip.emotion_unavailable": ("{name} (No disponible)", "{name} (Unavailable)", "{name} (利用不可)"),

    "emotion.neutral": ("Neutral", "Neutral", "ニュートラル"),
    "emotion.happy": ("Feliz", "Happy", "幸せ"),
    "emotion.sad": ("Triste", "Sad", "悲しい"),
    "emotion.angry": ("Enojado", "Angry", "怒り"),
    "emotion.fear": ("Miedo", "Fear", "恐怖"),
    "emotion.disgust": ("Asco", "Disgust", "嫌悪"),
    "emotion.surprise": ("Sorpresa", "Surprise", "驚き"),

    "state.closed": ("Cerrada", "Closed", "閉じ"),
    "state.open": ("Abierta", "Open", "開き"),

    "app.tray_info_msg": (
        "La aplicación seguirá ejecutándose en la bandeja del sistema.",
        "The application will keep running in the system tray.",
        "アプリケーションはシステムトレイで実行され続けます。",
    ),

    # --- Descarga de modelo ---
    "download.title": ("Descargando Modelo IA", "Downloading AI Model", "AIモデルをダウンロード中"),
    "download.downloading": ("Descargando: {model}", "Downloading: {model}", "ダウンロード中: {model}"),
    "download.info": (
        "Esto puede tardar unos minutos dependiendo de tu internet (aprox. 300MB - 1GB). Por favor espera.",
        "This may take a few minutes depending on your internet connection (approx. 300MB - 1GB). Please wait.",
        "インターネット環境により数分かかる場合があります(約300MB〜1GB)。しばらくお待ちください。",
    ),
    "download.complete_title": ("Descarga Completada", "Download Complete", "ダウンロード完了"),
    "download.complete_msg": ("Modelo listo.", "Model ready.", "モデルの準備ができました。"),
    "download.error_title": ("Error Fatal", "Fatal Error", "致命的なエラー"),
    "download.error_msg": (
        "No se pudo descargar el modelo.\nError: {error}",
        "The model could not be downloaded.\nError: {error}",
        "モデルをダウンロードできませんでした。\nエラー: {error}",
    ),

    # --- Tutorial ---
    "tutorial.hint": ("Flip: Ctrl+F\nClick derecho: Menú", "Flip: Ctrl+F\nRight-click: Menu", "反転: Ctrl+F\n右クリック: メニュー"),
    "tutorial.controls": ("Controles", "Controls", "操作"),
    "tutorial.click_start": ("Haz clic para comenzar", "Click to begin", "クリックして開始"),

    # --- Menú contextual ---
    "menu.mute": ("🔇 Silenciar / Mute", "🔇 Mute", "🔇 ミュート"),
    "menu.background": ("🎨 Fondo / Background", "🎨 Background", "🎨 背景"),
    "menu.shadow": ("Sombra / Shadow", "Shadow", "影"),
    "menu.skins": ("👕 Skins / Avatares", "👕 Skins / Avatars", "👕 スキン / アバター"),
    "menu.bounce": ("🎾 Rebote / Bounce", "🎾 Bounce", "🎾 バウンス"),
    "menu.open_settings": ("⚙️ Abrir Configuración...", "⚙️ Open Settings...", "⚙️ 設定を開く..."),

    # --- Import/Export de Skins ---
    "skin.import_dialog_title": ("Importar Skin (.ptuber)", "Import Skin (.ptuber)", "スキンをインポート (.ptuber)"),
    "skin.import_success": ("Skin '{name}' importado correctamente.", "Skin '{name}' imported successfully.", "スキン '{name}' を正常にインポートしました。"),
    "skin.import_error": ("No se pudo importar: {error}", "Could not import: {error}", "インポートできませんでした: {error}"),
    "skin.export_dialog_title": ("Exportar Skin (.ptuber)", "Export Skin (.ptuber)", "スキンをエクスポート (.ptuber)"),
    "skin.export_success": ("Skin guardado en:\n{path}", "Skin saved to:\n{path}", "スキンを保存しました:\n{path}"),
    "skin.export_error": ("Error al exportar: {error}", "Export failed: {error}", "エクスポートに失敗しました: {error}"),
    "skin.filter": ("Perfil PNGTuber (*.ptuber)", "PNGTuber Profile (*.ptuber)", "PNGTuberプロファイル (*.ptuber)"),

    # --- Creador de perfiles ---
    "creator.edit_title": ("Editar Skin: {name}", "Edit Skin: {name}", "スキンを編集: {name}"),
    "creator.create_title": ("Crear Nuevo Skin de Avatar", "Create New Avatar Skin", "新しいアバタースキンを作成"),
    "creator.name_label": ("Nombre del Skin:", "Skin Name:", "スキン名:"),
    "creator.name_placeholder": ("Escribe el nombre aquí...", "Type the name here...", "ここに名前を入力..."),
    "creator.assign_images": ("Asigna las imágenes correspondientes:", "Assign the corresponding images:", "対応する画像を割り当ててください:"),
    "creator.no_image": ("❌ Sin imagen", "❌ No image", "❌ 画像なし"),
    "creator.current_image": ("✅ Actual", "✅ Current", "✅ 現在の画像"),
    "creator.new_image": ("✅ Nuevo: {filename}", "✅ New: {filename}", "✅ 新規: {filename}"),
    "creator.save_changes": ("💾 Guardar Cambios", "💾 Save Changes", "💾 変更を保存"),
    "creator.save_create": ("💾 Guardar y Crear", "💾 Save and Create", "💾 保存して作成"),
    "creator.select_btn": ("📂 Seleccionar", "📂 Select", "📂 選択"),
    "creator.select_png_title": ("Seleccionar PNG", "Select PNG", "PNGを選択"),
    "creator.png_filter": ("Imágenes PNG (*.png *.PNG)", "PNG Images (*.png *.PNG)", "PNG画像 (*.png *.PNG)"),
    "creator.limit_title": ("Límite Alcanzado", "Limit Reached", "上限に達しました"),
    "creator.limit_msg": (
        "Has alcanzado el límite de 12 skins. Borra alguno manualmente antes de crear uno nuevo.",
        "You've reached the 12-skin limit. Manually delete one before creating a new one.",
        "スキンの上限(12個)に達しました。新しく作成する前に手動で削除してください。",
    ),
    "creator.name_required": ("Por favor escribe un nombre para el skin.", "Please enter a name for the skin.", "スキンの名前を入力してください。"),
    "creator.name_exists": ("Ya existe un skin con ese nombre.", "A skin with that name already exists.", "その名前のスキンは既に存在します。"),
    "creator.incomplete_title": ("Incompleto", "Incomplete", "未完了"),
    "creator.incomplete_msg": (
        "Debes tener al menos las imágenes 'Neutral' (Abierta y Cerrada).",
        "You must at least have the 'Neutral' images (Open and Closed).",
        "少なくとも「ニュートラル」画像(開き・閉じ)が必要です。",
    ),
    "creator.update_success": ("Skin actualizado correctamente.", "Skin updated successfully.", "スキンを正常に更新しました。"),
    "creator.create_success": ("Skin '{name}' creado correctamente.", "Skin '{name}' created successfully.", "スキン '{name}' を正常に作成しました。"),
    "creator.export_prompt_title": ("Exportar Skin", "Export Skin", "スキンをエクスポート"),
    "creator.export_prompt_msg": (
        "¿Deseas guardar un archivo .ptuber para compartir este skin?",
        "Do you want to save a .ptuber file to share this skin?",
        "このスキンを共有するために.ptuberファイルを保存しますか?",
    ),
    "creator.save_fatal_error": ("No se pudo guardar el perfil:\n{error}", "Could not save the profile:\n{error}", "プロファイルを保存できませんでした:\n{error}"),
    "creator.save_compact_title": ("Guardar Skin Compacto", "Save Compact Skin", "コンパクトスキンを保存"),
    "creator.exported_title": ("Exportado", "Exported", "エクスポート完了"),
    "creator.exported_msg": ("Archivo guardado en:\n{path}", "File saved to:\n{path}", "ファイルを保存しました:\n{path}"),
    "creator.export_error_title": ("Error Exportación", "Export Error", "エクスポートエラー"),
    "creator.export_fatal_error": (
        "Falló al crear el archivo .ptuber:\n{error}",
        "Failed to create the .ptuber file:\n{error}",
        ".ptuberファイルの作成に失敗しました:\n{error}",
    ),

    # --- Controles estilo Mac ---
    "mac.close": ("Cerrar", "Close", "閉じる"),
    "mac.minimize": ("Minimizar", "Minimize", "最小化"),
    "mac.zoom": ("Zoom / Pantalla Completa", "Zoom / Full Screen", "ズーム / フルスクリーン"),
}

TRANSLATIONS = {"es": {}, "en": {}, "ja": {}}
for _key, (_es, _en, _ja) in _STRINGS.items():
    TRANSLATIONS["es"][_key] = _es
    TRANSLATIONS["en"][_key] = _en
    TRANSLATIONS["ja"][_key] = _ja


class Translator(QObject):
    language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.language = DEFAULT_LANGUAGE

    def set_language(self, lang):
        if lang not in TRANSLATIONS:
            lang = DEFAULT_LANGUAGE
        if lang == self.language:
            return
        self.language = lang
        self.language_changed.emit(lang)

    def tr(self, key, **kwargs):
        text = TRANSLATIONS.get(self.language, {}).get(key)
        if text is None:
            text = TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text


i18n = Translator()


def tr(key, **kwargs):
    return i18n.tr(key, **kwargs)
