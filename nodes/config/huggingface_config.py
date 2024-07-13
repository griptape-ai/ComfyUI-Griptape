import os

from dotenv import load_dotenv
from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    HuggingFaceHubPromptDriver,
)

from .base_config import gtUIBaseConfig

load_dotenv()

default_string = "(use api_token_env_var)"


class gtUIHuggingFaceStructureConfig(gtUIBaseConfig):
    """
    Create an OpenAI Compatible Structure Config
    """

    DESCRIPTION = "OpenAI Compatible Structure Config."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["image_generation_driver"]
        inputs["optional"].update(
            {
                "prompt_model": ("STRING", {"default": "HuggingFaceH4/zephyr-7b-beta"}),
                "api_token_env_var": (
                    "STRING",
                    {"default": "HUGGINGFACE_HUB_ACCESS_TOKEN"},
                ),
                "api_token": (
                    "STRING",
                    {"default": default_string},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", None)
        api_token = kwargs.get("api_token", None)
        api_token_env_var = kwargs.get("api_token_env_var", None)

        if (
            not api_token or api_token.strip() == "" or api_token == default_string
        ) and api_token_env_var:
            api_token = os.getenv(api_token_env_var)

        configs = {}
        if prompt_model and api_token:
            configs["prompt_driver"] = HuggingFaceHubPromptDriver(
                model=prompt_model,
                api_token=api_token,
            )
        custom_config = StructureConfig(**configs)

        return (custom_config,)
