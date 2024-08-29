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

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        del inputs["optional"]["temperature"]
        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR))
        model = kwargs.get("model", models[0])
        stream = kwargs.get("stream", False)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if max_attempts:
            params["max_attempts"] = max_attempts
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        try:
            driver = CoherePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
