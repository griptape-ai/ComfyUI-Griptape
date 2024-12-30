import os
from typing import Any, Tuple


class gtUIBase:
    """
    Griptape Base Node
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {},
            "hidden": {"prompt": "PROMPT"},
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "create"

    CATEGORY = "Griptape"

    def run_envs(self, kwargs):
        prompt = kwargs.get("prompt", None)

        if prompt:
            # Get all environment variables from nodes named "Griptape Agent Config: Environment Variables"
            env_vars = {}
            for node_id, node_data in prompt.items():
                if (
                    node_data["class_type"]
                    == "Griptape Agent Config: Environment Variables"
                ):
                    env_vars_input = node_data["inputs"].get("Environment Vars", "")
                    if isinstance(env_vars_input, str):
                        for line in env_vars_input.split("\n"):
                            if "=" in line:
                                key, value = line.strip().split("=", 1)
                                env_vars[key] = value
                    else:
                        # This node will need to evaluate
                        pass

            # Set the environment variables
            for key, value in env_vars.items():
                os.environ[key] = value
                print(f"Set environment variable: {key}")

    def create(self, **kwargs) -> Tuple[Any, ...]:
        self.run_envs(kwargs)
        return (None,)
