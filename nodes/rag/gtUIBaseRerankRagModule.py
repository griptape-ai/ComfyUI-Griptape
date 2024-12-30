from .gtUIBaseRagModule import gtUIBaseRagModule


class gtUIBaseRerankRagModule(gtUIBaseRagModule):
    """
    Griptape Base Rerank Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "rerank_driver": ("RERANK_DRIVER", {"default": None}),
            }
        )
        return inputs

    RETURN_TYPES = ("MODULE",)
    RETURN_NAMES = ("MODULE",)

    def create(self, **kwargs):
        return (None,)
