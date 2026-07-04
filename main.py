from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.models.track import load_track_definition
from src.ui.mainmenu import MainMenu, apply_accessibility, load_settings
from src.ui.racetrack import TrackPreviewWindow


def build_app() -> QApplication:
    # Create the shared Qt application object once, then apply the saved accessibility settings.
    app = QApplication(sys.argv)
    apply_accessibility(app, load_settings())
    return app


def main() -> int:
    app = build_app()

    # Load the bundled track definition so both the menu and preview use the same source of truth.
    track_path = Path(__file__).resolve().parent / "src" / "data" / "track.json"
    track = load_track_definition(track_path)

    # Keep the preview window alive up front so the menu can reveal it on demand.
    track_window = TrackPreviewWindow(track)
    track_window.resize(1100, 800)

    # Wire the menu action directly to the preview window's show method.
    menu_window = MainMenu(on_start_race=track_window.show)
    menu_window.show()

    # Hand control over to Qt's event loop and return its exit code to the shell.
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())