from griptape.drivers import LocalVectorStoreDriver

from ..agent.gtComfyAgent import gtComfyAgent as Agent


class gtUIBaseVectorStoreTask:
    def __init__(self):
        self.default_namespace = "default"
        pass

    DESCRIPTION = "Operate on a Vector Store."

    @classmethod
    def INPUT_TYPES(s):
        # inputs = super().INPUT_TYPES()
        inputs = {
            "required": {},
            "optional": {},
        }

        inputs["required"].update(
            {
                "agent": ("AGENT",),
                # "driver": ("VECTOR_STORE_DRIVER", {"default": None}),
            }
        )
        return inputs

    RETURN_TYPES = (
        "AGENT",
        # "DRIVER",
    )
    RETURN_NAMES = (
        "AGENT",
        # "DRIVER",
    )

    FUNCTION = "run"

    CATEGORY = "Griptape/Text"

    def get_vector_store_driver(self, agent, driver):
        if driver:
            vector_store_driver = driver
        elif not driver and agent:
            vector_store_driver = agent.drivers_config.vector_store_driver
        else:
            vector_store_driver = LocalVectorStoreDriver()
        return vector_store_driver

    def run(self, **kwargs):
        agent = kwargs.get("agent", Agent())
        driver = kwargs.get("driver", None)

        vector_store_driver = self.get_vector_store_driver(agent, driver)
        return (
            agent,
            # vector_store_driver,
        )
