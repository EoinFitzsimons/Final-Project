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


def _generate_test_drivers():
    mod = _load_driver_module()

    # Generate 10 drivers, matching the number used in the race simulation.
    drivers = [mod.generate_driver() for _ in range(10)]

    return mod, drivers


def test_driver_creation_count():

    mod, drivers = _generate_test_drivers()

    # Confirm the correct number of drivers were created.
    assert len(drivers) == 10


def test_driver_names_are_not_empty():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure every driver has an assigned name.
        assert driver.name != ""


def test_driver_nationalities_are_valid():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure every driver has a recognised nationality.
        assert driver.nationality in mod.NATIONALITIES


def test_driver_archetypes_are_valid():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure every driver has a recognised racing archetype.
        assert driver.archetype in mod.ARCHETYPES


def test_driver_age_range():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure driver age is realistic based on the generation ranges.
        assert 16 <= driver.age <= 50


def test_driver_speed_range():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure all performance statistics are within valid limits.
        assert 0 <= driver.stats.speed <= 100


def test_driver_handling_range():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure all performance statistics are within valid limits.
        assert 0 <= driver.stats.handling <= 100


def test_driver_aggression_range():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure all performance statistics are within valid limits.
        assert 0 <= driver.stats.aggression <= 100


def test_driver_consistency_range():

    mod, drivers = _generate_test_drivers()

    for driver in drivers:

        # Ensure all performance statistics are within valid limits.
        assert 0 <= driver.stats.consistency <= 100


def test_unique_driver_ids():

    mod, drivers = _generate_test_drivers()

    # Extract generated IDs and names for validation.
    driver_ids = [driver.id for driver in drivers]

    # IDs should never be duplicated.
    assert len(driver_ids) == len(set(driver_ids))


def test_unique_driver_names():

    mod, drivers = _generate_test_drivers()

    # Extract generated IDs and names for validation.
    driver_names = [driver.name for driver in drivers]

    # Names should be unique within a generated race.
    assert len(driver_names) == len(set(driver_names))