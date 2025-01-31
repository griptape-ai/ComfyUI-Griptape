# pyright: reportMissingImports=false
import json
import os
import re

from dotenv import load_dotenv

from server import PromptServer

load_dotenv()


class GriptapeSettings:
    def __init__(self):
        # Get the directory where this Python file is located
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.current_dir = current_dir
        self.comfyui_dir = os.path.dirname(os.path.dirname(current_dir))
        self.settings_file = ""
        self.settings_api_keys_file = os.path.join(
            current_dir, "js", "griptape_api_keys.js"
        )
        self.key_config = {}
        self.settings = {}
        self.all_services = []

        # Call automatically on instantiation
        self.setup()

    def get_settings_file(self):
        """Get the settings file path for the default user"""
        # Get the user manager
        user_manager = PromptServer.instance.user_manager

        # Get the users directory
        users_dir = os.path.dirname(user_manager.get_users_file())
        # Use the default user directory (usually the first one we find)
        user_dirs = [
            d
            for d in os.listdir(users_dir)
            if os.path.isdir(os.path.join(users_dir, d))
        ]
        if not user_dirs:
            # Create a users dir if it doesn't exist
            user_dirs[0] = os.path.join(self.comfyui_dir, "user")
            os.mkdir(user_dirs[0])
            print(f"No user directories found.. creating {user_dirs[0]}")
        # Get the settings file path
        self.settings_file = os.path.join(
            users_dir, user_dirs[0], "comfy.settings.json"
        )

    def read_settings(self):
        """Read the settings file"""
        # Read the settings file
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)

    def get_settings_key(self, key, root="Griptape"):
        """Get a key from the settings"""
        # Get the key from the settings
        return self.settings.get(f"{root}.{key}", None)

    def overwrite_settings_key(self, key, value):
        """Overwrite the key in the settings"""
        self.settings[key] = value

    def set_settings_key(self, key, value):
        """Set the key to the settings only if it's not already set or if it's blank"""
        if key not in self.settings or str(self.settings[key]).strip() == "":
            self.settings[key] = value

    def save_settings(self):
        """Save the settings to the settings file"""
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_key_config(self):
        """Read the configuration from the Javascript file"""
        try:
            with open(self.settings_api_keys_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract everything between the first { and the last }
            match = re.search(
                r"export const keys_organized = ({.*})",
                content,
                re.DOTALL | re.MULTILINE,
            )
            if match:
                # Get the object definition
                obj_str = match.group(1)

                # Convert JavaScript object syntax to valid JSON
                # Replace single quotes with double quotes
                obj_str = obj_str.replace("'", '"')
                # Remove trailing commas (which are valid in JS but not JSON)
                obj_str = re.sub(r",(\s*[}\]])", r"\1", obj_str)

                # Parse as JSON
                self.key_config = json.loads(obj_str)
        except Exception as e:
            print(f"Error reading key config: {str(e)}")

    def get_settings_key_or_use_env(self, env, root="Griptape"):
        """Get an environment variable from the OS"""
        api_key = self.get_settings_key(env, root=root)
        if api_key:
            # Forces the API key to be set into the environment
            os.environ[env] = api_key
        else:
            api_key = os.getenv(env, None)
            if api_key:
                self.set_settings_key(f"{root}.{env}", api_key)
                self.save_settings()

        if not api_key:
            print(f"   \033[34m- \033[92m[WARNING]: {env} is not set\033[0m\n")
            return None
            # raise ValueError(f"Environment variable {env} is not set")
        return api_key

    def get_all_services(self):
        """Get all the services from the key config"""
        self.all_services = list(self.key_config.keys())

    def get_keys_for_service(self, service_name):
        """Get the keys for a service"""
        return self.key_config.get(service_name, [])

    def setup(self):
        self.get_settings_file()
        self.read_settings()
