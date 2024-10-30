import os

from griptape.drivers import (
    BaseVectorStoreDriver,
    DummyEmbeddingDriver,
    OpenAiEmbeddingDriver,
)

from .gtUIBaseDriver import gtUIBaseDriver

# default_embedding_driver = OpenAiEmbeddingDriver()


class gtUIBaseVectorStoreDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_driver": (
                    "EMBEDDING_DRIVER",
                    {
                        "default": None,
                        "tooltip": "Select an embedding driver or leave as default.",
                    },
                )
            }
        )

        return inputs

    CATEGORY = "Griptape/Agent Drivers/Vector Store"
    RETURN_TYPES = ("VECTOR_STORE_DRIVER",)

    def get_default_embedding_driver(self):
        if os.getenv("OPENAI_API_KEY"):
            return OpenAiEmbeddingDriver()
        else:
            return DummyEmbeddingDriver()

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)

        params = {}
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        driver = BaseVectorStoreDriver(**params)
        return (driver,)
