from griptape.configs.drivers import (
    GoogleDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    GooglePromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

google_models = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]

DEFAULT_API_KEY = "GOOGLE_API_KEY"


class gtUIGoogleStructureConfig(gtUIBaseConfig):
    """
    The Griptape Google Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "prompt_model": (
                    google_models,
                    {"default": google_models[0]},
                ),
            },
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    DESCRIPTION = (
        "Google Structure Config. Use Google's models for prompt and image query."
    )

    def create(
        self,
        **kwargs,
    ):
        self.run_envs(kwargs)
        params = {}
        temperature = kwargs.get("temperature", 0.7)
        prompt_model = kwargs.get("prompt_model", google_models[0])
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        custom_config = GoogleDriversConfig(
            prompt_driver=GooglePromptDriver(
                model=prompt_model,
                temperature=temperature,
                max_attempts=max_attempts,
                api_key=api_key,
                use_native_tools=use_native_tools,
                **params,
            ),
        )

        return (custom_config,)
