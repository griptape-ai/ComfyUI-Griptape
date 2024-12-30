from typing import Any, Tuple

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseVectorStoreTask import gtUIBaseVectorStoreTask

default_namespace = "default"


class gtUIVectorStoreQueryTask(gtUIBaseVectorStoreTask):
    DESCRIPTION = "Query a Vector Store."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "namespace": ("STRING", {"default": default_namespace}),
                "count": ("INT", {"default": 1}),
                "STRING": (
                    "STRING",
                    {
                        "default": "",
                        "description": "The prompt to query the vector store with.",
                        "multiline": True,
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "input_string": ("STRING", {"forceInput": True}),
            }
        )
        return inputs

    RETURN_TYPES = (
        "STRING",
        "AGENT",
        # "VECTOR_STORE_DRIVER",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
        # "DRIVER",
    )

    FUNCTION = "run"

    CATEGORY = "Griptape/Text"

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("STRING", "")
        input_string = kwargs.get("input_string", "")
        agent = kwargs.get("agent", Agent())
        driver = kwargs.get("driver", None)
        count = kwargs.get("count", 1)
        namespace = kwargs.get("namespace", default_namespace)
        # get all the inputs that start with "input_"
        vector_store_driver = self.get_vector_store_driver(agent, driver)
        prompt_text = str(STRING + "\n\n" + input_string).strip()

        results = vector_store_driver.query(
            prompt_text, count=count, namespace=namespace
        )
        values = [r.to_artifact().value for r in results]
        value = "\n\n".join(values)
        return (
            value,
            agent,
            # vector_store_driver,
        )
