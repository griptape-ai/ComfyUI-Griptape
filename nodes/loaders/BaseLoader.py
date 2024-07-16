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

    CATEGORY = "Griptape/Agent Tasks"

    def run(
        self,
    ):
        artifact = BaseArtifact()
        return (artifact,)
