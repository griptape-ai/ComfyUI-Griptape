from typing import Any, Tuple

from griptape.engines.rag.modules import TextChunksResponseRagModule

from .gtUIBaseResponseRagModule import gtUIBaseResponseRagModule


class gtUITextChunksResponseRagModule(gtUIBaseResponseRagModule):
    """
    Griptape TextChunks Response Rag Module.
    """

    def __init__(self):
        pass

    def create(self, **kwargs) -> Tuple[Any, ...]:
        module = TextChunksResponseRagModule()
        return ([module],)
