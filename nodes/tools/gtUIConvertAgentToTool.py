from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient

from .gtUIBaseTool import gtUIBaseTool


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

    CATEGORY = "Griptape/Agent"

    def safe_name(self, name):
        # Convert the name to a safe name. Name can't have any spaces or underscores
        safe_name = name.replace(" ", "-").replace("_", "-").lower()
        return safe_name

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
                name=self.safe_name(name),
                # name=name,
                description=description,
                driver=driver,
                off_prompt=off_prompt,
            )
            return ([tool],)
        else:
            return None
