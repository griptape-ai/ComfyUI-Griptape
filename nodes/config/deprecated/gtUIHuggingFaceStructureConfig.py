from dotenv import load_dotenv
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    HuggingFaceHubPromptDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

DEFAULT_API_KEY = "HUGGINGFACE_HUB_ACCESS_TOKEN"


class gtUIHuggingFaceStructureConfig(gtUIBaseConfig):
    """
    Create a HuggingFace Structure Config
    """

    DESCRIPTION = "HuggingFace Structure Config."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "prompt_model": ("STRING", {"default": "HuggingFaceH4/zephyr-7b-beta"}),
                "api_token_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY},
                ),
            }
        )
        del inputs["optional"]["max_tokens"]

        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", None)
        temperature = kwargs.get("temperature", 0.7)
        stream = kwargs.get("stream", False)
        max_attempts = kwargs.get("max_attempts_on_fail", 2)
        use_native_tools = kwargs.get("use_native_tools", False)
        api_token = self.getenv(kwargs.get("api_token_env_var", DEFAULT_API_KEY))
        configs = {}
        if prompt_model and api_token:
            configs["prompt_driver"] = HuggingFaceHubPromptDriver(
                model=prompt_model,
                api_token=api_token,
                max_attempts=max_attempts,
                temperature=temperature,
                stream=stream,
                use_native_tools=use_native_tools,
            )
        custom_config = DriversConfig(**configs)

        return (custom_config,)
