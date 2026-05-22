'''
FUNCTION GenerateDriver()

    CREATE Driver

    Driver.ID = Start from 0 then +1 for each new driver
    Driver.Name = Random Name

    Driver.Archtype = Random FROM
    (
        Veteran Defender,
        Wild Rookie,
        Calculated Racer,
        Speed Demon,
        Street Fighter,
        Seasoned Veteran,
        Future Champion,
        Ol Reliable,
        Pay Driver,
        Reigning Champion
    )

    IF Driver.Archtype = "Veteran Defender" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Wild Rookie" THEN

        Driver.Age = Random FROM (16-24)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Calculated Racer" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Speed Demon" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (34-66),
            Aggression: Random FROM (34-66),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Street Fighter" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (0-33),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Seasoned Veteran" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Future Champion" THEN

        Driver.Age = Random FROM (16-24)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (34-66),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Ol Reliable" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (34-66),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Pay Driver" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (0-33),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Reigning Champion" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (67-100)
        )

    END IF

    RETURN Driver
END FUNCTION
'''
from dataclasses import dataclass
from itertools import count
from random import choice, randint

_DRIVER_ID_COUNTER = count(0)

ARCHETYPES = (
    "Veteran Defender",
    "Wild Rookie",
    "Calculated Racer",
    "Speed Demon",
    "Street Fighter",
    "Seasoned Veteran",
    "Future Champion",
    "Ol Reliable",
    "Pay Driver",
    "Reigning Champion",
)

FIRST_NAMES = ("Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Jamie", "Quinn", "Avery", "Parker")
LAST_NAMES = ("Stone", "Brooks", "Hart", "Cole", "Reed", "Bennett", "Foster", "Hayes", "Shaw", "Vaughn")


@dataclass(frozen=True)
class DriverStats:
    speed: int
    handling: int
    aggression: int
    consistency: int


@dataclass(frozen=True)
class Driver:
    id: int
    name: str
    archetype: str
    age: int
    stats: DriverStats


def _random_name() -> str:
    return f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}"


def _random_stats(ranges: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]) -> DriverStats:
    speed, handling, aggression, consistency = ranges
    return DriverStats(
        speed=randint(*speed),
        handling=randint(*handling),
        aggression=randint(*aggression),
        consistency=randint(*consistency),
    )


def generate_driver() -> Driver:
    archetype = choice(ARCHETYPES)

    if archetype == "Veteran Defender":
        age = randint(36, 50)
        stats = _random_stats(((0, 33), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Wild Rookie":
        age = randint(16, 24)
        stats = _random_stats(((67, 100), (67, 100), (67, 100), (0, 33)))
    elif archetype == "Calculated Racer":
        age = randint(25, 35)
        stats = _random_stats(((34, 66), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Speed Demon":
        age = randint(25, 35)
        stats = _random_stats(((67, 100), (34, 66), (34, 66), (0, 33)))
    elif archetype == "Street Fighter":
        age = randint(25, 35)
        stats = _random_stats(((34, 66), (0, 33), (67, 100), (34, 66)))
    elif archetype == "Seasoned Veteran":
        age = randint(36, 50)
        stats = _random_stats(((34, 66), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Future Champion":
        age = randint(16, 24)
        stats = _random_stats(((67, 100), (67, 100), (34, 66), (34, 66)))
    elif archetype == "Ol Reliable":
        age = randint(36, 50)
        stats = _random_stats(((0, 33), (34, 66), (0, 33), (34, 66)))
    elif archetype == "Pay Driver":
        age = randint(36, 50)
        stats = _random_stats(((0, 33), (0, 33), (0, 33), (0, 33)))
    else:
        age = randint(25, 35)
        stats = _random_stats(((67, 100), (67, 100), (67, 100), (67, 100)))

    return Driver(
        id=next(_DRIVER_ID_COUNTER),
        name=_random_name(),
        archetype=archetype,
        age=age,
        stats=stats,
    )
