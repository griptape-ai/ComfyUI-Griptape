class gtUIExpandConfig:
    DESCRIPTION = (
        "Expand the components of a Griptape Config into their individual drivers"
    )

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "PROMPT_DRIVER",
        "DRIVER",  # Image Generation Driver
        "EMBEDDING_DRIVER",
        "VECTOR_STORE_DRIVER",
        "TEXT_TO_SPEECH_DRIVER",
        "AUDIO_TRANSCRIPTION_DRIVER",
    )
    RETURN_NAMES = (
        "PROMPT_DRIVER",
        "IMAGE_GENERATION_DRIVER",
        "EMBEDDING_DRIVER",
        "VECTOR_STORE_DRIVER",
        "TEXT_TO_SPEECH_DRIVER",
        "AUDIO_TRANSCRIPTION_DRIVER",
    )

    FUNCTION = "expand"

    CATEGORY = "Griptape/Agent Configs"
    OUTPUT_NODE = True

    def expand(self, **kwargs):
        config = kwargs.get("config", None)

        if config is not None:
            prompt_driver = config.prompt_driver
            image_generation_driver = config.image_generation_driver
            embedding_driver = config.embedding_driver
            vector_store_driver = config.vector_store_driver
            text_to_speech_driver = config.text_to_speech_driver
            audio_transcription_driver = config.audio_transcription_driver
        else:
            raise ValueError("No config provided")
        return (
            prompt_driver,
            image_generation_driver,
            embedding_driver,
            vector_store_driver,
            text_to_speech_driver,
            audio_transcription_driver,
        )
