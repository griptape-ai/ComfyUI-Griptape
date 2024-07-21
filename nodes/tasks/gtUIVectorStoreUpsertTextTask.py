from griptape.artifacts import TextArtifact
from griptape.chunkers import TextChunker
from griptape.loaders import TextLoader

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseVectorStoreTask import gtUIBaseVectorStoreTask

default_namespace = "default"


class gtUIVectorStoreUpsertTextTask(gtUIBaseVectorStoreTask):
    DESCRIPTION = "Operate on a Vector Store."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "namespace": ("STRING", {"default": default_namespace}),
                "max_chunk_tokens": ("INT", {"default": 100}),
                "input": ("*",),
            }
        )
        return inputs

    RETURN_TYPES = (
        "AGENT",
        # "VECTOR_STORE_DRIVER",
    )
    RETURN_NAMES = (
        "AGENT",
        # "DRIVER",
    )

    FUNCTION = "run"

    def run(self, **kwargs):
        agent = kwargs.get("agent", Agent())
        driver = kwargs.get("driver", None)
        max_tokens = kwargs.get("max_chunk_tokens", 100)
        namespace = kwargs.get("namespace", default_namespace)
        # get all the inputs that start with "input_"
        inputs = [value for key, value in kwargs.items() if key.startswith("input")]

        vector_store_driver = self.get_vector_store_driver(agent, driver)
        embedding_driver = agent.config.embedding_driver
        # generate artifacts for each input
        artifacts = []
        for input in inputs:
            if isinstance(input, str):
                # Use a TextLoader
                artifacts = TextLoader(
                    chunker=TextChunker(max_tokens=max_tokens),
                    embedding_driver=embedding_driver,
                ).load(input)
                # artifacts.append(TextArtifact(input))
            elif isinstance(input, TextArtifact):
                artifacts.append(input)

        # Upsert Artifacts into the Vector Store Driver
        [
            vector_store_driver.upsert_text_artifact(a, namespace=namespace)
            for a in artifacts
        ]

        return (
            agent,
            # vector_store_driver,
        )
