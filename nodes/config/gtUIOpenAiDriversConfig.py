from griptape.configs import Defaults
from griptape.configs.drivers import (
    OpenAiDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    LocalVectorStoreDriver,
    OpenAiAudioTranscriptionDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiTextToSpeechDriver,
)

# Get all the drivers
from ..drivers.gtUIOpenAiAudioTranscriptionDriver import (
    gtUIOpenAiAudioTranscriptionDriver,
)
from ..drivers.gtUIOpenAiChatPromptDriver import gtUIOpenAiChatPromptDriver
from ..drivers.gtUIOpenAiEmbeddingDriver import gtUIOpenAiEmbeddingDriver
from ..drivers.gtUIOpenAiImageGenerationDriver import gtUIOpenAiImageGenerationDriver
from ..drivers.gtUIOpenAiTextToSpeechDriver import gtUIOpenAiTextToSpeechDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

default_prompt_model = "gpt-4o"
default_image_query_model = "gpt-4o"
DEFAULT_API_KEY = "OPENAI_API_KEY"

# Define the list of drivers
drivers = [
    ("prompt", gtUIOpenAiChatPromptDriver),
    ("image_generation", gtUIOpenAiImageGenerationDriver),
    ("embedding", gtUIOpenAiEmbeddingDriver),
    ("text_to_speech", gtUIOpenAiTextToSpeechDriver),
    ("audio_transcription", gtUIOpenAiAudioTranscriptionDriver),
]


class gtUIOpenAiDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "OpenAI Drivers Config. Use OpenAI's models for prompt, embedding, image generation, and image query."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    RETURN_TYPES = ("CONFIG",)

    def create(
        self,
        **kwargs,
    ):
        self.run_envs(kwargs)

        drivers_config_params = {}
        # Create instances of the driver classes
        prompt_driver_builder = gtUIOpenAiChatPromptDriver()
        embedding_driver_builder = gtUIOpenAiEmbeddingDriver()
        audio_transcription_driver_builder = gtUIOpenAiAudioTranscriptionDriver()
        image_generation_driver_builder = gtUIOpenAiImageGenerationDriver()
        text_to_speech_driver_builder = gtUIOpenAiTextToSpeechDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)
        audio_transcription_driver_params = (
            audio_transcription_driver_builder.build_params(**kwargs)
        )
        image_generation_driver_params = image_generation_driver_builder.build_params(
            **kwargs
        )
        text_to_speech_driver_params = text_to_speech_driver_builder.build_params(
            **kwargs
        )
        # Create Driver Configs
        drivers_config_params["prompt_driver"] = OpenAiChatPromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = OpenAiEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["audio_transcription_driver"] = (
            OpenAiAudioTranscriptionDriver(**audio_transcription_driver_params)
        )
        drivers_config_params["image_generation_driver"] = OpenAiImageGenerationDriver(
            **image_generation_driver_params
        )
        drivers_config_params["text_to_speech_driver"] = OpenAiTextToSpeechDriver(
            **text_to_speech_driver_params
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=OpenAiEmbeddingDriver(**embedding_driver_params)
        )
        try:
            Defaults.drivers_config = OpenAiDriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise Exception(f"Error creating OpenAiStructureConfig: {e}")

        return (custom_config,)
