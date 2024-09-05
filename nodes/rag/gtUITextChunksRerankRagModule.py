from griptape.engines.rag.modules import TextChunksRerankRagModule

from .gtUIBaseRerankRagModule import gtUIBaseRerankRagModule


class gtUITextChunksRerankRagModule(gtUIBaseRerankRagModule):
    """
    Griptape Text Loader Retrieval Rag Module. Used for the Retrieval Stage of the RAG Engine.
    """

    def __init__(self):
        pass

    def create(self, **kwargs):
        params = {}
        rerank_driver = kwargs.get("rerank_driver", None)
        if rerank_driver:
            params["rerank_driver"] = rerank_driver

        module = TextChunksRerankRagModule(**params)
        return (module,)
