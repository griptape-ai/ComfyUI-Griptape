from ...py.griptape_config import update_config_with_dict
from .base_agent import BaseAgent


class gtUISetDefaultAgent(BaseAgent):
    DESCRIPTION = "Set the default agent."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]
        del inputs["optional"]["agent"]
        del inputs["optional"]["input_string"]
        del inputs["optional"]["STRING"]
        return inputs

    RETURN_TYPES = ("CONFIG",)
    OUTPUT_NODE = True

    def run(self, config=None):
        update_config_with_dict(config.to_dict())
        return (config,)
