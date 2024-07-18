from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()


class gtUILocalVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Local Vector Store Driver"

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)

        params = {}
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = LocalVectorStoreDriver(**params)
        return (driver,)
