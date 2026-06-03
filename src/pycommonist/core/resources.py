"""Package resource paths."""

from importlib import resources


def resource_path(*parts: str) -> str:
    """Return absolute path to a file under pycommonist.resources."""
    return str(resources.files("pycommonist.resources").joinpath(*parts))
