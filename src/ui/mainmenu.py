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


# default accessibility configuration
DEFAULT_SETTINGS = {
    "theme": "standard",
    "ui_scale": 100,
}

# file used for persistence
SETTINGS_PATH = os.path.join(
    os.path.expanduser("~"),
    ".momentum_accessibility.json"
)


def load_settings():
    # load settings from disk or fallback to defaults
    if not os.path.exists(SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return validate_settings(data)
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    # persist validated settings
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(validate_settings(settings), f, indent=2)


def validate_settings(raw):
    # ensure only supported values are used
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
    # return stylesheet for selected theme
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
    # apply font scaling and theme globally
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
        # save updated settings and close dialog
        save_settings({
            "theme": self.theme.currentData(),
            "ui_scale": self.scale.value(),
        })
        self.accept()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Momentum")

        layout = QVBoxLayout(self)

        start = QPushButton("Start Race")
        settings = QPushButton("Settings")

        start.clicked.connect(self.start_race)
        settings.clicked.connect(self.open_settings)

        layout.addWidget(start)
        layout.addWidget(settings)

    def start_race(self):
        # placeholder for race launch logic
        pass

    def open_settings(self):
        # open settings dialog and reapply accessibility on save
        dlg = SettingsDialog(self)
        if dlg.exec():
            apply_accessibility(QApplication.instance(), load_settings())


def main():
    # create application and apply accessibility settings
    app = QApplication(sys.argv)

    apply_accessibility(app, load_settings())

    window = MainMenu()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()