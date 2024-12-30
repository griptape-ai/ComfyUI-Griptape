from griptape.drivers import ElevenLabsTextToSpeechDriver

from .gtUIBaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

premade_voices = []

DEFAULT_API_KEY_ENV_VAR = "ELEVEN_LABS_API_KEY"


class gtUIElevenLabsTextToSpeechDriver(gtUIBaseTextToSpeechDriver):
    DESCRIPTION = "Griptape ElevenLabs to Speech Driver: https://elevenlabs.io/apps/"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": (
                    "STRING",
                    {
                        "default": "eleven_multilingual_v2",
                        "tooltip": "The model to use for text-to-speech.",
                    },
                ),
                "voice": (
                    "STRING",
                    {
                        "default": "Matilda",
                        "tooltip": "The voice to use for text-to-speech.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "The environment variable name for the API key. Do not use your actual API key here.",
                    },
                ),
            }
        )
        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        params = {}
        params["api_key"] = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        params["model"] = kwargs.get("model", "eleven_multilingual_v2")
        params["voice"] = kwargs.get("voice", "Matilda")
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        driver = ElevenLabsTextToSpeechDriver(**params)
        return (driver,)
