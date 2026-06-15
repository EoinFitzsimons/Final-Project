'''FUNCTION CreateCar()

    CREATE Car

    Car.ID = Start from 0 then +1 for each new car

    Car.DriverID = Randomly assign existing Driver.ID

    Car.BaseTopSpeed = 350 km/h
    Car.BaseAcceleration = 2 seconds (0-100 km/h)
    Car.BaseHandling = 100

    Car.CurrentSpeed = 0 km/h

    Car.TyreCondition = 100
    Car.FuelLoad = 100

    Car.CurrentLap = 0
    Car.CurrentPosition = Starting Grid Position

    Car.CurrentCheckpoint = 0

    Car.RaceStatus = Active

    RETURN Car

END FUNCTION'''
from __future__ import annotations  # allows forward references in type hints so classes can reference themselves cleanly

from dataclasses import dataclass, field  # dataclass reduces boilerplate for storing state-like objects such as a Car
from typing import ClassVar, List, Optional  # ClassVar is used for shared class-level state, List/Optional are type hints for readability and tooling
import random  # used to randomly assign a driver from the available pool


@dataclass
class Car:
    _id_counter: ClassVar[int] = 0  # shared counter across all Car instances, used to generate unique IDs

    id: int = field(init=False)  # assigned automatically in __post_init__, not passed in manually
    driver_id: int  # links this car to an existing driver in the simulation system

    base_top_speed: float = 350.0  # maximum theoretical speed in km/h under ideal conditions
    base_acceleration: float = 2.0  # time in seconds to reach 0–100 km/h
    base_handling: int = 100  # abstract handling value (higher means more stable and responsive)

    current_speed: float = 0.0  # current live speed of the car in km/h during simulation
    tyre_condition: int = 100  # tyre health from 100 (new) down to 0 (fully worn)
    fuel_load: int = 100  # fuel percentage remaining

    current_lap: int = 0  # current lap number in the race
    current_position: int = 0  # grid position or live race position depending on context
    current_checkpoint: int = 0  # last checkpoint reached on the track

    race_status: str = "Active"  # current state of the car in the race ("Active", "Finished", "Retired")

    def __post_init__(self) -> None:  # runs automatically after dataclass initialisation
        self.id = self._generate_id()  # assign unique ID once object is created

    @classmethod
    def _generate_id(cls) -> int:  # increments shared counter and returns new unique value
        cls._id_counter += 1
        return cls._id_counter


def create_car(existing_driver_ids: List[int], starting_grid_position: Optional[int] = None) -> Car:
    # factory function used to create a fully initialised Car with a valid driver assigned

    if not existing_driver_ids:
        raise ValueError("No driver IDs provided")  # cannot create a car without at least one valid driver

    driver_id = random.choice(existing_driver_ids)  # randomly assign a driver from available pool

    car = Car(
        driver_id=driver_id,
        current_position=starting_grid_position if starting_grid_position is not None else 0
    )  # create car with initial race state

    return car


if __name__ == "__main__":
    # simple test harness to validate Car creation logic outside the simulation engine

    drivers = [101, 102, 103, 104]  # example driver pool

    cars = [
        create_car(drivers, i + 1)  # assign grid positions starting from 1
        for i in range(5)
    ]

    for car in cars:
        print(car)  # output dataclass representation for debugging