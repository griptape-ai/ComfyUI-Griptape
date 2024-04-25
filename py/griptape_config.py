import json
import os
from server import PromptServer

# Setup to compute file paths relative to the directory containing this script
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)  # Move one directory up to the parent directory

DEFAULT_CONFIG_FILE = os.path.join(PARENT_DIR, "griptape_config.json.default")
USER_CONFIG_FILE = os.path.join(PARENT_DIR, "griptape_config.json")


def load_config_file(config_path):
    """
    Load the JSON configuration from the specified file path.
    """
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist


def get_env_config(config):
    """
    Extract the 'env' section from the loaded configuration.
    """
    return config.get("env", {})  # Return an empty dict if 'env' is not found


def set_environment_variables(config_file=USER_CONFIG_FILE):
    """
    Set environment variables from the key/value pairs in the 'env' configuration.
    """
    config = load_config_file(config_file)
    env_config = get_env_config(config)
    for key, value in env_config.items():
        os.environ[key] = str(value)
        print(f"Set ENV {key} = {value}")  # Optional: for debugging purposes


def load_config(default_file, user_file):
    # Load default configuration
    with open(default_file, "r") as file:
        default_config = json.load(file)

    # Load user configuration if it exists, otherwise create an empty dict
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            try:
                user_config = json.load(file)
            except json.JSONDecodeError:
                user_config = {}
    else:
        user_config = {}

    # Merge configurations: add missing keys from default to user config
    merged_config = merge_configs(default_config, user_config)

    # Update user config with values from environment variables where empty
    update_config_with_env(merged_config)

    # Save the updated configuration back to the user file
    with open(user_file, "w") as file:
        json.dump(merged_config, file, indent=4)

    return merged_config


def merge_configs(default_config, user_config):
    """Recursively merge default and user configurations."""
    for key, value in default_config.items():
        if key not in user_config:
            user_config[key] = value
        elif isinstance(value, dict):
            user_config[key] = merge_configs(value, user_config.get(key, {}))
    return user_config


def update_config_with_env(config):
    """Fill empty config values with environment variables if they exist."""
    for key, value in config.items():
        if isinstance(value, dict):
            update_config_with_env(value)  # Recursive call for nested dictionaries
        else:
            if value == "" and key in os.environ:
                config[key] = os.environ[key]


# Load and merge configurations
final_config = load_config(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)


def get_config(key, default=None):
    parts = key.split(".")
    value = final_config
    try:
        for part in parts:
            value = value[part]
        return value
    except KeyError:
        return default


def send_config_to_js(config_file=USER_CONFIG_FILE):
    # Assuming your configuration is loaded into a dictionary called config
    env_config = load_config_file(config_file)["env"]
    PromptServer.instance.send_sync("config-update", env_config)
