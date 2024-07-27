from griptape.drivers import GooglePromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]

DEFAULT_API_KEY_ENV_VAR = "GOOGLE_API_KEY"


class gtUIGooglePromptDriver(gtUIBasePromptDriver):
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

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR))
        model = kwargs.get("model", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)

        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts

        try:
            driver = GooglePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
