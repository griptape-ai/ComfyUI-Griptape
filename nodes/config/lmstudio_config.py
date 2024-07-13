from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyImageGenerationDriver,
    OpenAiChatPromptDriver,
)

from ..utilities import get_lmstudio_models
from .base_config import gtUIBaseConfig

lmstudio_models = get_lmstudio_models(port="1234")
lmstudio_models.append("")
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
            prompt_driver=OpenAiChatPromptDriver(
                model=prompt_model,
                base_url=f"{base_url}:{port}/v1",
                api_key="lm_studio",
                temperature=temperature,
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
