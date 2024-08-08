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
    OUTPUT_NODE = True

    CATEGORY = "Griptape"

    def run(self, **kwargs):
        envirs = kwargs.get("Environment Vars", default_env)
        environment_vars = []
        if envirs == default_env:
            return ()
        envirs = envirs.strip()
        for envir in envirs.split("\n"):
            if "=" in envir:
                key, value = envir.split("=", 1)
                if key and value:
                    os.environ[key] = value
                    environment_vars.append(f"{key}={value}")
        return (environment_vars,)
