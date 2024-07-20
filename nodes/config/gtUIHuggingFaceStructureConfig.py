from dotenv import load_dotenv
from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    HuggingFaceHubPromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

default_api_key = "HUGGINGFACE_HUB_ACCESS_TOKEN"


class gtUIHuggingFaceStructureConfig(gtUIBaseConfig):
    """
    Create a HuggingFace Structure Config
    """

    DESCRIPTION = "HuggingFace Structure Config."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "prompt_model": ("STRING", {"default": "HuggingFaceH4/zephyr-7b-beta"}),
                "api_token_env_var": (
                    "STRING",
                    {"default": default_api_key},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", None)
        temperature = kwargs.get("temperature", 0.7)

        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        api_token = self.getenv(kwargs.get("api_token_env_var", default_api_key))

        configs = {}
        if prompt_model and api_token:
            configs["prompt_driver"] = HuggingFaceHubPromptDriver(
                model=prompt_model,
                api_token=api_token,
                max_attempts=max_attempts,
                temperature=temperature,
            )
        custom_config = StructureConfig(**configs)

        return (custom_config,)
