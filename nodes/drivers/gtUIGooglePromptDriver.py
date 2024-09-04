from griptape.drivers import GooglePromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro"]

DEFAULT_API_KEY_ENV_VAR = "GOOGLE_API_KEY"


class gtUIGooglePromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": (models, {"default": models[0]}),
                "google_api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("google_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("model", None)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        params = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            "max_attempts": max_attempts,
            "use_native_tools": use_native_tools,
        }

        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = GooglePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
