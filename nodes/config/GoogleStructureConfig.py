from griptape.config import (
    GoogleStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyImageGenerationDriver,
    GooglePromptDriver,
)

from .BaseConfig import gtUIBaseConfig

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
        **kwargs,
    ):
        temperature = kwargs.get("temperature", 0.7)
        prompt_model = kwargs.get("prompt_model", google_models[0])
        image_generation_driver = kwargs.get(
            "image_generation_driver", DummyImageGenerationDriver()
        )
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        stream = kwargs.get("stream", False)
        # custom_config = GoogleStructureConfig()

        custom_config = GoogleStructureConfig(
            prompt_driver=GooglePromptDriver(
                model=prompt_model,
                temperature=temperature,
                max_attempts=max_attempts,
                stream=stream,
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
