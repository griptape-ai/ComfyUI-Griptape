from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

lmstudio_port = "1234"
lmstudio_base_url = "http://127.0.0.1"


class gtUILMStudioStructureConfig(gtUIBaseConfig):
    """
    The Griptape LM Studio Structure Config
    """

    DESCRIPTION = (
        "LM Studio Prompt Driver. LMStudio is available at https://lmstudio.ai "
    )

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": ((), {}),
                "base_url": ("STRING", {"default": lmstudio_base_url}),
                "port": (
                    "STRING",
                    {"default": lmstudio_port},
                ),
            },
        )
        inputs["optional"].update(
            {
                "use_native_tools": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "label_on": "True (LLM-native tool calling)",
                        "label_off": "False (Griptape tool calling)",
                    },
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        params = {}
        params["model"] = kwargs.get("model", "")
        port = kwargs.get("port", lmstudio_port)
        base_url = kwargs.get("base_url", lmstudio_base_url)
        params["base_url"] = f"{base_url}:{port}/v1"
        params["temperature"] = kwargs.get("temperature", 0.7)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        params["stream"] = kwargs.get("stream", False)
        params["seed"] = kwargs.get("seed", 12341)
        params["use_native_tools"] = kwargs.get("use_native_tools", False)

        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        custom_config = DriversConfig(
            prompt_driver=OpenAiChatPromptDriver(**params),
        )

        return (custom_config,)
