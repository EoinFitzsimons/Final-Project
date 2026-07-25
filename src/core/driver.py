from dataclasses import dataclass
from itertools import count
from random import SystemRandom
from typing import Optional

_DRIVER_ID_COUNTER = count(0)
_RNG = SystemRandom()
_USED_NAMES: set[str] = set() #keep track of selected names.

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

NATIONALITIES = (
    "British",
    "French",
    "German",
    "Italian",
    "Spanish",
    "Brazilian",
    "Japanese",
    "Mexican",
    "Swedish",
    "Australian",
)

# Mapping of nationality -> (first_names_tuple, last_names_tuple)
NAMES_BY_NATIONALITY = {
    "British": (
        ("Oliver", "Jack", "George", "Harry"),
        ("Smith", "Bennett", "Hughes", "Clark"),
    ),
    "French": (
        ("Antoine", "Lucas", "Jules", "Pierre"),
        ("Dubois", "Moreau", "Lefèvre", "Laurent"),
    ),
    "German": (
        ("Lukas", "Max", "Nico", "Jonas"),
        ("Müller", "Schmidt", "Fischer", "Weber"),
    ),
    "Italian": (
        ("Matteo", "Luca", "Alessandro", "Marco"),
        ("Rossi", "Bianchi", "Romano", "Conti"),
    ),
    "Spanish": (
        ("Alejandro", "Carlos", "Javier", "Sergio"),
        ("García", "Fernández", "Martínez", "López"),
    ),
    "Brazilian": (
        ("João", "Pedro", "Rafael", "Lucas"),
        ("Souza", "Silva", "Oliveira", "Pereira"),
    ),
    "Japanese": (
        ("Takumi", "Yuki", "Haruki", "Kenta"),
        ("Sato", "Suzuki", "Takahashi", "Tanaka"),
    ),
    "Mexican": (
        ("Diego", "Miguel", "José", "Luis"),
        ("Hernández", "Rodríguez", "González", "Ramírez"),
    ),
    "Swedish": (
        ("Erik", "Johan", "Viktor", "Anton"),
        ("Andersson", "Johansson", "Karlsson", "Larsson"),
    ),
    "Australian": (
        ("Liam", "Noah", "Ethan", "James"),
        ("Wilson", "Taylor", "Brown", "Harris"),
    ),
}



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
    nationality: str
    archetype: str
    age: int
    stats: DriverStats


def _random_name(nationality: Optional[str] = None) -> tuple[str, str]:
    """Return (full_name, nationality).

    If `nationality` is None a nationality is chosen at random.
    """
    if nationality is None:
        nationality = _RNG.choice(NATIONALITIES)

    # Use the chosen nationality to keep the generated name consistent with the driver's profile.
    first_names, last_names = NAMES_BY_NATIONALITY[nationality]

    while True:
        full_name = f"{_RNG.choice(first_names)} {_RNG.choice(last_names)}"

        if full_name not in _USED_NAMES:
            _USED_NAMES.add(full_name)
            return full_name, nationality


def _random_stats(ranges: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]) -> DriverStats:
    speed, handling, aggression, consistency = ranges
    return DriverStats(
        speed=_RNG.randint(*speed),
        handling=_RNG.randint(*handling),
        aggression=_RNG.randint(*aggression),
        consistency=_RNG.randint(*consistency),
    )


def generate_driver(archetype: str | None = None) -> Driver:
    if archetype is None:
        archetype = _RNG.choice(ARCHETYPES)

    if archetype not in ARCHETYPES:
        raise ValueError(f"Unknown archetype: {archetype}")

    if archetype == "Veteran Defender":
        age = _RNG.randint(36, 50)
        stats = _random_stats(((0, 33), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Wild Rookie":
        age = _RNG.randint(16, 24)
        stats = _random_stats(((67, 100), (67, 100), (67, 100), (0, 33)))
    elif archetype == "Calculated Racer":
        age = _RNG.randint(25, 35)
        stats = _random_stats(((34, 66), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Speed Demon":
        age = _RNG.randint(25, 35)
        stats = _random_stats(((67, 100), (34, 66), (34, 66), (0, 33)))
    elif archetype == "Street Fighter":
        age = _RNG.randint(25, 35)
        stats = _random_stats(((34, 66), (0, 33), (67, 100), (34, 66)))
    elif archetype == "Seasoned Veteran":
        age = _RNG.randint(36, 50)
        stats = _random_stats(((34, 66), (67, 100), (0, 33), (67, 100)))
    elif archetype == "Future Champion":
        age = _RNG.randint(16, 24)
        stats = _random_stats(((67, 100), (67, 100), (34, 66), (34, 66)))
    elif archetype == "Ol Reliable":
        age = _RNG.randint(36, 50)
        stats = _random_stats(((0, 33), (34, 66), (0, 33), (34, 66)))
    elif archetype == "Pay Driver":
        age = _RNG.randint(36, 50)
        stats = _random_stats(((0, 33), (0, 33), (0, 33), (0, 33)))
    else:
        age = _RNG.randint(25, 35)
        stats = _random_stats(((67, 100), (67, 100), (67, 100), (67, 100)))

    name, nationality = _random_name()

    return Driver(
        id=next(_DRIVER_ID_COUNTER),
        name=name,
        nationality=nationality,
        archetype=archetype,
        age=age,
        stats=stats,
    )
