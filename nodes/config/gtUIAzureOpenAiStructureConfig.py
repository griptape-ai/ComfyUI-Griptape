import os

from griptape.configs.drivers import AzureOpenAiDriversConfig

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AzureOpenAiChatPromptDriver,
    AzureOpenAiEmbeddingDriver,
    AzureOpenAiImageGenerationDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

DEFAULT_AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEFAULT_AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


class gtUIAzureOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "Azure OpenAI Structure Config. Requires AZURE_OPENAI_ENDPOINT_3 and AZURE_OPENAI_API_KEY_3"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    ["gpt-4o", "gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"],
                    {"default": "gpt-4o"},
                ),
                "prompt_model_deployment_name": (
                    "STRING",
                    {"default": "gpt4o"},
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AZURE_OPENAI_API_KEY},
                ),
                "azure_endpoint_env_var": (
                    "STRING",
                    {"default": DEFAULT_AZURE_OPENAI_ENDPOINT},
                ),
            }
        )

        return inputs

    def create(
        self,
        **kwargs,
    ):
        prompt_model = kwargs.get("prompt_model", "gpt-4o")
        temperature = kwargs.get("temperature", 0.7)
        seed = kwargs.get("seed", 12341)
        image_generation_driver = kwargs.get("image_generation_driver", None)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        prompt_model_deployment_id = kwargs.get("prompt_model_deployment_name", "gpt4o")
        stream = kwargs.get("stream", False)
        AZURE_OPENAI_API_KEY = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_AZURE_OPENAI_API_KEY)
        )
        AZURE_OPENAI_ENDPOINT = self.getenv(
            kwargs.get("azure_endpoint_env_var", DEFAULT_AZURE_OPENAI_ENDPOINT)
        )

        prompt_driver = AzureOpenAiChatPromptDriver(
            api_key=AZURE_OPENAI_API_KEY,
            model=prompt_model,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=prompt_model_deployment_id,
            temperature=temperature,
            seed=seed,
            max_attempts=max_attempts,
            stream=stream,
        )
        embedding_driver = AzureOpenAiEmbeddingDriver(
            api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT
        )

        if not image_generation_driver:
            image_generation_driver = AzureOpenAiImageGenerationDriver(
                azure_deployment="dall-e-3",
                model="dall-e-3",
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
            )

        custom_config = AzureOpenAiDriversConfig(
            prompt_driver=prompt_driver,
            embedding_driver=embedding_driver,
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
