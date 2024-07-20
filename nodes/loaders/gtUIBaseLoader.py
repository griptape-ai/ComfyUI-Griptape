from griptape.artifacts import BaseArtifact


class gtUIBaseLoader:
    def __init__(self):
        pass

    DESCRIPTION = "Loader"

    @classmethod
    def INPUT_TYPES(s):
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
        artifact = BaseArtifact()
        return (artifact,)
