from ...py.griptape_config import get_config
from .agent import gtComfyAgent

default_prompt = "{{ input_string }}"


def get_default_config():
    return get_config("agent_config")


class BaseAgent:
    """
    Create a Griptape Agent
    """

    def __init__(self):
        self.default_prompt = default_prompt
        self.agent = gtComfyAgent()
        self.agent.set_default_config()

        # config = get_default_config()
        # if config:
        #     self.agent.config = BaseStructureConfig.from_dict(config)
        # pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                    },
                ),
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                    },
                ),
                "tools": ("TOOL_LIST", {"forceInput": True, "INPUT_IS_LIST": True}),
                "rulesets": ("RULESET", {"forceInput": True}),
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "AGENT",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
    )
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent"

    # def set_default_config(self):
    #     agent_config = get_config("agent_config")
    #     if agent_config:
    #         self.agent.config = BaseStructureConfig.from_dict(agent_config)

    # def model_check(self):
    #     # There are certain models that can't handle Tools well.
    #     # If this agent is using one of those models AND they have tools supplied, we'll
    #     # warn the user.
    #     simple_models = ["llama3", "mistral", "LLama-3"]
    #     drivers = ["OllamaPromptDriver", "LMStudioPromptDriver"]
    #     agent_prompt_driver_name = self.agent.config.prompt_driver.__class__.__name__
    #     model = self.agent.config.prompt_driver.model
    #     if agent_prompt_driver_name in drivers:
    #         if model == "":
    #             return (model, True)
    #         for simple in simple_models:
    #             if simple in model:
    #                 if len(self.agent.tools) > 0:
    #                     return (model, True)
    #     return (model, False)

    # def model_response(self, model):
    #     if model == "":
    #         return "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent."
    #     else:
    #         return f"This Agent Configuration Model: **{ self.agent.config.prompt_driver.model }** may run into issues using tools.\n\nPlease consider using a different configuration, a different model, or removing tools from the agent and use the **Griptape Run: Tool Task** node for specific tool use."

    def run(
        self,
        STRING,
        config=None,
        tools=[],
        rulesets=[],
        agent=None,
        input_string=None,
    ):
        if agent:
            self.agent = agent

        # Replace bits of the agent based off the inputs
        if config:
            self.agent.config = config
        else:
            self.agent.set_default_config()

        if len(tools) > 0:
            self.agent.tools = tools
        if len(rulesets) > 0:
            self.agent.rulesets = rulesets

        # Warn for models
        model, simple_model = self.agent.model_check()
        if simple_model:
            return (self.agent.model_response(model), self.agent)

        # Check for inputs. If none, then just create the agent
        if not input_string and STRING == "":
            output_string = "Agent created."
        else:
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
