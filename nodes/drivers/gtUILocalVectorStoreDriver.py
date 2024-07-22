from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()
default_filename = "griptape_local_vector_file.txt"


class gtUILocalVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Local Vector Store Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "persist_file": ("BOOLEAN", {"default": False}),
                "persist_filename": (
                    "STRING",
                    {"default": default_filename, "visible": "persist_file"},
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        persist_file = kwargs.get("persist_file", False)
        persist_filename = kwargs.get("persist_filename", default_filename)

        params = {}
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver

        if persist_file and persist_filename:
            params["persist_file"] = persist_filename
        driver = LocalVectorStoreDriver(**params)
        return (driver,)
