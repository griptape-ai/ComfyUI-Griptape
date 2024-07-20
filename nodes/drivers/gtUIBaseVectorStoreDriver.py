from griptape.drivers import BaseVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

default_embedding_driver = OpenAiEmbeddingDriver()


class gtUIBaseVectorStoreDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update({"embedding_driver": ("DRIVER", {"default": None})})

        return inputs

    CATEGORY = "Griptape/Drivers/Vector Store"

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)

        params = {}
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver

        driver = BaseVectorStoreDriver(**params)
        return (driver,)
