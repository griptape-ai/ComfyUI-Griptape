from griptape.drivers.structure_run.local import LocalStructureRunDriver


class gtUILocalStructureRunDriver:
    def __init__(self):
        pass

    DESCRIPTION = "Local Structure Run Driver"

    @classmethod
    def INPUT_TYPES(cls):
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
            driver = LocalStructureRunDriver(create_structure=lambda: agent)
            return (driver,)
        else:
            return None
