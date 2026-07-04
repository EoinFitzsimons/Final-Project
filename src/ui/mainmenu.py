import sys
import os
import json

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QDialog,
    QComboBox,
    QLabel,
    QSpinBox,
    QDialogButtonBox,
)


# Default accessibility values keep the UI usable even before any settings file exists.
DEFAULT_SETTINGS = {
    "theme": "standard",
    "ui_scale": 100,
}

# Store the settings file in the user's home directory so it survives app restarts.
SETTINGS_PATH = os.path.join(
    os.path.expanduser("~"),
    ".momentum_accessibility.json"
)


def load_settings():
    # Load persisted settings, but fall back to defaults if the file is missing or invalid.
    if not os.path.exists(SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return validate_settings(data)
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    # Save only validated settings so corruption cannot leak back into the file.
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(validate_settings(settings), f, indent=2)


def validate_settings(raw):
    # Clamp user-provided values to the small set of options the UI actually supports.
    settings = dict(DEFAULT_SETTINGS)

    if isinstance(raw, dict):
        theme = str(raw.get("theme", "standard")).strip().lower()
        if theme not in {"standard", "high_contrast", "colorblind_safe"}:
            theme = "standard"

        try:
            scale = int(raw.get("ui_scale", 100))
        except Exception:
            scale = 100

        if scale not in {100, 125, 150}:
            scale = 100

        settings["theme"] = theme
        settings["ui_scale"] = scale

    return settings


def get_theme(theme):
    # Each theme is represented as a full stylesheet so the whole UI changes together.
    if theme == "high_contrast":
        return """
        QWidget { background: black; color: white; }
        QPushButton { border: 2px solid white; background: black; }
        """

    if theme == "colorblind_safe":
        return """
        QWidget { background: #1F2430; color: #E6E6E6; }
        QPushButton { border: 1px solid #5DA5DA; }
        """

    return """
    QWidget { background: #353839; color: #B9F2FF; }
    QPushButton { background: #2b2f30; }
    """


def apply_accessibility(app, settings):
    # Apply font scaling and theme globally so the entire interface updates at once.
    font = app.font()

    base_size = font.pointSizeF()
    if base_size <= 0:
        base_size = 10

    scale = settings["ui_scale"] / 100.0
    font.setPointSizeF(max(8.0, base_size * scale))

    app.setFont(font)
    app.setStyleSheet(get_theme(settings["theme"]))


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.settings = load_settings()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Theme"))

        self.theme = QComboBox()
        self.theme.addItem("Standard", "standard")
        self.theme.addItem("High Contrast", "high_contrast")
        self.theme.addItem("Colourblind Safe", "colorblind_safe")
        self.theme.setCurrentText(self.settings["theme"])
        layout.addWidget(self.theme)

        layout.addWidget(QLabel("UI Scale"))

        self.scale = QSpinBox()
        self.scale.setRange(100, 150)
        self.scale.setSingleStep(25)
        self.scale.setValue(self.settings["ui_scale"])
        layout.addWidget(self.scale)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def save(self):
        # Persist the updated values, then close the dialog if validation succeeds.
        save_settings({
            "theme": self.theme.currentData(),
            "ui_scale": self.scale.value(),
        })
        self.accept()


class MainMenu(QWidget):
    def __init__(self, on_start_race=None):
        super().__init__()

        self.setWindowTitle("Momentum")
        self._on_start_race = on_start_race

        layout = QVBoxLayout(self)

        start = QPushButton("Start Race")
        settings = QPushButton("Settings")

        start.clicked.connect(self.start_race)
        settings.clicked.connect(self.open_settings)

        layout.addWidget(start)
        layout.addWidget(settings)

    def start_race(self):
        if self._on_start_race is not None:
            self._on_start_race()

    def open_settings(self):
        # Reapply accessibility immediately after a successful settings save.
        dlg = SettingsDialog(self)
        if dlg.exec():
            apply_accessibility(QApplication.instance(), load_settings())


def main():
    # Create the app, apply accessibility defaults, then show the main menu.
    app = QApplication(sys.argv)

    apply_accessibility(app, load_settings())

    window = MainMenu()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()