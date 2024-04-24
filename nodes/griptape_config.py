# This config code from rgthree-comfy - an incredibly helpful library!
# https://github.com/rgthree/rgthree-comfy
import os
import json
import re

from .utils import get_dict_value, set_dict_value, dict_has_key


def get_config_value(key):
    return get_dict_value(GRIPTAPE_CONFIG, key)


def extend_config(default_config, user_config):
    """Returns a new config dict combining user_config into defined keys for default_config."""
    cfg = {}
    for key, value in default_config.items():
        if key not in user_config:
            cfg[key] = value
        elif isinstance(value, dict):
            cfg[key] = extend_config(value, user_config[key])
        else:
            cfg[key] = user_config[key] if key in user_config else value
    return cfg


def set_user_config(data: dict):
    """Sets the user configuration."""
    count = 0
    for key, value in data.items():
        if dict_has_key(DEFAULT_CONFIG, key):
            set_dict_value(USER_CONFIG, key, value)
            set_dict_value(GRIPTAPE_CONFIG, key, value)
            count += 1
    if count > 0:
        write_user_config()


def get_griptape_default_config():
    """Gets the default configuration."""
    with open(DEFAULT_CONFIG_FILE, "r", encoding="UTF-8") as file:
        config = re.sub(r"(?:^|\s)//.*", "", file.read(), flags=re.MULTILINE)
    return json.loads(config)


def get_griptape_user_config():
    """Gets the user configuration."""
    if os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, "r", encoding="UTF-8") as file:
            config = re.sub(r"(?:^|\s)//.*", "", file.read(), flags=re.MULTILINE)
        return json.loads(config)
    else:
        return {}


def write_user_config():
    """Writes the user configuration."""
    with open(USER_CONFIG_FILE, "w+", encoding="UTF-8") as file:
        json.dump(USER_CONFIG, file, sort_keys=True, indent=2, separators=(",", ": "))


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(THIS_DIR, "..", "griptape_config.json.default")
USER_CONFIG_FILE = os.path.join(THIS_DIR, "..", "griptape_config.json")
DEFAULT_CONFIG = get_griptape_default_config()

USER_CONFIG = get_griptape_user_config()

# Migrate old config options into "features"
needs_to_write_user_config = False

if needs_to_write_user_config is True:
    print("writing new user config.")
    write_user_config()

GRIPTAPE_CONFIG = extend_config(DEFAULT_CONFIG, USER_CONFIG)
