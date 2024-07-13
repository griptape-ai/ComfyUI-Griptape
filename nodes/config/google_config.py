from griptape.config import (
    GoogleStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyImageGenerationDriver,
    GooglePromptDriver,
)

from .base_config import gtUIBaseConfig

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
