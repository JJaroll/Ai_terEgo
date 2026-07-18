# 🎙️ (AI)terEgo (Python + PyTorch)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green) ![Version](https://img.shields.io/badge/Version-1.2.0-blue)


*🌍 [Español](README.md) | [English](README_en.md) | **日本語***

**(AI)terEgo** は Python で書かれたスマートでモダンなバーチャルアバターアプリケーションです。マイクの音量にのみ反応する従来の PNGTuber とは異なり、このプロジェクトでは **人工知能 (Wav2Vec2)** を使用して声のトーンをリアルタイムで分析し、アバターの表情を自動的に変化させます。

ストリーマー、コンテンツクリエイター、または Discord や Zoom で楽しみたい方に最適です。

## ✨ 主な機能

* **🌍 多言語サポート:**
    *   インターフェースはスペイン語と英語で利用可能で、国際化 (i18n) サポートが組み込まれています。
* **🧠 マルチモデル AI ブレイン:**
    *   **スペイン語 (SomosNLP):** *Neutral (ニュートラル), Feliz (喜び), Triste (悲しみ), Enojado (怒り)* を検出します。
    *   **英語/グローバル (XLS-R):** *Neutral (ニュートラル), Happy (喜び), Sad (悲しみ), Angry (怒り), Surprise (驚き), Disgust (嫌悪), Fear (恐れ)* を検出します。
    *   *注: 設定からリアルタイムで AI モデルを切り替えることができます。*
* **🗣️ リップシンク:** マイクの音量に基づいた反応的な口の動き。
* **🐇 視覚効果:**
    *   **バウンス (Bounce):** 話すとアバターがわずかにジャンプします。
    *   **ソフトシャドウ:** アバターの下のリアルな影。
    *   **ミラー効果 (Flip):** アバターを瞬時に反転させます。
* **🎨 スキンシステム (.ptuber):**
    *   **内蔵クリエイター**で独自のアバターを作成できます。
    *   最大 **7つの感情** と口の状態 (開/閉) をサポートします。
    *   スキンのインポート・エクスポートが簡単で、友達とシェアできます。
* **⚙️ カスタマイズ可能な設定:**
    * **システムタブ:** AI モデルの選択と自動更新の制御。
    * **ショートカット:** 感情ごとにグローバルホットキーを設定できます。
    * **永続性:** マイク、感度、カラー設定を自動的に保存します。
    *   アプリをシステムトレイに最小化し、邪魔にならずにバックグラウンドで実行できます。
* **🔋 拡張機能とユーティリティ:**
    *   **簡単なダウンロード:** プログレスウィンドウが統合された AI モデルのダウンロードと管理。
    *   **永続性:** マイク、感度、カラー、および選択したプロファイルを自動的に保存します。
    *   **グローバルショートカット:** ウィンドウをアクティブにする必要なく、設定可能なキーボードショートカットですべてを制御します。
* **🖥️ モダンなインターフェース:**
    *   透明な背景を持つボーダーレス (Frameless) なメインウィンドウ。
    *   **通知:** 新しいアップデートが利用可能な場合の控えめなピル型アラート。

---

## 📥 ダウンロードとインストール (バイナリ)

(AI)terEgo はすべてのプラットフォームでネイティブに利用可能です！オペレーティングシステムに対応するバージョンを選択し、すぐに使えるアプリケーションをダウンロードしてください (Python は不要です)。

### 🍎 macOS
* **ユニバーサルインストーラー (.dmg):** [AI.terEgo_Installer.dmg をダウンロード](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AI.terEgo_Installer.dmg)
  > **インストール:** `.dmg` ファイルを開き、アプリケーションを「アプリケーション」フォルダにドラッグします。初めて開くとき、macOS はマイクの使用許可を求めます。アバターを反応させるには、これを許可する必要があります。

### 🪟 Windows
* **Windows インストーラー (.exe):** [AI.terEgo_Windows_WebInstaller.exe をダウンロード](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AI.terEgo_Windows_WebInstaller.exe)
  > **インストール:** インストーラーが希望するバージョン（Nvidia カードで高いパフォーマンスを発揮する GPU、または最大限の互換性を持つ CPU）を選択するよう求めます。

### 🐧 Linux
* **ユニバーサル実行ファイル (.AppImage):** 
  [パートAをダウンロード](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AI.terEgo-Linux.AppImage.partaa) | [パートBをダウンロード](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.2.0/AI.terEgo-Linux.AppImage.partab)

  > **インストールと実行:** 
  > 1. 両方のパート（`.partaa` と `.partab`）をダウンロードし、同じフォルダに配置します。
  > 2. そのフォルダでターミナルを開き、次のコマンドでパートを結合します：
  >    `cat AIterEgo-Linux.AppImage.part* > "(AI)terEgo-Linux.AppImage"`
  > 3. 生成された `(AI)terEgo-Linux.AppImage` ファイルを右クリックし、**「プロパティ」 -> 「アクセス権」** に進み、「プログラムとして実行可能」オプションにチェックを入れます。
  > 4. 最後に、ファイルをダブルクリックしてアプリケーションを実行します。

