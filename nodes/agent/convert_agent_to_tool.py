from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient

from ..base_tool import gtUIBaseTool


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


class gtUIConvertAgentToTool(gtUIBaseTool):
    def __init__(self):
        pass

    DESCRIPTION = "Convert Agent to Tool"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "agent": ("AGENT", {"forceInput": True, "default": None}),
                "name": ("STRING", {"default": "Give the agent a name"}),
                "description": (
                    "STRING",
                    {
                        "default": "Describe what the agent should be used for",
                        "multiline": True,
                    },
                ),
            }
        )
        return inputs

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent Convert"

    def run(
        self,
        off_prompt,
        name,
        description,
        agent=None,
    ):
        if agent:
            # Create a local structure function
            driver = LocalStructureRunDriver(structure_factory_fn=lambda: agent)
            tool = StructureRunClient(
                name=name, description=description, driver=driver, off_prompt=off_prompt
            )
            return ([tool],)
        else:
            return None
