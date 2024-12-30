from griptape.configs.drivers import (
    DriversConfig,
)
from griptape.drivers import (
    DummyAudioTranscriptionDriver,
    DummyEmbeddingDriver,
    DummyImageGenerationDriver,
    DummyPromptDriver,
    DummyTextToSpeechDriver,
)

from ..gtUIBase import gtUIBase


class gtUIStructureConfig(gtUIBase):
    """
    Griptape Structure Config
    """

    def __init__(self):
        self.default_chat_prompt_driver = DummyPromptDriver()
        self.default_image_generation_driver = DummyImageGenerationDriver()
        self.default_embedding_driver = DummyEmbeddingDriver()
        self.default_text_to_speech_driver = DummyTextToSpeechDriver()
        self.default_audio_transcription_driver = DummyAudioTranscriptionDriver()

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "prompt_driver": ("PROMPT_DRIVER", {}),
                "image_generation_driver": ("DRIVER", {}),
                "embedding_driver": ("EMBEDDING_DRIVER", {}),
                "vector_store_driver": ("VECTOR_STORE_DRIVER", {}),
                "text_to_speech_driver": ("TEXT_TO_SPEECH_DRIVER", {}),
                "audio_transcription_driver": ("AUDIO_TRANSCRIPTION_DRIVER", {}),
            },
        )
        return inputs

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Configs"

    def create(self, **kwargs):
        self.run_envs(kwargs)

        prompt_driver = kwargs.get("prompt_driver", self.default_chat_prompt_driver)
        image_generation_driver = kwargs.get(
            "image_generation_driver", self.default_image_generation_driver
        )
        embedding_driver = kwargs.get("embedding_driver", self.default_embedding_driver)
        vector_store_driver = kwargs.get("vector_store_driver", None)
        text_to_speech_driver = kwargs.get(
            "text_to_speech_driver", self.default_text_to_speech_driver
        )
        audio_transcription_driver = kwargs.get(
            "audio_transcription_driver", self.default_audio_transcription_driver
        )

        drivers = {}

        if prompt_driver:
            drivers["prompt_driver"] = prompt_driver
        if image_generation_driver:
            drivers["image_generation_driver"] = image_generation_driver
        if embedding_driver:
            drivers["embedding_driver"] = embedding_driver
        if vector_store_driver:
            drivers["vector_store_driver"] = vector_store_driver
        if text_to_speech_driver:
            drivers["text_to_speech_driver"] = text_to_speech_driver
        if audio_transcription_driver:
            drivers["audio_transcription_driver"] = audio_transcription_driver

        return (DriversConfig(**drivers),)
