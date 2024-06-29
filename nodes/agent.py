from ..py.griptape_config import update_config_with_dict
from .base_agent import BaseAgent

default_prompt = "{{ input_string }}"


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


class RunAgent(BaseAgent):
    DESCRIPTION = "Run a simple Griptape Agent"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["config"]
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]

        return inputs

    def run(
        self,
        STRING,
        agent=None,
        input_string=None,
    ):
        if agent:
            self.agent = agent
        else:
            # make sure we update the config if it's changed
            self.set_default_config()

        # Warn for models
        model, simple_model = self.model_check()
        if simple_model:
            return (self.model_response(model), self.agent)

        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string

        result = self.agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            self.agent,
        )


class CreateAgent(BaseAgent): ...


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
        if config:
            self.agent.config = config

        update_config_with_dict(self.agent.config.to_dict())
        return (config,)


class ExpandAgent:
    DESCRIPTION = "Expand the components of a Griptape Agent."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "AGENT",
        "CONFIG",
        "RULESET",
        "TOOL_LIST",
        "MEMORY",
    )
    RETURN_NAMES = (
        "AGENT",
        "CONFIG",
        "RULESETS",
        "TOOLS",
        "MEMORY",
    )

    FUNCTION = "expand"

    CATEGORY = "Griptape/Agent"
    OUTPUT_NODE = True

    def expand(self, agent):
        rulesets = agent.rulesets
        tools = agent.tools
        conversation_memory = agent.conversation_memory
        config = agent.config
        # Run the agent
        return (
            agent,
            config,
            rulesets,
            tools,
            conversation_memory,
        )
