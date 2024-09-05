from griptape.drivers import CoherePromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = [
    "command-r-plus",
    "command-r",
    "command",
    "command-light",
    "command-nightly",
    "command-light-nightly",
]

DEFAULT_API_KEY_ENV_VAR = "COHERE_API_KEY"


class gtUICoherePromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": (models, {"default": models[0]}),
                "cohere_api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        del inputs["optional"]["temperature"]
        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("cohere_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("model", models[0])
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        params = {
            "api_key": api_key,
            "model": model,
            "max_attempts": max_attempts,
            "use_native_tools": use_native_tools,
        }
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = CoherePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
