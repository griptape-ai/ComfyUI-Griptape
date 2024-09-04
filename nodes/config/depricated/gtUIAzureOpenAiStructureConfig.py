from griptape.configs.drivers import AzureOpenAiDriversConfig

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AzureOpenAiChatPromptDriver,
    AzureOpenAiEmbeddingDriver,
    AzureOpenAiImageGenerationDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

DEFAULT_AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
DEFAULT_AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"


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
        params = {}
        params["model"] = kwargs.get("prompt_model", "gpt-4o")
        params["temperature"] = kwargs.get("temperature", 0.7)
        params["seed"] = kwargs.get("seed", 12341)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        params["azure_deployment"] = kwargs.get("prompt_model_deployment_name", "gpt4o")
        params["use_native_tools"] = kwargs.get("use_native_tools", False)
        params["stream"] = kwargs.get("stream", False)
        image_generation_driver = kwargs.get("image_generation_driver", None)

        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        AZURE_OPENAI_API_KEY = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_AZURE_OPENAI_API_KEY)
        )
        AZURE_OPENAI_ENDPOINT = self.getenv(
            kwargs.get("azure_endpoint_env_var", DEFAULT_AZURE_OPENAI_ENDPOINT)
        )

        params["api_key"] = self.getenv("AZURE_OPENAI_API_KEY")
        params["azure_endpoint"] = self.getenv("AZURE_OPENAI_ENDPOINT")

        prompt_driver = AzureOpenAiChatPromptDriver(**params)
        embedding_driver = AzureOpenAiEmbeddingDriver(
            api_key=self.getenv(AZURE_OPENAI_API_KEY),
            azure_endpoint=self.getenv(AZURE_OPENAI_ENDPOINT),
        )

        if not image_generation_driver:
            image_generation_driver = AzureOpenAiImageGenerationDriver(
                azure_deployment="dall-e-3",
                model="dall-e-3",
                azure_endpoint=params["azure_endpoint"],
                api_key=params["api_key"],
            )

        custom_config = AzureOpenAiDriversConfig(
            prompt_driver=prompt_driver,
            embedding_driver=embedding_driver,
            image_generation_driver=image_generation_driver,
            azure_endpoint=params["azure_endpoint"],
            api_key=params["api_key"],
        )

        return (custom_config,)
