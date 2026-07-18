# 🎙️ (AI)terEgo (Python + PyTorch)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green) ![Version](https://img.shields.io/badge/Version-1.2.0-blue)

*🌍 [Español](README.md) | **English** | [日本語](README_ja.md)*

**(AI)terEgo** is a smart, modern virtual avatar application written in Python. Unlike traditional PNGTubers that only react to microphone volume, this project uses **Artificial Intelligence (Wav2Vec2)** to analyze your voice tone in real-time and automatically change your avatar's expression.

Ideal for streamers, content creators, or just having fun on Discord/Zoom.

## ✨ Key Features

* **🌍 Multi-Language Support:**
    *   Interface available in Spanish and English with built-in internationalization (i18n).
* **🧠 Multi-Model AI Brain:**
    *   **Spanish (SomosNLP):** Detects *Neutral, Happy, Sad, Angry*.
    *   **English/Global (XLS-R):** Detects *Neutral, Happy, Sad, Angry, Surprise, Disgust, Fear*.
    *   *Note: You can switch AI models in real-time from the Settings.*
* **🗣️ Lip Sync:** Reactive mouth movement based on microphone volume.
* **🐇 Visual Effects:**
    *   **Bounce:** The avatar subtly jumps when you speak.
    *   **Soft Shadow:** Realistic shadow beneath the avatar.
    *   **Mirror Effect (Flip):** Instantly flip your avatar.
* **🎨 Skins System (.ptuber):**
    *   Create your own avatars with the **Built-in Creator**.
    *   Support for up to **7 emotions** and mouth states (closed/open).
    *   Import and export skins easily to share with friends.
* **⚙️ Customizable Configuration:**
    * **System Tab:** AI model selector and automatic updates control.
    * **Shortcuts:** Configure global hotkeys for each emotion.
    * **Persistence:** Automatically saves your microphone, sensitivity, and colors.
    *   The app can be minimized to the system tray to run in the background without being intrusive.
* **🔋 Enhancements & Utilities:**
    *   **Easy Download:** AI model downloading and management with an integrated progress window.
    *   **Persistence:** Automatically saves your microphone, sensitivity, colors, and chosen profiles.
    *   **Global Shortcuts:** Control everything via configurable keyboard shortcuts, without needing the window to be active.
* **🖥️ Modern Interface:**
    *   Frameless main window with transparent background.
    *   **Notifications:** Discreet pill-like alerts when new updates are available.

---

## 📥 Download and Installation (Binaries)

(AI)terEgo is available natively for all platforms! Choose the version corresponding to your operating system to download the ready-to-use application (no Python required).

### 🍎 macOS
* **Universal Installer (.dmg):** [Download AIterEgo_Installer.dmg](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AIterEgo_Installer.dmg)
  > **Installation:** Open the `.dmg` file and drag the application to your Applications folder. When opening it for the first time, macOS will ask for permission to use the microphone; you must accept this for the avatar to react.

### 🪟 Windows
* **Windows Installer (.exe):** [Download setup.exe](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/setup.exe)
* **GPU Version (Nvidia CUDA):** [Download (AI)terEgo_GPU_Win-64.zip](https://drive.google.com/file/d/154DRv8xT6BG37Fc4wkSMSnRo75FLDeco/view?usp=sharing)
  > **Installation:** Download and run the `setup.exe` installer to automatically install the application on your system.

### 🐧 Linux
* **Universal Executable (.AppImage):** [Download AIterEgo-Linux.AppImage](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AIterEgo-Linux.AppImage)
  > **Installation and Execution:** Download the `.AppImage` file. Right-click on it, go to **Properties -> Permissions**, check the "Allow executing file as program" option, and then simply double-click it to open.

*Important Note: The first time you open the application on any system, it might take a few extra seconds (or show a loading screen) while the Artificial Intelligence models are downloaded or initialized in your device's memory.*

---

## 🛠️ Building from Source Code

If you are a developer and prefer to run or modify the source code directly:

### Prerequisites
* Python 3.10 or higher.
* A microphone.

### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/JJaroll/Ai_terEgo.git
    cd Ai_terEgo
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    *(Note: PyTorch may require a specific installation depending on your system. Check [pytorch.org](https://pytorch.org))*
    ```bash
    pip install -r requirements.txt
    ```
    *If you do not have the requirements.txt file, the core libraries are:*
    `PyQt6`, `torch`, `torchaudio`, `transformers`, `huggingface_hub`, `pyaudio`, `numpy`.

4.  **Install PyAudio (If errors occur):**
    * **Windows:** `pip install pipwin && pipwin install pyaudio`
    * **macOS:** `brew install portaudio && pip install pyaudio`
    * **Linux:** `sudo apt-get install python3-pyaudio`

## 🚀 Usage

Run the main file:

```bash
python main.py
```

## 🎨 Controls

*   **Left Click + Drag:** Move the character around the screen.
*   **Right Click:** Open the Context Menu (Quick Settings).
*   **Bottom Right Corner:** Resize the character.
*   **Bottom Buttons (Dock):**
    *   🔊: Mute/Unmute microphone.
    *   🔄: Flip Avatar Horizontally (Mirror Effect).
    *   ⚙️: Open full configuration window.
    *   🤖: Activate **AI Mode** (Automatic).
    *   😐, 😄, etc.: Force an emotion manually.
    *   *Note: Emotions not supported by the current model will be hidden under a `›` expansion button but can still be triggered manually.*

### Keyboard Shortcuts (Default)
*   **1-4:** Basic emotions (Neutral, Happy, Sad, Angry).
*   **7-9:** Extra emotions (Surprise, Fear, Disgust).
*   **X:** Activate AI Mode.
*   **M:** Mute microphone.
*   **Ctrl+F / Cmd+F:** Mirror Effect (Horizontal Flip).

### Advanced Configuration (Right Click -> Settings)
From here you can control everything:
*   **System:** Change AI Model (Spanish/English), check for updates.
*   **Audio:** Adjust sensitivity and silence threshold.
*   **Appearance:** Change background color (Transparent/Chroma), activate shadow, etc.
*   **Avatar:** Manage and edit Skin profiles.
*   **Shortcuts:** Globally customize hotkeys.

## 📁 Project Structure

* **main.py:** Entry point. Connects the interface with the logic.
* **core_systems.py:** The Brain. Contains the Audio (PyAudio) and Download & AI (Transformers) threads.
* **background.py:** Manages the visual context menu of the avatar.
* **profile_manager.py:** Logic for saving, loading, importing, and exporting skins (.ptuber).
* **profile_creator.py:** GUI interface for creating avatars.
* **config_manager.py:** Save and persistence system (settings.json).
* **settings_window.py:** Management of the full configuration window.
* **ui_components.py:** Contains reusable UI modals and components.
* **update_manager.py:** Checks if there are new updates on GitHub.
* **hotkey_manager.py:** Connects global keystrokes with application actions.

## 🤝 Contributing

Contributions are welcome!

1.  **Fork** the project.
2.  Create a branch (`git checkout -b feature/NewFeature`).
3.  Make your changes and commits.
4.  Push to the branch (`git push origin feature/NewFeature`).
5.  Open a **Pull Request**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Created with ❤️ by **JJaroll**
