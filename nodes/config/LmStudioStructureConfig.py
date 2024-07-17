from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyImageGenerationDriver,
    OpenAiChatPromptDriver,
)

from ..utilities import get_lmstudio_models
from .BaseConfig import gtUIBaseConfig

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

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", "")
        base_url = kwargs.get("base_url", lmstudio_base_url)
        port = kwargs.get("port", lmstudio_port)
        temperature = kwargs.get("temperature", 0.7)
        image_generation_driver = kwargs.get(
            "image_generation_driver", DummyImageGenerationDriver()
        )
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        stream = kwargs.get("stream", False)
        seed = kwargs.get("seed", 12341)
        custom_config = StructureConfig(
            prompt_driver=OpenAiChatPromptDriver(
                model=prompt_model,
                base_url=f"{base_url}:{port}/v1",
                api_key="lm_studio",
                temperature=temperature,
                max_attempts=max_attempts,
                stream=stream,
                seed=seed,
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
