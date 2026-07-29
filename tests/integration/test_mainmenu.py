from pathlib import Path

from src.core.race_controller import RaceController
from PyQt6.QtWidgets import QPushButton
from src.models.track import load_track_definition
from src.ui.mainmenu import MainMenu


def _create_controller():

    track = load_track_definition(
        Path(__file__).resolve().parents[2]
        / "src"
        / "data"
        / "track.json"
    )

    controller = RaceController(
        track=track,
        num_cars=10,
        max_ticks=3000
    )

    controller.setup()

    return controller


def test_race_controller_integrates_with_main_menu(qtbot):

    controller = _create_controller()

    race_started = False

    def start_callback():
        nonlocal race_started
        race_started = True

    menu = MainMenu(
        controller=controller,
        on_start_race=start_callback
    )

    qtbot.addWidget(menu)

    # Verify the menu receives generated drivers.
    assert menu._controller is controller

    # Verify driver roster data is available.
    assert len(controller.drivers) == 10

    # Verify required controls exist.
    assert menu.start_button.text() == "Start Race"
    assert menu.settings_button.text() == "Settings"

    # Trigger the race start action.
    menu.start_race()

    # Verify GUI communicates with race startup logic.
    assert race_started is True