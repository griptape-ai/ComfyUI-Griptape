from dotenv import load_dotenv
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
from ..drivers.gtUIOpenAiCompatibleChatPromptDriver import (
    gtUIOpenAiCompatibleChatPromptDriver,
)
from ..drivers.gtUIOpenAiCompatibleEmbeddingDriver import (
    gtUIOpenAiCompatibleEmbeddingDriver,
)
from ..drivers.gtUIOpenAiCompatibleImageGenerationDriver import (
    gtUIOpenAiCompatibleImageGenerationDriver,
)
from ..drivers.gtUIOpenAiTextToSpeechDriver import gtUIOpenAiTextToSpeechDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

load_dotenv()

DEFAULT_API_KEY = "OPENAI_API_KEY"

# Define the list of drivers
drivers = [
    ("prompt", gtUIOpenAiCompatibleChatPromptDriver),
    ("image_generation", gtUIOpenAiCompatibleImageGenerationDriver),
    ("embedding", gtUIOpenAiCompatibleEmbeddingDriver),
    ("text_to_speech", gtUIOpenAiTextToSpeechDriver),
    ("audio_transcription", gtUIOpenAiAudioTranscriptionDriver),
]


class gtUIOpenAiCompatibleDriversConfig(gtUIBaseDriversConfig):
    """
    Create an OpenAI Compatible Structure Config
    """

    DESCRIPTION = "OpenAI Compatible Structure Config."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(self, **kwargs):
        self.run_envs(kwargs)
        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIOpenAiCompatibleChatPromptDriver()
        embedding_driver_builder = gtUIOpenAiCompatibleEmbeddingDriver()
        audio_transcription_driver_builder = gtUIOpenAiAudioTranscriptionDriver()
        image_generation_driver_builder = gtUIOpenAiCompatibleEmbeddingDriver()
        text_to_speech_driver_builder = gtUIOpenAiTextToSpeechDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)
        image_generation_driver_params = image_generation_driver_builder.build_params(
            **kwargs
        )
        text_to_speech_driver_params = text_to_speech_driver_builder.build_params(
            **kwargs
        )
        audio_transcription_driver_params = (
            audio_transcription_driver_builder.build_params(**kwargs)
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
            raise Exception(f"Error creating OpenAiCompatibleDriversConfig: {e}")
        return (custom_config,)
