from griptape.config import BaseStructureConfig
from griptape.structures import Agent

from ...py.griptape_config import get_config

default_prompt = "{{ input_string }}"


class gtComfyAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Check if 'config' is in kwargs
        if "config" not in kwargs:
            # Get the default config
            agent_config = get_config("agent_config")
            if agent_config:
                config = BaseStructureConfig.from_dict(agent_config)
                kwargs["config"] = config

        # Initialize the parent class
        super().__init__(*args, **kwargs)

        # # Add any additional initialization here
        # if "config" not in kwargs:
        #     self.set_default_config()

    def set_default_config(self):
        agent_config = get_config("agent_config")
        if agent_config:
            config = BaseStructureConfig.from_dict(agent_config)
            new_agent = self.update_config(config)
            self = new_agent

    def model_check(self):
        # There are certain models that can't handle Tools well.
        # If this agent is using one of those models AND they have tools supplied, we'll
        # warn the user.
        simple_models = ["llama3", "mistral", "LLama-3"]
        drivers = ["OllamaPromptDriver", "LMStudioPromptDriver"]
        agent_prompt_driver_name = self.config.prompt_driver.__class__.__name__
        print(agent_prompt_driver_name)

        model = self.config.prompt_driver.model
        if agent_prompt_driver_name in drivers:
            if model == "":
                return (model, True)
            for simple in simple_models:
                if simple in model:
                    if len(self.tools) > 0:
                        return (model, True)
        return (model, False)

    def model_response(self, model):
        if model == "":
            return "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent."
        else:
            return f"This Agent Configuration Model: **{ self.config.prompt_driver.model }** may run into issues using tools.\n\nPlease consider using a different configuration, a different model, or removing tools from the agent and use the **Griptape Run: Tool Task** node for specific tool use."

    def update_agent(
        self,
        config=None,
        tools=None,
        rulesets=None,
        conversation_memory=None,
        meta_memory=None,
        task_memory=None,
    ):
        update_dict = {
            "config": config or self.config,
            "tools": tools or self.tools,
            "rulesets": rulesets or self.rulesets,
            "conversation_memory": conversation_memory or self.conversation_memory,
            "meta_memory": meta_memory or self.meta_memory,
            "task_memory": task_memory or self.task_memory,
        }
        new_agent = gtComfyAgent(**update_dict)
        return new_agent

    def update_config(self, config):
        tools = self.tools
        rulesets = self.rulesets
        conversation_memory = self.conversation_memory
        new_agent = gtComfyAgent(
            config=config,
            tools=tools,
            rulesets=rulesets,
            conversation_memory=conversation_memory,
        )

        return new_agent


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
