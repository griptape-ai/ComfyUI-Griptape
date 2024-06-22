import os

from griptape.config import (
    AmazonBedrockStructureConfig,
    AnthropicStructureConfig,
    GoogleStructureConfig,
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AmazonBedrockPromptDriver,
    AnthropicImageQueryDriver,
    AnthropicPromptDriver,
    BedrockClaudeImageQueryModelDriver,
    OllamaPromptDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiImageQueryDriver,
)
from griptape.tokenizers import SimpleTokenizer

from ..py.griptape_config import get_config
from .base_config import gtUIBaseConfig
from .utilities import get_ollama_models


class gtUIEnv:
    """
    The Griptape Environment Config
    Setting environment variables
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "Environment Vars": ("STRING", {"default": "ENV=", "multiline": True})
            },
        }

    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ENVIRS",)
    OUTPUT_NODE = True

    CATEGORY = "Griptape"

    def run(self, **kwargs):
        envirs = kwargs.get("Environment Vars", "")
        environment_vars = []
        for envir in envirs.split("\n"):
            if "=" in envir:
                key, value = envir.split("=", 1)
                if key and value:
                    os.environ[key] = value
                    environment_vars.append(f"{key}={value}")
        return (environment_vars,)


ollama_models = get_ollama_models()
ollama_models.append("")


class gtUILMStudioStructureConfig(gtUIBaseConfig):
    """
    The Griptape LM Studio Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {},
            "required": {
                "prompt_model": (
                    ["STRING"],
                    {"default": "llama3"},
                ),
            },
        }

    def create(
        self,
        prompt_model,
    ):
        custom_config = StructureConfig(
            prompt_driver=OpenAiChatPromptDriver(
                model=prompt_model,
                base_url="http://localhost:11434/v1",
                api_key="",
                tokenizer=SimpleTokenizer(
                    characters_per_token=4,
                    max_input_tokens=1024,
                    max_output_tokens=1024,
                ),
            ),
        )

        return (custom_config,)


class gtUIOllamaStructureConfig(gtUIBaseConfig):
    """
    The Griptape Ollama Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {},
            "required": {
                "prompt_model": (
                    ollama_models,
                    {"default": ollama_models[0]},
                ),
            },
        }

    def create(
        self,
        prompt_model,
    ):
        custom_config = StructureConfig(
            prompt_driver=OllamaPromptDriver(model=prompt_model),
        )

        return (custom_config,)


amazonBedrockPromptModels = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]
amazonBedrockImageQueryModels = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
]


class gtUIAmazonBedrockStructureConfig(gtUIBaseConfig):
    """
    The Griptape Amazon Bedrock Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {},
            "required": {
                "prompt_model": (
                    amazonBedrockPromptModels,
                    {"default": amazonBedrockPromptModels[0]},
                ),
                "image_query_model": (
                    amazonBedrockImageQueryModels,
                    {"default": amazonBedrockImageQueryModels[0]},
                ),
            },
        }

    def create(
        self,
        prompt_model,
        image_query_model,
    ):
        custom_config = AmazonBedrockStructureConfig()
        custom_config.prompt_driver = AmazonBedrockPromptDriver(model=prompt_model)
        custom_config.image_query_driver = AmazonBedrockImageQueryDriver(
            image_query_model_driver=BedrockClaudeImageQueryModelDriver(),
            model=image_query_model,
        )

        return (custom_config,)


class gtUIGoogleStructureConfig(gtUIBaseConfig):
    """
    The Griptape Google Structure Config
    """

    def create(
        self,
    ):
        custom_config = GoogleStructureConfig()

        return (custom_config,)


anthropicPromptModels = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
anthropicImageQueryModels = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
voyageAiEmbeddingModels = [
    "voyage-large-2",
]


class gtUIAnthropicStructureConfig(gtUIBaseConfig):
    """
    The Griptape Anthropic Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {},
            "required": {
                "prompt_model": (
                    anthropicPromptModels,
                    {"default": anthropicPromptModels[0]},
                ),
                "image_query_model": (
                    anthropicImageQueryModels,
                    {"default": anthropicImageQueryModels[0]},
                ),
            },
        }

    def create(
        self,
        prompt_model,
        image_query_model,
    ):
        custom_config = AnthropicStructureConfig()
        custom_config.prompt_driver = AnthropicPromptDriver(model=prompt_model)
        custom_config.image_query_driver = AnthropicImageQueryDriver(
            model=image_query_model
        )

        return (custom_config,)


class gtUIOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                    {"default": "gpt-4o"},
                ),
                "image_query_model": (
                    ["gpt-4o", "gpt-4-vision-preview"],
                    {"default": "gpt-4o"},
                ),
            }
        )
        return inputs

    def create(self, prompt_model, image_query_model):
        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        custom_config = StructureConfig(
            prompt_driver=OpenAiChatPromptDriver(
                model=prompt_model, api_key=OPENAI_API_KEY
            ),
            embedding_driver=OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY),
            image_generation_driver=OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dalle-e-3",
            ),
            image_query_driver=OpenAiImageQueryDriver(
                api_key=OPENAI_API_KEY, model=image_query_model
            ),
        )

        return (custom_config,)
