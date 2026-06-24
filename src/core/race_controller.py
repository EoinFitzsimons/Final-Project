from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict
import random
import math

from src.core.car import Car, create_car
from src.core.driver import Driver, generate_driver
from src.models.track import TrackDefinition


@dataclass
class RaceResult:
    finishing_order: List[Car] = field(default_factory=list)


class RaceController:
    """
    Minimal deterministic race simulation controller.

    Responsibilities:
    - Initialise drivers and cars
    - Run tick-based race loop
    - Update lap progression
    - Determine finishing order
    """

    def __init__(
        self,
        track: TrackDefinition,
        num_cars: int = 10,
        max_ticks: int = 5000,
    ) -> None:
        self.track = track
        self.num_cars = num_cars
        self.max_ticks = max_ticks

        self.drivers: List[Driver] = []
        self.cars: List[Car] = []

        self.lap_distance = self.track.total_length_km * 1000.0  # convert to metres
        self.race_distance = self.lap_distance * self.track.total_laps

        self._progress: Dict[int, float] = {}  # car_id -> metres completed

    def setup(self) -> None:
        """
        Creates drivers and cars and initialises race state.
        """

        self.drivers = [generate_driver() for _ in range(self.num_cars)]
        driver_ids = [d.id for d in self.drivers]

        self.cars = [
            create_car(driver_ids, starting_grid_position=i + 1)
            for i in range(self.num_cars)
        ]

        for car in self.cars:
            self._progress[car.id] = 0.0

    def _calculate_tick_speed(self, car: Car, driver: Driver) -> float:
        """
        Simplified speed model:
        - base top speed influenced by driver speed stat
        - handling reduces instability (not modelled deeply here)
        """

        speed_factor = driver.stats.speed / 100.0
        consistency_factor = driver.stats.consistency / 100.0

        max_speed = car.base_top_speed * (0.5 + speed_factor * 0.5)

        # randomness simulates race variance
        variance = random.uniform(0.95, 1.05)

        effective_speed = max_speed * consistency_factor * variance

        # convert km/h to m per tick (assume 1 tick = 1 second)
        return (effective_speed * 1000.0) / 3600.0

    def step(self) -> None:
        """
        Advances the simulation by one tick.
        """

        for car, driver in zip(self.cars, self.drivers):
            if car.race_status != "Active":
                continue

            speed_mps = self._calculate_tick_speed(car, driver)
            self._progress[car.id] += speed_mps

            # update car state
            car.current_speed = speed_mps * 3.6

            # lap progression
            completed_laps = int(self._progress[car.id] // self.lap_distance)
            car.current_lap = completed_laps

            # finish condition
            if self._progress[car.id] >= self.race_distance:
                car.race_status = "Finished"

    def run(self) -> RaceResult:
        """
        Runs full race simulation.
        """

        self.setup()

        for _ in range(self.max_ticks):
            active_cars = [c for c in self.cars if c.race_status == "Active"]

            if not active_cars:
                break

            self.step()

        # final ordering
        ordered = sorted(
            self.cars,
            key=lambda c: self._progress[c.id],
            reverse=True,
        )

        return RaceResult(finishing_order=ordered)


if __name__ == "__main__":
    from src.models.track import load_track_definition
    from pathlib import Path

    track = load_track_definition(
        Path(__file__).resolve().parents[2] / "src" / "data" / "track.json"
    )

    controller = RaceController(track, num_cars=10, max_ticks=3000)
    result = controller.run()

    print("\nFINISHING ORDER:")
    for i, car in enumerate(result.finishing_order, 1):
        print(f"{i}. Car {car.id} (Driver {car.driver_id}) - Laps: {car.current_lap}")