*重要な注意: どのシステムでも初めてアプリケーションを開く際、人工知能モデルがダウンロードされたり、デバイスのメモリに初期化されたりするため、数秒余分に時間がかかる (またはロード画面が表示される) ことがあります。*

---

## 🛠️ ソースコードからのビルド

開発者で、ソースコードを直接実行または変更したい場合:

### 前提条件
* Python 3.10 以上。
* マイク。

### 手順
1.  **リポジトリをクローンする:**
    ```bash
    git clone https://github.com/JJaroll/Ai_terEgo.git
    cd Ai_terEgo
    ```

2.  **仮想環境を作成する (推奨):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **依存関係をインストールする:**
    *(注: PyTorch はシステムに応じて特定のインストールが必要になる場合があります。[pytorch.org](https://pytorch.org) を確認してください)*
    ```bash
    pip install -r requirements.txt
    ```
    *requirements.txt ファイルがない場合、主要なライブラリは以下の通りです:*
    `PyQt6`, `torch`, `torchaudio`, `transformers`, `huggingface_hub`, `pyaudio`, `numpy`.

4.  **PyAudio をインストールする (エラーが発生する場合):**
    * **Windows:** `pip install pipwin && pipwin install pyaudio`
    * **macOS:** `brew install portaudio && pip install pyaudio`
    * **Linux:** `sudo apt-get install python3-pyaudio`

## 🚀 使い方

メインファイルを実行します:

```bash
python main.py
```

## 🎨 コントロール

*   **左クリック + ドラッグ:** 画面上でキャラクターを移動させます。
*   **右クリック:** コンテキストメニュー (クイック設定) を開きます。
*   **右下隅:** キャラクターのサイズを変更します。
*   **下部ボタン (ドック):**
    *   🔊: マイクのミュート/ミュート解除。
    *   🔄: アバターを水平に反転 (ミラー効果)。
    *   ⚙️: 完全な設定ウィンドウを開きます。
    *   🤖: **AI モード** (自動) をアクティブにします。
    *   😐, 😄, など: 手動で感情を強制的に表示します。
    *   *注: 現在のモデルでサポートされていない感情は `›` 展開ボタンの下に隠れますが、手動でトリガーすることは可能です。*

### キーボードショートカット (デフォルト)
*   **1-4:** 基本的な感情 (Neutral, Happy, Sad, Angry)。
*   **7-9:** 追加の感情 (Surprise, Fear, Disgust)。
*   **X:** AI モードをアクティブにします。
*   **M:** マイクをミュートします。
*   **Ctrl+F / Cmd+F:** ミラー効果 (水平反転)。

### 高度な設定 (右クリック -> 設定)
ここからすべてを制御できます:
*   **システム:** AI モデル (スペイン語/英語) の変更、アップデートの確認。
*   **オーディオ:** 感度と無音しきい値の調整。
*   **外観:** 背景色の変更 (透明/クロマ)、シャドウの有効化など。
*   **アバター:** スキンプロファイルの管理と編集。
*   **ショートカット:** グローバルホットキーをカスタマイズ。

## 📁 プロジェクト構造

* **main.py:** エントリーポイント。インターフェースとロジックを接続します。
* **core_systems.py:** ブレイン。オーディオ (PyAudio) と ダウンロード & AI (Transformers) スレッドを含みます。
* **background.py:** アバターの視覚的なコンテキストメニューを管理します。
* **profile_manager.py:** スキン (.ptuber) の保存、ロード、インポート、エクスポートのロジック。
* **profile_creator.py:** アバターを作成するための GUI インターフェース。
* **config_manager.py:** 保存および永続性システム (settings.json)。
* **settings_window.py:** 完全な設定ウィンドウの管理。
* **ui_components.py:** 再利用可能な UI モーダルとコンポーネントを含みます。
* **update_manager.py:** GitHub で新しいアップデートがあるかを確認します。
* **hotkey_manager.py:** グローバルキーストロークをアプリケーションのアクションに接続します。

## 🤝 貢献する

貢献を歓迎します！

1.  プロジェクトを **Fork** します。
2.  ブランチを作成します (`git checkout -b feature/NewFeature`)。
3.  変更とコミットを行います。
4.  ブランチに Push します (`git push origin feature/NewFeature`)。
5.  **Pull Request** を開きます。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細については [LICENSE](LICENSE) ファイルを参照してください。

❤️ を込めて **JJaroll** により作成されました
