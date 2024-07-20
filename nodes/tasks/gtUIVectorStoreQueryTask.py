from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseVectorStoreTask import gtUIBaseVectorStoreTask

default_namespace = "default"


class gtUIVectorStoreQueryTask(gtUIBaseVectorStoreTask):
    DESCRIPTION = "Query a Vector Store."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "namespace": ("STRING", {"default": default_namespace}),
                "count": ("INT", {"default": 1}),
            }
        )
        inputs["optional"].update(
            {
                "input_string": ("STRING", {"forceInput": True}),
                "STRING": ("STRING", {"default": None, "multiline": True}),
            }
        )
        return inputs

    RETURN_TYPES = (
        "AGENT",
        "DRIVER",
        "STRING",
    )
    RETURN_NAMES = (
        "AGENT",
        "DRIVER",
        "OUTPUT",
    )

    FUNCTION = "run"

    CATEGORY = "Griptape/Vector Store"

    def run(self, **kwargs):
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
            agent,
            vector_store_driver,
            value,
        )
