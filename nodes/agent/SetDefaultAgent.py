from ...py.griptape_config import update_config_with_dict
from .BaseAgent import BaseAgent


class gtUISetDefaultAgent(BaseAgent):
    DESCRIPTION = "Set the default agent."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]
        del inputs["optional"]["input_string"]
        del inputs["optional"]["STRING"]
        return inputs

    RETURN_TYPES = ("CONFIG",)
    OUTPUT_NODE = True

    def run(self, **kwargs):
        config = kwargs.get("config", None)
        agent = kwargs.get("agent", None)
        if config:
            update_config_with_dict(config.to_dict())
        if agent:
            config = agent.drivers_config
            update_config_with_dict(config.to_dict())
        return (config,)
