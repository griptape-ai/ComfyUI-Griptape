from griptape.artifacts import TextArtifact

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
                "input_1": ("*",),
            }
        )
        return inputs

    RETURN_TYPES = (
        "AGENT",
        "DRIVER",
    )
    RETURN_NAMES = (
        "AGENT",
        "DRIVER",
    )

    FUNCTION = "run"

    def run(self, **kwargs):
        agent = kwargs.get("agent", Agent())
        driver = kwargs.get("driver", None)
        namespace = kwargs.get("namespace", default_namespace)
        # get all the inputs that start with "input_"
        inputs = [value for key, value in kwargs.items() if key.startswith("input_")]

        vector_store_driver = self.get_vector_store_driver(agent, driver)

        # generate artifacts for each input
        artifacts = []
        for input in inputs:
            if isinstance(input, str):
                # split the inputs by newlines
                for line in input.split("\n"):
                    artifacts.append(TextArtifact(line))
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
            vector_store_driver,
        )
