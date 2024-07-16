from griptape.drivers import LocalStructureRunDriver


class gtUILocalStructureRunDriver:
    def __init__(self):
        pass

    DESCRIPTION = "Local Structure Run Driver"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"agent": ("AGENT", {"forceInput": True, "default": None})},
        }

    RETURN_TYPES = ("ARTIFACT",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent Structures"

    def run(
        self,
        agent=None,
    ):
        if agent:
            # Create a local structure function
            driver = LocalStructureRunDriver(structure_factory_fn=lambda: agent)
            return (driver,)
        else:
            return None
