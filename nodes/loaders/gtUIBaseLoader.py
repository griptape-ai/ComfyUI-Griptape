from griptape.artifacts import TextArtifact


class gtUIBaseLoader:
    def __init__(self):
        pass

    DESCRIPTION = "Loader"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("ARTIFACT",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Loaders"

    def run(self, **kwargs):
        artifact = TextArtifact(value="")
        return (artifact,)
