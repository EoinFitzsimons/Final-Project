from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path


def _load_driver_module(): #Dynamically loads the driver module.This allows the test to access driver.py without requiring the project package structure to be installed.
    repo_root = Path(__file__).resolve().parents[2]
    driver_path = repo_root / "src" / "core" / "driver.py"

    spec = spec_from_file_location("driver", str(driver_path))

    assert spec is not None
    assert spec.loader is not None

    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_generate_driver_creation():

    mod = _load_driver_module()

    # Generate 10 drivers, matching the number used in the race simulation.
    drivers = [mod.generate_driver() for _ in range(10)]

    # Confirm the correct number of drivers were created.
    assert len(drivers) == 10

    # Extract generated IDs and names for validation.
    driver_ids = [driver.id for driver in drivers]
    driver_names = [driver.name for driver in drivers]

    for driver in drivers:

        # Ensure every driver has an assigned name.
        assert driver.name != ""

        # Ensure every driver has a recognised nationality.
        assert driver.nationality in mod.NATIONALITIES

        # Ensure every driver has a recognised racing archetype.
        assert driver.archetype in mod.ARCHETYPES

        # Ensure driver age is realistic based on the generation ranges.
        assert 16 <= driver.age <= 50

        # Ensure all performance statistics are within valid limits.
        assert 0 <= driver.stats.speed <= 100
        assert 0 <= driver.stats.handling <= 100
        assert 0 <= driver.stats.aggression <= 100
        assert 0 <= driver.stats.consistency <= 100

    # IDs should never be duplicated.
    assert len(driver_ids) == len(set(driver_ids))

    # Names should be unique within a generated race.
    assert len(driver_names) == len(set(driver_names))