from griptape.drivers import HuggingFaceHubPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_model = "HuggingFaceH4/zephyr-7b-beta"

DEFAULT_API_KEY_ENV_VAR = "HUGGINGFACE_HUB_ACCESS_TOKEN"


class gtUIHuggingFaceHubPromptDriver(gtUIBasePromptDriver):
    DESCRIPTION = "Hugging Face Hub Prompt Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update({})
        inputs["optional"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "api_token_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        # del inputs["optional"]["stream"]
        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_token_env_var", DEFAULT_API_KEY_ENV_VAR))
        model = kwargs.get("model", default_model)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        temperature = kwargs.get("temperature", 0.7)
        use_native_tools = kwargs.get("use_native_tools", False)
        params = {
            "api_token": api_key,
            "model": model,
            "temperature": temperature,
            "use_native_tools": use_native_tools,
        }
        if max_attempts:
            params["max_attempts"] = max_attempts
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = HuggingFaceHubPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
