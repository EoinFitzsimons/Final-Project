import sys
import os
import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QDialog,
    QComboBox,
    QLabel,
    QScrollArea,
    QSpinBox,
    QDialogButtonBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from src.ui.colours import (
    CAR_COLOURS,
    MENU_BACKGROUND_1,
    MENU_BACKGROUND_2,
    MENU_ACCENT,
    MENU_BUTTON_BACKGROUND,
    MENU_BUTTON_BORDER,
    MENU_FOREGROUND_1,
    MENU_FOREGROUND_2,
    MENU_MUTED_TEXT,
    MENU_PANEL_BACKGROUND,
    MENU_PANEL_BORDER,
    MENU_PANEL_TEXT,
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGO_PATH = PROJECT_ROOT / "assets" / "Momentum Logo.png"


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
        if theme not in {"standard", "high_contrast", "colourblind_safe"}:
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
    if theme == "standard":
        return f"""
    QWidget {{ background: {MENU_BACKGROUND_1}; color: {MENU_FOREGROUND_1}; }}
    QPushButton {{ background: {MENU_BUTTON_BACKGROUND}; }}
    """

    if theme == "high_contrast":
        return """
        QWidget { background: black; color: white; }
        QPushButton { border: 2px solid white; background: black; }
        """

    if theme == "colourblind_safe":
        return f"""
        QWidget {{ background: {MENU_BACKGROUND_2}; color: {MENU_FOREGROUND_2}; }}
        QPushButton {{ border: 1px solid {MENU_BUTTON_BORDER}; }}
        """

    return f"""
    QWidget {{ background: {MENU_BACKGROUND_1}; color: {MENU_FOREGROUND_1}; }}
    QPushButton {{ background: {MENU_BUTTON_BACKGROUND}; }}
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
        self.theme.addItem("Default", "standard")
        self.theme.addItem("High Contrast", "high_contrast")
        self.theme.addItem("Colourblind Safe", "colourblind_safe")
        current_index = self.theme.findData(self.settings["theme"])
        if current_index >= 0:
            self.theme.setCurrentIndex(current_index)
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


class DriverRosterWidget(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._controller = controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        title = QLabel("Driver roster")
        title.setStyleSheet(f"color: {MENU_PANEL_TEXT}; font-weight: 700; font-size: 16px;")
        layout.addWidget(title)

        subtitle = QLabel("Each driver is paired with a race colour and stat profile.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {MENU_MUTED_TEXT};")
        layout.addWidget(subtitle)

        for index, driver in enumerate(self._controller.drivers):
            color = CAR_COLOURS[index % len(CAR_COLOURS)]
            card = QFrame()
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(
                f"QFrame {{ background: {MENU_PANEL_BACKGROUND}; border: 1px solid {MENU_PANEL_BORDER}; border-radius: 10px; }}"
            )

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 10)
            card_layout.setSpacing(12)

            swatch = QLabel()
            swatch.setFixedSize(18, 18)
            swatch.setStyleSheet(f"background: {color}; border: 1px solid {MENU_ACCENT}; border-radius: 9px;")
            card_layout.addWidget(swatch, alignment=Qt.AlignmentFlag.AlignTop)

            details = QVBoxLayout()
            details.setSpacing(3)

            name = QLabel(f"{driver.name}  |  {driver.archetype}")
            name.setWordWrap(True)
            name.setStyleSheet(f"color: {MENU_PANEL_TEXT}; font-weight: 600;")
            details.addWidget(name)

            meta = QLabel(
                f"Colour {index + 1}: {color}   •   Nationality: {driver.nationality}   •   Age: {driver.age}"
            )
            meta.setWordWrap(True)
            meta.setStyleSheet(f"color: {MENU_MUTED_TEXT};")
            details.addWidget(meta)

            stats = QLabel(
                "Speed {0}   •   Handling {1}   •   Aggression {2}   •   Consistency {3}".format(
                    driver.stats.speed,
                    driver.stats.handling,
                    driver.stats.aggression,
                    driver.stats.consistency,
                )
            )
            stats.setWordWrap(True)
            stats.setStyleSheet(f"color: {MENU_MUTED_TEXT};")
            details.addWidget(stats)

            card_layout.addLayout(details)
            layout.addWidget(card)

        layout.addStretch(1)


class MainMenu(QWidget):
    def __init__(self, controller=None, on_start_race=None):
        super().__init__()

        self.setWindowTitle("Momentum")
        self.resize(1920, 1080)
        self._controller = controller
        self._on_start_race = on_start_race

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_pixmap = QPixmap(str(LOGO_PATH))
        if not logo_pixmap.isNull():
            logo.setPixmap(
                logo_pixmap.scaledToWidth(260, Qt.TransformationMode.SmoothTransformation)
            )
            layout.addWidget(logo)

        header = QLabel("Momentum")
        header.setStyleSheet(f"color: {MENU_FOREGROUND_1}; font-size: 28px; font-weight: 700;")
        layout.addWidget(header)

        intro = QLabel("Select a theme, review the field, then launch the live race.")
        intro.setWordWrap(True)
        intro.setStyleSheet(f"color: {MENU_MUTED_TEXT};")
        layout.addWidget(intro)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        start = QPushButton("Start Race")
        settings = QPushButton("Settings")

        start.clicked.connect(self.start_race)
        settings.clicked.connect(self.open_settings)

        button_row.addWidget(start)
        button_row.addWidget(settings)
        layout.addLayout(button_row)

        if self._controller is not None:
            roster_scroll = QScrollArea()
            roster_scroll.setWidgetResizable(True)
            roster_scroll.setFrameShape(QFrame.Shape.NoFrame)
            roster_scroll.setStyleSheet(
                f"QScrollArea {{ background: transparent; border: 1px solid {MENU_PANEL_BORDER}; border-radius: 12px; }}"
            )
            roster_scroll.setWidget(DriverRosterWidget(self._controller))
            layout.addWidget(roster_scroll, stretch=1)

    def start_race(self):
        self.hide()
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
    window.resize(1920, 1080)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()