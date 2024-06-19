from griptape.drivers import OpenAiAudioTranscriptionDriver

from .base_task import gtUIBaseTask


class gtUIBaseAudioTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "audio": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
            },
        )
        inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["input_string"]
        del inputs["optional"]["agent"]
        del inputs["required"]["STRING"]
        return inputs

    CATEGORY = "Griptape/Audio"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    def run(self, audio, driver=None):
        if not driver:
            driver = OpenAiAudioTranscriptionDriver(model="whisper-1")
        output = "Output"
        return (output,)
