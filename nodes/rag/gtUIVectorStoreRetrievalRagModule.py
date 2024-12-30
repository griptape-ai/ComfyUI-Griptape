from typing import Any, Tuple

from griptape.engines.rag.modules import VectorStoreRetrievalRagModule

from .gtUIBaseRetrievalRagModule import gtUIBaseRetrievalRagModule


class gtUIVectorStoreRetrievalRagModule(gtUIBaseRetrievalRagModule):
    """
    Griptape Text Loader Retrieval Rag Module. Used for the Retrieval Stage of the RAG Engine.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                # "namespace": (
                #     "STRING",
                #     {"default": "default", "tooltip": "Namespace of the vector store."},
                # ),
                # "query_params": (
                #     "STRING",
                #     {
                #         "dynamicPrompts": True,
                #         "tooltip": "Dict of any query parameters.",
                #         "multiline": True,
                #         "default": '{"top_n": 20}',
                #     },
                # ),
            }
        )
        return inputs

    def create(self, **kwargs) -> Tuple[Any, ...]:
        vector_store_driver = self.get_vector_store_driver(
            kwargs.get("vector_store_driver", None)
        )
        # namespace = kwargs.get("namespace", "default")
        # query_params = kwargs.get("query_params", {})

        # query_params_dict = self.ensure_dict(query_params)
        # query_params_dict["namespace"] = namespace

        params = {}
        params["query_params"] = self.get_query_params(kwargs)

        params["vector_store_driver"] = vector_store_driver
        # params["query_params"] = query_params_dict
        module = VectorStoreRetrievalRagModule(**params)
        return ([module],)
