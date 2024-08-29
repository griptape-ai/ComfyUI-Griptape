from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

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
    def INPUT_TYPES(s):
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
                "use_native_tools": ("BOOLEAN", {"default": False}),
            }
        )
        return inputs

    def create(self, **kwargs):
        model = kwargs.get("model", "")
        base_url = kwargs.get("base_url", lmstudio_base_url)
        port = kwargs.get("port", lmstudio_port)
        temperature = kwargs.get("temperature", 0.7)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        stream = kwargs.get("stream", False)
        seed = kwargs.get("seed", 12341)
        use_native_tools = kwargs.get("use_native_tools", False)
        custom_config = DriversConfig(
            prompt_driver=OpenAiChatPromptDriver(
                model=model,
                base_url=f"{base_url}:{port}/v1",
                api_key="lm_studio",
                temperature=temperature,
                max_attempts=max_attempts,
                stream=stream,
                seed=seed,
                use_native_tools=use_native_tools,
            ),
        )

        return (custom_config,)
