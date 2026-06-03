"""Load default configuration from packaged YAML."""

import yaml

from pycommonist.core.resources import resource_path


def load_config_as_dict():
    path = resource_path("config", "general.yaml")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


_config = load_config_as_dict()


class LeftFrameConfig:
    _config = _config["left_frame"]
    username = _config["username"]
    source = _config["source"]
    author = _config["author"]
    categories = _config["categories"]
    license = _config["license"]
    language = _config["language"]


class RightFrameConfig:
    _config = _config["right_frame"]
    default_image_sort = _config["default_image_sort"]
