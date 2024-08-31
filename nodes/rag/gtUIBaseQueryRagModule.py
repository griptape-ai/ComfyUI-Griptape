from griptape.engines.rag.modules import BaseQueryRagModule

from .gtUIBaseRagModule import gtUIBaseRagModule


class gtUIBaseQueryRagModule(gtUIBaseRagModule):
    """
    Griptape Base Query Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        return inputs

    def create(self):
        return ([BaseQueryRagModule()],)
