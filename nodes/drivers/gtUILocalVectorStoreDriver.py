from griptape.drivers import (
    LocalVectorStoreDriver,
)

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_filename = "griptape_local_vector_file.txt"


class gtUILocalVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Local Vector Store Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "persist_file": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Enable or disable persistence to a file.",
                        "label_on": "True (Save data to file)",
                        "label_off": "False (Keep data in memory)",
                    },
                ),
                "persist_filename": (
                    "STRING",
                    {
                        "default": default_filename,
                        "visible": "persist_file",
                        "tooltip": "Filename for persisting data.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        persist_file = kwargs.get("persist_file", False)
        persist_filename = kwargs.get("persist_filename", default_filename)

        params = {}
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        if persist_file and persist_filename:
            params["persist_file"] = persist_filename

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = LocalVectorStoreDriver(**params)
        return (driver,)
