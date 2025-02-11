from griptape.drivers.structure_run.local import LocalStructureRunDriver
from griptape.tools import StructureRunTool

from ..utilities import to_pascal_case
from .gtUIBaseTool import gtUIBaseTool


class gtUIConvertAgentToTool(gtUIBaseTool):
    def __init__(self):
        pass

    DESCRIPTION = "Convert Agent to Tool"

    @classmethod
    def INPUT_TYPES(cls):
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

    CATEGORY = "Griptape/Agent Tools"

    def run(
        self,
        off_prompt,
        name,
        description,
        agent=None,
    ):
        if agent:
            # Create a local structure function
            driver = LocalStructureRunDriver(create_structure=lambda: agent)
            tool = StructureRunTool(
                name=to_pascal_case(name),
                # name=name,
                description=description,
                structure_run_driver=driver,
                off_prompt=off_prompt,
            )
            return ([tool],)
        else:
            return None
