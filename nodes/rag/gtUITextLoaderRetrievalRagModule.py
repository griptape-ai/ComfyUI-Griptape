from griptape.engines.rag.modules import TextLoaderRetrievalRagModule
from griptape.loaders import CsvLoader, TextLoader, WebLoader

from .gtUIBaseRetrievalRagModule import gtUIBaseRetrievalRagModule

loaders = ["TextLoader", "WebLoader", "CsvLoader"]


class gtUITextLoaderRetrievalRagModule(gtUIBaseRetrievalRagModule):
    """
    Griptape Text Loader Retrieval Rag Module. Used for the Retrieval Stage of the RAG Engine.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "loader": (loaders, {"default": "TextLoader"}),
            }
        )
        inputs["optional"].update(
            {
                "text": (
                    "STRING",
                    {
                        "forceInput": True,
                        "dynamicPrompts": True,
                        "tooltip": "Text to be loaded.",
                    },
                ),
                "url": (
                    "STRING",
                    {"tooltip": "URL to be loaded.", "default": "https://griptape.ai"},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        vector_store_driver = self.get_vector_store_driver(
            kwargs.get("vector_store_driver", None)
        )
        text = kwargs.get("text", None)
        url = kwargs.get("url", "https://griptape.ai")
        loader = kwargs.get("loader", "TextLoader")

        params = {}
        params["query_params"] = self.get_query_params(kwargs)
        params["vector_store_driver"] = vector_store_driver
        if loader == "TextLoader":
            params["loader"] = TextLoader()
            params["source"] = text
        if loader == "WebLoader":
            params["loader"] = WebLoader()
            params["source"] = url
        if loader == "CsvLoader":
            params["loader"] = CsvLoader()
            params["source"] = text

        module = TextLoaderRetrievalRagModule(**params)
        return ([module],)
