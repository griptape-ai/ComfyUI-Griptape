from griptape.chunkers import TextChunker

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseVectorStoreTask import gtUIBaseVectorStoreTask

default_namespace = "default"


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIVectorStoreUpsertTextTask(gtUIBaseVectorStoreTask):
    DESCRIPTION = "Operate on a Vector Store."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "namespace": ("STRING", {"default": default_namespace}),
                "max_chunk_tokens": ("INT", {"default": 100}),
                "input": ("*",),
            }
        )
        return inputs

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

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
        input = kwargs.get("input", None)
        vector_store_driver = self.get_vector_store_driver(agent, driver)
        chunker = TextChunker(max_tokens=max_tokens)
        chunks = chunker.chunk(input)

        vector_store_driver.upsert_text_artifacts({namespace: chunks})

        return (agent,)
