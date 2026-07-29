from pathlib import Path

from src.core.race_controller import RaceController
from src.models.track import load_track_definition


def _load_test_track():
    # Load the track configuration used by the race simulation.
    return load_track_definition(
        Path(__file__).resolve().parents[2]
        / "src"
        / "data"
        / "track.json"
    )


def _create_controller():
    # Create a RaceController with the default race configuration.
    track = _load_test_track()

    return RaceController(
        track=track,
        num_cars=10,
        max_ticks=3000,
    )


def test_race_controller_initialisation():

    controller = _create_controller()

    # Ensure the controller stores the provided track.
    assert controller.track is not None

    # Ensure the correct number of cars is configured.
    assert controller.num_cars == 10

    # Ensure the maximum tick limit is stored correctly.
    assert controller.max_ticks == 3000

    # Drivers and cars should not exist before setup.
    assert controller.drivers == []
    assert controller.cars == []


def test_race_controller_setup_creates_drivers_and_cars():

    controller = _create_controller()

    controller.setup()

    # Confirm the correct number of drivers were created.
    assert len(controller.drivers) == 10

    # Confirm the correct number of cars were created.
    assert len(controller.cars) == 10


def test_race_controller_setup_initialises_progress():

    controller = _create_controller()

    controller.setup()

    # Ensure every car has initial progress tracked.
    for car in controller.cars:

        assert car.id in controller._progress
        assert controller._progress[car.id] == 0.0

        assert car.id in controller._lap_times
        assert controller._lap_times[car.id] == []

        assert car.id in controller._lap_start_progress
        assert controller._lap_start_progress[car.id] == 0.0


def test_race_controller_step_updates_car_progress():

    controller = _create_controller()

    controller.setup()

    initial_progress = controller._progress[controller.cars[0].id]

    controller.step()

    updated_progress = controller._progress[controller.cars[0].id]

    # Cars should move forward after a simulation tick.
    assert updated_progress > initial_progress


def test_race_controller_generates_telemetry():

    controller = _create_controller()

    controller.setup()

    telemetry = controller.get_telemetry()

    # Confirm telemetry is generated for all cars.
    assert len(telemetry) == 10

    for data in telemetry:

        # Ensure telemetry contains valid race information.
        assert data.driver_name != ""
        assert data.position > 0
        assert data.car_id is not None
        assert data.driver_id is not None


def test_race_controller_orders_cars_by_progress():

    controller = _create_controller()

    controller.setup()

    # Manually set different progress values.
    controller._progress[controller.cars[0].id] = 5000
    controller._progress[controller.cars[1].id] = 1000

    ordered = controller._ordered_cars()

    # Cars should be ordered from highest to lowest progress.
    assert ordered[0].id == controller.cars[0].id
    assert ordered[1].id == controller.cars[1].id


def test_race_controller_run_returns_results():

    controller = _create_controller()

    result = controller.run()

    # Ensure a RaceResult object is returned.
    assert result is not None

    # Ensure finishing order contains all cars.
    assert len(result.finishing_order) == 10