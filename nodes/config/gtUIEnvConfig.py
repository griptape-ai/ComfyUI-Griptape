import os

# StructureGlobalDriversConfig,

default_env = "ENV=VALUE"


class gtUIEnvConfig:
    """
    The Griptape Environment Config
    Setting environment variables
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "Environment Vars": (
                    "STRING",
                    {
                        "default": default_env,
                        "multiline": True,
                        "tooltip": "Set your environment variables.\nUse the format 'KEY=VALUE'.\nAdd each variable on a new line.",
                    },
                ),
            },
        }

    FUNCTION = "run"
    RETURN_TYPES = ("ENV",)
    RETURN_NAMES = ("ENV",)

    CATEGORY = "Griptape/Agent Configs"
    OUTPUT_NODE = True

    def run(self, **kwargs):
        envirs = kwargs.get("Environment Vars", default_env)
        environment_vars = []
        if envirs == default_env:
            print("No custom environment variables set.")
            return ()

        envirs = envirs.strip()
        for envir in envirs.split("\n"):
            envir = envir.strip()
            if "=" in envir:
                key, value = envir.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key and value:
                    os.environ[key] = value
                    environment_vars.append(f"{key}={value}")
                    print(f"Environment variable set: {key}")
                else:
                    print(f"Warning: Invalid environment variable format: {envir}")
            else:
                print(f"Warning: Skipping invalid line: {envir}")

        if environment_vars:
            print(f"Total environment variables set: {len(environment_vars)}")
        else:
            print("No valid environment variables were set.")
        return (environment_vars,)
