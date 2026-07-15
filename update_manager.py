"""
(AI)terEgo
-----------
Una aplicación de avatar virtual controlada por voz e Inteligencia Artificial.

Desarrollado por: JJaroll
GitHub: https://github.com/JJaroll
Fecha: 10/02/2026
Licencia: MIT
"""

__author__ = "JJaroll"
__version__ = "1.1.0"
__maintainer__ = "JJaroll"
__status__ = "Production"

import json
import re
import urllib.request
from PyQt6.QtCore import QThread, pyqtSignal

# --- CONSTANTES ---
CURRENT_VERSION = "1.1.0"

# Repositorio de GitHub donde se publican los releases de la aplicación.
GITHUB_REPO = "JJaroll/Ai_terego"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def parse_version(version_str):
    """Convierte un string de versión ('v1.10.2', '1.2') en una tupla de enteros
    comparable, p. ej. (1, 10, 2). Los sufijos no numéricos se ignoran."""
    if not version_str:
        return (0,)
    cleaned = version_str.strip().lstrip("vV")
    parts = re.split(r"[.\-+]", cleaned)
    numbers = []
    for part in parts:
        match = re.match(r"\d+", part)
        if match:
            numbers.append(int(match.group(0)))
        else:
            break
    return tuple(numbers) if numbers else (0,)


def is_newer_version(remote_version, current_version):
    return parse_version(remote_version) > parse_version(current_version)


class UpdateChecker(QThread):
    # (url_de_descarga, version_nueva)
    update_available = pyqtSignal(str, str)

    def run(self):
        try:
            req = urllib.request.Request(
                GITHUB_API_URL,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/vnd.github+json",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            remote_tag = data.get("tag_name", "")
            if not remote_tag:
                return

            if is_newer_version(remote_tag, CURRENT_VERSION):
                download_url = self._pick_asset_url(data) or data.get("html_url", "")
                remote_version = remote_tag.lstrip("vV")
                self.update_available.emit(download_url, remote_version)

        except Exception as e:
            print(f"[ERROR] Update check failed: {e}")

    @staticmethod
    def _pick_asset_url(release_data):
        import platform
        system = platform.system().lower()

        keywords = {
            "darwin": ["dmg", "mac", "macos", "apple"],
            "windows": ["win", "exe", ".zip"],
            "linux": ["linux", ".deb", ".tar.gz", "appimage"],
        }.get(system, [])

        for asset in release_data.get("assets", []):
            name = asset.get("name", "").lower()
            if any(kw in name for kw in keywords):
                return asset.get("browser_download_url", "")
        return None
