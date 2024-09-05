from griptape.engines.rag.modules import TextChunksResponseRagModule

from .gtUIBaseReponseRagModule import gtUIBaseResponseRagModule


class gtUITextChunksResponseRagModule(gtUIBaseResponseRagModule):
    """
    Griptape TextChunks Response Rag Module.
    """

    def __init__(self):
        pass

    def create(self, **kwargs):
        module = TextChunksResponseRagModule()
        return ([module],)
