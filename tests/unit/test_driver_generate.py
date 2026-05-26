from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path


def _load_driver_module():
    repo_root = Path(__file__).resolve().parents[2]
    driver_path = repo_root / "src" / "core" / "driver.py"
    spec = spec_from_file_location("driver", str(driver_path))
    assert spec is not None
    mod = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_generate_three_drivers():
    mod = _load_driver_module()
    generate_driver = mod.generate_driver

    drivers = [generate_driver() for _ in range(3)]
    for d in drivers:
        print(d)
    assert len(drivers) == 3
