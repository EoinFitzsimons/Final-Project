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


@dataclass(frozen=True) #dataclass decorator is used to automatically generate special methods like __init__() and __repr__() for the class. frozen=True makes the instances of this class immutable, meaning that once an instance is created, its attributes cannot be modified. This is useful for telemetry data, which should not change after being recorded. https://docs.python.org/3/library/dataclasses.html
class RaceTelemetry:
    position: int
    car_id: int
    driver_id: int
    driver_name: str
    gap_to_leader_m: float
    current_lap: int
    lap_time_s: float
    current_checkpoint_id: int
    current_checkpoint_name: str
    current_speed_kmh: float
    tyre_condition: int
    fuel_load: int
    race_status: str


class RaceController:
    def __init__(
        self,
        track: TrackDefinition,
        num_cars: int = 10,
        max_ticks: int = 5000, # Maximum number of simulation ticks in the race, limiting the race duration to avoid infinite loops in case of bugs or unexpected behavior.
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
            generate_driver(archetypes[i % len(archetypes)]) #Use one of the shuffled archetypes for each driver, cycling through them if there are more drivers than archetypes.
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
        variance = _RNG.uniform(0.95, 1.05) #equal chance of being slower or faster than the calculated speed.

        # Apply consistency and variance to the final speed.
        effective_speed = max_speed * consistency_factor * variance

        # Convert km/h to m/s (one simulation tick equals one second).
        return (effective_speed * 1000.0) / 3600.0

    def _current_checkpoint(self, progress_m: float) -> tuple[int, str]:
        if not self.track.checkpoints:
            return 0, ""

        fraction = (progress_m % self.lap_distance) / max(self.lap_distance, 1.0) #Calculate the fraction of the current lap completed by dividing the distance travelled in the current lap by the total lap distance. The modulo operator (%) is used to get the distance into the current lap, and max() ensures that we don't divide by zero if the lap distance is zero. https://www.geeksforgeeks.org/python/what-is-a-modulo-operator-in-python/
        checkpoint = self.track.checkpoints[0]

        for candidate in self.track.checkpoints: #find current checkpoint by compariong the fraction of lap completed to the checkpoints' positions. The last checkpoint crossed is the current checkpoint.
            if fraction >= candidate.position:
                checkpoint = candidate
            else:
                break

        return checkpoint.id, checkpoint.name

    def _lap_time_seconds(self, progress_m: float, current_speed_kmh: float) -> float:
        current_speed_mps = current_speed_kmh / 3.6
        if current_speed_mps <= 0.0:
            return 0.0

        distance_into_lap = progress_m % max(self.lap_distance, 1.0)
        return distance_into_lap / current_speed_mps #Calculate the time taken to travel the distance into the current lap, dividing by the current speed in m/s.

    def _ordered_cars(self) -> list[Car]:
        return sorted(
            self.cars,
            key=lambda car: self._progress.get(car.id, 0.0), #Sort the cars based on their progress in the race. Lambda is used here over a function as it is a simple one-line operation that doesn't require a separate function definition. The get() method is used to retrieve the progress of each car, defaulting to 0.0 if the car's ID is not found in the _progress dictionary. This ensures that all cars are included in the sorting, even if they haven't started moving yet.
            reverse=True, #Sort in descending order so that the car with the most progress appears first in the list.
        )

    def get_telemetry(self) -> list[RaceTelemetry]:
        ordered = self._ordered_cars()
        if not ordered:
            return []

        leader_progress = self._progress.get(ordered[0].id, 0.0)
        drivers_by_id = {driver.id: driver for driver in self.drivers}

        telemetry: list[RaceTelemetry] = []
        for position, car in enumerate(ordered, start=1):
            progress = self._progress.get(car.id, 0.0)
            driver = drivers_by_id.get(car.driver_id)
            if driver is None:
                continue

            checkpoint_id, checkpoint_name = self._current_checkpoint(progress)
            gap_to_leader_m = max(0.0, leader_progress - progress)
            lap_time_s = self._lap_time_seconds(progress, car.current_speed)

            car.current_position = position
            car.current_checkpoint = checkpoint_id

            telemetry.append(
                RaceTelemetry(
                    position=position,
                    car_id=car.id,
                    driver_id=driver.id,
                    driver_name=driver.name,
                    gap_to_leader_m=gap_to_leader_m,
                    current_lap=car.current_lap,
                    lap_time_s=lap_time_s,
                    current_checkpoint_id=checkpoint_id,
                    current_checkpoint_name=checkpoint_name,
                    current_speed_kmh=car.current_speed,
                    tyre_condition=car.tyre_condition,
                    fuel_load=car.fuel_load,
                    race_status=car.race_status,
                )
            )

        return telemetry

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
        ordered = self._ordered_cars()

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