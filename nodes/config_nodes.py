import os

from griptape.config import (
    AmazonBedrockStructureConfig,
    AnthropicStructureConfig,
    GoogleStructureConfig,
    OpenAiStructureConfig,
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AmazonBedrockPromptDriver,
    AnthropicImageQueryDriver,
    AnthropicPromptDriver,
    BedrockClaudeImageQueryModelDriver,
    DummyImageGenerationDriver,
    GooglePromptDriver,
    OllamaPromptDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiImageQueryDriver,
)
from griptape.tokenizers import SimpleTokenizer
from griptape.utils import PromptStack

from ..py.griptape_config import get_config
from .base_config import gtUIBaseConfig
from .utilities import get_lmstudio_models, get_ollama_models


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
ollama_port = "11434"
ollama_base_url = "http://127.0.0.1"

lmstudio_models = get_lmstudio_models(port="1234")
lmstudio_models.append("")
lmstudio_port = "1234"
lmstudio_base_url = "http://127.0.0.1"


class LMStudioPromptDriver(OpenAiChatPromptDriver):
    def _prompt_stack_input_to_message(self, prompt_input: PromptStack.Input) -> dict:
        content = prompt_input.content

        if prompt_input.is_system():
            return {
                "role": "system",
                # "content": content, # This is the original line - it kept coming back blank
                "content": "Always answer with integrity and never lie.",
            }
        elif prompt_input.is_assistant():
            return {"role": "assistant", "content": content}
        else:
            return {"role": "user", "content": content}


class gtUILMStudioStructureConfig(gtUIBaseConfig):
    """
    The Griptape LM Studio Structure Config
    """

    DESCRIPTION = (
        "LM Studio Prompt Driver. LMStudio is available at https://lmstudio.ai "
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    [],
                    {"default": ""},
                ),
                # "prompt_model": ("STRING", {"default": ""}),
                "base_url": ("STRING", {"default": lmstudio_base_url}),
                "port": (
                    "STRING",
                    {"default": lmstudio_port},
                ),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        base_url,
        port,
        temperature,
        seed,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        custom_config = StructureConfig(
            prompt_driver=LMStudioPromptDriver(
                model=prompt_model,
                base_url=f"{base_url}:{port}/v1",
                api_key="lm_studio",
                temperature=temperature,
                tokenizer=SimpleTokenizer(
                    characters_per_token=4,
                    max_input_tokens=1024,
                    max_output_tokens=1024,
                ),
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)


class gtUIOllamaStructureConfig(gtUIBaseConfig):
    """
    The Griptape Ollama Structure Config
    """

    DESCRIPTION = "Ollama Prompt Driver. Use local models with Ollama. Available at https://ollama.com"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    [""],
                    {"default": ""},
                ),
                "base_url": ("STRING", {"default": ollama_base_url}),
                "port": ("STRING", {"default": ollama_port}),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        temperature,
        base_url,
        port,
        seed,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        custom_config = StructureConfig(
            prompt_driver=OllamaPromptDriver(
                model=prompt_model,
                options={"temperature": temperature},
                host=f"{base_url}:{port}",
            ),
            image_generation_driver=image_generation_driver,
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

    DESCRIPTION = "Amazon Bedrock Prompt Driver."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    amazonBedrockPromptModels,
                    {"default": amazonBedrockPromptModels[0]},
                ),
                "image_query_model": (
                    amazonBedrockImageQueryModels,
                    {"default": amazonBedrockImageQueryModels[0]},
                ),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        image_query_model,
        temperature,
        seed,
        image_generation_driver=None,
    ):
        custom_config = AmazonBedrockStructureConfig()
        custom_config.prompt_driver = AmazonBedrockPromptDriver(
            model=prompt_model, temperature=temperature
        )
        custom_config.image_query_driver = AmazonBedrockImageQueryDriver(
            image_query_model_driver=BedrockClaudeImageQueryModelDriver(),
            model=image_query_model,
        )
        if image_generation_driver:
            custom_config.image_generation_driver = image_generation_driver
        return (custom_config,)


google_models = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]


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
        return inputs

    DESCRIPTION = (
        "Google Structure Config. Use Google's models for prompt and image query."
    )

    def create(
        self,
        temperature,
        seed,
        prompt_model,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        # custom_config = GoogleStructureConfig()

        custom_config = GoogleStructureConfig(
            prompt_driver=GooglePromptDriver(
                model=prompt_model, temperature=temperature
            ),
            image_generation_driver=image_generation_driver,
        )

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

    DESCRIPTION = (
        "Anthropic Structure Config. Use Anthropic's models for prompt and image query."
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    anthropicPromptModels,
                    {"default": anthropicPromptModels[0]},
                ),
                "image_query_model": (
                    anthropicImageQueryModels,
                    {"default": anthropicImageQueryModels[0]},
                ),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        image_query_model,
        temperature,
        seed,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        custom_config = AnthropicStructureConfig()
        custom_config.prompt_driver = AnthropicPromptDriver(
            model=prompt_model, temperature=temperature
        )
        custom_config.image_query_driver = AnthropicImageQueryDriver(
            model=image_query_model
        )
        custom_config.image_generation_driver = image_generation_driver

        return (custom_config,)


class gtUIOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "OpenAI Structure Config. Use OpenAI's models for prompt, embedding, image generation, and image query."

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

    def create(
        self,
        prompt_model,
        image_query_model,
        temperature,
        seed,
        image_generation_driver=None,
    ):
        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        prompt_driver = OpenAiChatPromptDriver(
            model=prompt_model,
            api_key=OPENAI_API_KEY,
            temperature=temperature,
            seed=seed,
        )
        embedding_driver = OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY)
        if not image_generation_driver:
            image_generation_driver = OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dalle-e-3",
            )

        image_query_driver = OpenAiImageQueryDriver(
            api_key=OPENAI_API_KEY, model=image_query_model
        )

        # OpenAiStructureConfig()
        custom_config = OpenAiStructureConfig(
            prompt_driver=prompt_driver,
            embedding_driver=embedding_driver,
            image_generation_driver=image_generation_driver,
            image_query_driver=image_query_driver,
        )

        return (custom_config,)
