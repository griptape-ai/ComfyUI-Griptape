from griptape.config import (
    StructureConfig,
)
from griptape.drivers import (
    OpenAiAudioTranscriptionDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiImageQueryDriver,
    OpenAiTextToSpeechDriver,
)

default_chat_prompt_driver = OpenAiChatPromptDriver(model="gpt-4o")
default_image_generation_driver = OpenAiImageGenerationDriver(model="dall-e-3")
default_image_query_driver = OpenAiImageQueryDriver(model="gpt-4o")
default_embedding_driver = OpenAiEmbeddingDriver()
default_text_to_speech_driver = OpenAiTextToSpeechDriver(model="tts-1", voice="alloy")
default_audio_transcription_driver = OpenAiAudioTranscriptionDriver(model="whisper-1")


class gtUIStructureConfig:
    """
    Griptape Structure Config
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "prompt_driver": ("DRIVER", {}),
                "image_generation_driver": ("DRIVER", {}),
                "image_query_driver": ("DRIVER", {}),
                "embedding_driver": ("DRIVER", {}),
                "vector_store_driver": ("DRIVER", {}),
                "text_to_speech_driver": ("DRIVER", {}),
                "audio_transcription_driver": ("DRIVER", {}),
            },
        }

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Configs"

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver", default_chat_prompt_driver)
        image_generation_driver = kwargs.get(
            "image_generation_driver", default_image_generation_driver
        )
        image_query_driver = kwargs.get(
            "image_query_driver", default_image_query_driver
        )
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        vector_store_driver = kwargs.get("vector_store_driver", None)
        text_to_speech_driver = kwargs.get(
            "text_to_speech_driver", default_text_to_speech_driver
        )
        audio_transcription_driver = kwargs.get(
            "audio_transcription_driver", default_audio_transcription_driver
        )

        drivers = {}

        if prompt_driver:
            drivers["prompt_driver"] = prompt_driver
        if image_generation_driver:
            drivers["image_generation_driver"] = image_generation_driver
        if image_query_driver:
            drivers["image_query_driver"] = image_query_driver
        if embedding_driver:
            drivers["embedding_driver"] = embedding_driver
        if vector_store_driver:
            drivers["vector_store_driver"] = vector_store_driver
        if text_to_speech_driver:
            drivers["text_to_speech_driver"] = text_to_speech_driver
        if audio_transcription_driver:
            drivers["audio_transcription_driver"] = audio_transcription_driver

        return (StructureConfig(**drivers),)
