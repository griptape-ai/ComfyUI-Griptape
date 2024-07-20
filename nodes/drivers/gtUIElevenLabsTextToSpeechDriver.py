from griptape.drivers import ElevenLabsTextToSpeechDriver

from .gtUIBaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

premade_voices = []

DEFAULT_API_KEY_ENV_VAR = "ELEVEN_LABS_API_KEY"


class gtUIElevenLabsTextToSpeechDriver(gtUIBaseTextToSpeechDriver):
    DESCRIPTION = "Griptape ElevenLabs to Speech Driver: https://elevenlabs.io/apps/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": ("STRING", {"default": "eleven_multilingual_v2"}),
                "voice": ("STRING", {"default": "Matilda"}),
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )
        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR))

        model = kwargs.get("model", "eleven_multilingual_v2")
        voice = kwargs.get("voice", "Matilda")
        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if voice:
            params["voice"] = voice

        driver = ElevenLabsTextToSpeechDriver(**params)
        return (driver,)
