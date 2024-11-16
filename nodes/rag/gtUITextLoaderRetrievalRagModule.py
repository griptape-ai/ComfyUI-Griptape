import os
import tempfile

import folder_paths
from griptape.engines.rag.modules import TextLoaderRetrievalRagModule
from griptape.loaders import CsvLoader, TextLoader, WebLoader

from .gtUIBaseRetrievalRagModule import gtUIBaseRetrievalRagModule

loaders = ["TextLoader", "CsvLoader", "WebLoader"]
input_source_options = ["Text Input", "File Path"]


class gtUITextLoaderRetrievalRagModule(gtUIBaseRetrievalRagModule):
    """
    Griptape Text Loader Retrieval Rag Module. Used for the Retrieval Stage of the RAG Engine.
    """

    SUPPORTED_FORMATS = (
        ".data",
        ".env",
        ".info",
        ".json",
        ".log",
        ".text",
        ".txt",
        ".yaml",
        ".yml",
        ".csv",
        ".tsv",
        ".md",
    )

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if (
                os.path.isfile(os.path.join(input_dir, f))
                and f.endswith(gtUITextLoaderRetrievalRagModule.SUPPORTED_FORMATS)
            )
        ]
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "loader": (
                    loaders,
                    {
                        "default": "TextInput",
                        "tooltip": "The type of text to load. If TextLoader or CsvLoader, it won't use the Text Input Port.",
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "text": (
                    "STRING",
                    {
                        "forceInput": True,
                        "dynamicPrompts": False,
                        "tooltip": "Text to be loaded.",
                    },
                ),
                "input_source": (
                    input_source_options,
                    {
                        "default": input_source_options[0],
                        "tooltip": "Use a specified file path or the text input port.",
                        "label_on": "Use file path",
                        "label_off": "Use incoming text",
                    },
                ),
                "file_path": (
                    sorted(files),
                    {
                        "text_upload": True,
                        "tooltip": "File to be loaded.",
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
        input_source = kwargs.get("input_source", input_source_options[0])
        params = {}
        params["query_params"] = self.get_query_params(kwargs)
        params["vector_store_driver"] = vector_store_driver
        if loader == "WebLoader":
            params["loader"] = WebLoader()
            params["source"] = url
        else:
            if loader == "CsvLoader":
                params["loader"] = CsvLoader()
            elif loader == "TextLoader":
                params["loader"] = TextLoader()

            # Get the input source
            if input_source == input_source_options[1]:
                params["source"] = folder_paths.get_annotated_filepath(
                    kwargs.get("file_path")
                )
            else:
                # write the text to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(text.encode())
                    temp_filename = temp_file.name
                    temp_file.close()
                params["source"] = temp_filename

        module = TextLoaderRetrievalRagModule(**params)
        return ([module],)
