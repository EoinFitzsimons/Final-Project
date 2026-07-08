from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict
from random import SystemRandom
from pathlib import Path

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.core.car import Car, create_car
from src.core.driver import ARCHETYPES, Driver, generate_driver
from src.models.track import TrackDefinition


_RNG = SystemRandom()


@dataclass
class RaceResult:
    finishing_order: List[Car] = field(default_factory=list)


class RaceController:
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

        # Convert the track length from kilometres to metres.
        self.lap_distance = self.track.total_length_km * 1000.0

        # Calculate the total race distance.
        self.race_distance = self.lap_distance * self.track.total_laps

        # Store the distance travelled by each car.
        self._progress: Dict[int, float] = {}

    def setup(self) -> None:
        # Generate the drivers for the race.
        archetypes = list(ARCHETYPES)
        _RNG.shuffle(archetypes)

        self.drivers = [
            generate_driver(archetypes[i % len(archetypes)])
            for i in range(self.num_cars)
        ]
        driver_ids = [d.id for d in self.drivers]

        # Create a car for each driver using the starting grid order.
        self.cars = [
            create_car(driver_ids, starting_grid_position=i + 1)
            for i in range(self.num_cars)
        ]

        # Initialise every car's progress to zero metres.
        for car in self.cars:
            self._progress[car.id] = 0.0

    def _calculate_tick_speed(self, car: Car, driver: Driver) -> float:
        # Convert driver statistics into scaling factors.
        speed_factor = driver.stats.speed / 100.0
        consistency_factor = driver.stats.consistency / 100.0

        # Calculate the maximum speed for this driver and car.
        max_speed = car.base_top_speed * (0.5 + speed_factor * 0.5)

        # Introduce a small amount of random variation.
        variance = _RNG.uniform(0.95, 1.05)

        # Apply consistency and variance to the final speed.
        effective_speed = max_speed * consistency_factor * variance

        # Convert km/h to m/s (one simulation tick equals one second).
        return (effective_speed * 1000.0) / 3600.0

    def step(self) -> None:
        # Update every active car for one simulation tick.
        for car, driver in zip(self.cars, self.drivers):

            # Skip cars that have already finished.
            if car.race_status != "Active":
                continue

            # Calculate the distance travelled during this tick.
            speed_mps = self._calculate_tick_speed(car, driver)
            self._progress[car.id] += speed_mps

            # Store the current speed in km/h.
            car.current_speed = speed_mps * 3.6

            # Update the current lap from the total distance travelled.
            completed_laps = int(self._progress[car.id] // self.lap_distance)
            car.current_lap = completed_laps

            # Mark the car as finished once the race distance is reached.
            if self._progress[car.id] >= self.race_distance:
                car.race_status = "Finished"

    def run(self) -> RaceResult:
        # Create the drivers, cars and initial race state.
        self.setup()

        # Continue running until all cars finish or the tick limit is reached.
        for _ in range(self.max_ticks):
            active_cars = [c for c in self.cars if c.race_status == "Active"]

            if not active_cars:
                break

            self.step()

        # Order cars by the total distance travelled.
        ordered = sorted(
            self.cars,
            key=lambda c: self._progress[c.id],
            reverse=True,
        )

        return RaceResult(finishing_order=ordered)


def main() -> int:
    from src.models.track import load_track_definition

    # Load the track configuration from disk.
    track = load_track_definition(
        Path(__file__).resolve().parents[2] / "src" / "data" / "track.json"
    )

    # Create and run the race simulation.
    controller = RaceController(track, num_cars=10, max_ticks=3000)
    result = controller.run()

    # Display the finishing order.
    print("\nFINISHING ORDER:")
    for i, car in enumerate(result.finishing_order, 1):
        print(f"{i}. Car {car.id} (Driver {car.driver_id}) - Laps: {car.current_lap}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())