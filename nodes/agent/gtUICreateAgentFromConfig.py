from .BaseAgent import BaseAgent
from .gtComfyAgent import gtComfyAgent


class gtUICreateAgentFromConfig(BaseAgent):
    DESCRIPTION = "Create an Agent from a Config"

    def __init__(self):
        self.agent = None

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]
        del inputs["optional"]["STRING"]
        del inputs["optional"]["agent"]
        del inputs["optional"]["input_string"]
        return inputs

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("AGENT",)

    def run(self, **kwargs):
        config = kwargs.get("config", None)

        create_dict = {}

        if config:
            create_dict["config"] = config

        # Now create the agent
        self.agent = gtComfyAgent(**create_dict)

        return (self.agent,)
