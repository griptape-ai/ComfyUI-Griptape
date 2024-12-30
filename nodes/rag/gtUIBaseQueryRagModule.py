from .gtUIBaseRagModule import gtUIBaseRagModule


class gtUIBaseQueryRagModule(gtUIBaseRagModule):
    """
    Griptape Base Query Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        return inputs

    def create(self, **kwargs):
        return ([None],)
