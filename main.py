from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.core.race_controller import RaceController
from src.models.track import load_track_definition
from src.ui.mainmenu import MainMenu, apply_accessibility, load_settings
from src.ui.race import RaceWindow


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

    # Create the shared race controller once so the menu roster and race window show the same field.
    controller = RaceController(track, num_cars=10, max_ticks=5000)
    controller.setup()

    # Keep the live race window alive up front so the menu can reveal it on demand.
    race_window = RaceWindow(track, controller)
    race_window.resize(1200, 850)

    # Wire the menu action directly to the live race window's show method.
    menu_window = MainMenu(controller=controller, on_start_race=race_window.show)
    menu_window.show()

    # Hand control over to Qt's event loop and return its exit code to the shell.
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())