from griptape.drivers.embedding.dummy import DummyEmbeddingDriver
from griptape.drivers.vector.dummy import DummyVectorStoreDriver
from griptape.drivers.vector.local import LocalVectorStoreDriver

from .gtUIBaseRagModule import gtUIBaseRagModule


class gtUIBaseRetrievalRagModule(gtUIBaseRagModule):
    """
    Griptape Base Query Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {
            "vector_store_driver": ("VECTOR_STORE_DRIVER", {"default": None}),
            "namespace": (
                "STRING",
                {"default": "default", "tooltip": "Namespace of the vector store."},
            ),
            # "top_n": (
            #     "INT",
            #     {"default": 20, "tooltip": "Return the # most similar items."},
            # ),
            "count": (
                "INT",
                {"default": 5, "tooltip": "Total number of results to return."},
            ),
        }
        return inputs

    def get_query_params(self, kwargs):
        query_params = {}
        query_params["namespace"] = kwargs.get("namespace", "default")
        # query_params["top_n"] = kwargs.get("top_n", 20)

        if kwargs.get("count") != -1:
            query_params["count"] = kwargs.get("count")
        return query_params

    def get_vector_store_driver(self, vector_store_driver=None):
        if not vector_store_driver or isinstance(
            vector_store_driver, DummyVectorStoreDriver
        ):
            return LocalVectorStoreDriver(embedding_driver=DummyEmbeddingDriver())
        else:
            return vector_store_driver
        return None

    def create(self, **kwargs):
        return ([None],)
