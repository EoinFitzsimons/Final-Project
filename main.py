from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.models.track import load_track_definition
from src.ui.mainmenu import MainMenu, apply_accessibility, load_settings
from src.ui.racetrack import TrackPreviewWindow


def build_app() -> QApplication:
    app = QApplication(sys.argv)
    apply_accessibility(app, load_settings())
    return app


def main() -> int:
    app = build_app()

    track_path = Path(__file__).resolve().parent / "src" / "data" / "track.json"
    track = load_track_definition(track_path)

    track_window = TrackPreviewWindow(track)
    track_window.resize(1100, 800)

    menu_window = MainMenu(on_start_race=track_window.show)
    menu_window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())