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
                "top_p": (
                    "FLOAT",
                    {
                        "default": 0.999,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": "Controls the cumulative probability distribution cutoff. The model will only consider the top p% most probable tokens.",
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 250,
                        "min": 0,
                        "max": 500,
                        "step": 1,
                        "tooltip": "Limits the number of tokens considered for each step of the generation. Pevents the model from focusing too narrowly on the top choices.",
                    },
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
        top_p = kwargs.get("top_p", None)
        top_k = kwargs.get("top_k", None)
        params = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            "max_attempts": max_attempts,
            "use_native_tools": use_native_tools,
        }

        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        if top_p:
            params["top_p"] = top_p
        if top_k:
            params["top_k"] = top_k
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = GooglePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
