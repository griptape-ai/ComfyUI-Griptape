from griptape.config import BaseStructureConfig
from griptape.structures import Agent

from ...py.griptape_config import get_config

default_prompt = "{{ input_string }}"


class gtComfyAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Initialize the parent class
        super().__init__(*args, **kwargs)

        # Add any additional initialization here

    def set_default_config(self):
        agent_config = get_config("agent_config")
        if agent_config:
            self.agent.config = BaseStructureConfig.from_dict(agent_config)

    def model_check(self):
        # There are certain models that can't handle Tools well.
        # If this agent is using one of those models AND they have tools supplied, we'll
        # warn the user.
        simple_models = ["llama3", "mistral", "LLama-3"]
        drivers = ["OllamaPromptDriver", "LMStudioPromptDriver"]
        agent_prompt_driver_name = self.agent.config.prompt_driver.__class__.__name__
        model = self.agent.config.prompt_driver.model
        if agent_prompt_driver_name in drivers:
            if model == "":
                return (model, True)
            for simple in simple_models:
                if simple in model:
                    if len(self.agent.tools) > 0:
                        return (model, True)
        return (model, False)


def model_check(agent):
    # There are certain models that can't handle Tools well.
    # If this agent is using one of those models AND they have tools supplied, we'll
    # warn the user.
    simple_models = ["llama3", "mistral", "LLama-3"]
    drivers = ["OllamaPromptDriver", "LMStudioPromptDriver"]
    agent_prompt_driver_name = agent.config.prompt_driver.__class__.__name__
    model = agent.config.prompt_driver.model
    print(f"Model: {model}")
    if agent_prompt_driver_name in drivers:
        if model == "":
            return (model, True)
        for simple in simple_models:
            if simple in model:
                if len(agent.tools) > 0:
                    return (model, True)
    return (model, False)
