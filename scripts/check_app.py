"""Quick launch checks for the ECON 101 Streamlit app."""

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


REQUIRED_PACKAGES = [
    "streamlit",
    "plotly",
    "pandas",
    "numpy",
    "folium",
    "streamlit_folium",
]

PROJECT_MODULES = [
    "modules_data",
]


def main():
    for module_name in REQUIRED_PACKAGES:
        if find_spec(module_name) is None:
            raise ModuleNotFoundError(module_name)
        print(f"ok: {module_name}")
    for module_name in PROJECT_MODULES:
        import_module(module_name)
        print(f"ok: {module_name}")


if __name__ == "__main__":
    main()
