import json
import os


def load_config(default_file, user_file):
    # Load default configuration
    with open(default_file, "r") as file:
        default_config = json.load(file)

    # Load user configuration if it exists, otherwise create an empty dict
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_config = json.load(file)
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
