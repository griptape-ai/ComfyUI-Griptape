from griptape.configs import Defaults

from .BaseAgent import BaseAgent
from .gtComfyAgent import gtComfyAgent


class gtUICreateAgentFromConfig(BaseAgent):
    DESCRIPTION = "Create an Agent from a Config"

    def __init__(self):
        self.agent = None

    @classmethod
    def INPUT_TYPES(cls):
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

        Defaults.drivers_config = config

        if config:
            # create_dict["prompt_driver"] = Defaults.drivers_config.prompt_driver
            create_dict["drivers_config"] = Defaults.drivers_config
        # Now create the agent
        self.agent = gtComfyAgent(**create_dict)

        return (self.agent,)
