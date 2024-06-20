from textwrap import dedent

from griptape.config import (
    OpenAiStructureConfig,
)
from griptape.drivers import OllamaPromptDriver
from griptape.structures import Agent as gtAgent
from griptape.tools import TaskMemoryClient

from .base_agent import BaseAgent

default_prompt = "{{ input_string }}"


def model_check(agent):
    # There are certain models that can't handle Tools well.
    # If this agent is using one of those models AND they have tools supplied, we'll
    # warn the user.
    simple_models = ["llama3", "mistral"]

    model = agent.config.prompt_driver.model
    if isinstance(agent.config.prompt_driver, OllamaPromptDriver):
        if model == "":
            return (model, True)
        if model in simple_models:
            if len(agent.tools) > 0:
                return (model, True)
    return (model, False)


class RunAgent(BaseAgent):
    def run(
        self,
        STRING,
        agent=None,
        input_string=None,
    ):
        if not agent:
            agent = gtAgent()

        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string

        # There are certain models that can't handle Tools well.
        model, simple_model = model_check(agent)
        if simple_model:
            if model == "":
                return (
                    "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent.",
                    agent,
                )
            else:
                return (
                    dedent(
                        f"""This Agent Configuration Model: **{ agent.config.prompt_driver.model }** may run into issues using tools.\n\nPlease consider using a different configuration, a different model, or removing tools from the agent and use the **Griptape Run: Tool Task** node for specific tool use."""
                    ),
                    agent,
                )
        result = agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            agent,
        )


class CreateAgent(BaseAgent):
    """
    Create a Griptape Agent
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                    },
                ),
                "tools": ("TOOL_LIST", {"forceInput": True, "INPUT_IS_LIST": True}),
                "rulesets": ("RULESET", {"forceInput": True}),
            },
        )
        return inputs

    RETURN_TYPES = ("STRING", "AGENT")
    RETURN_NAMES = ("OUTPUT", "AGENT")
    FUNCTION = "run"

    CATEGORY = "Griptape/Agent"

    def run(
        self,
        STRING,
        agent=None,
        config=None,
        input_string=None,
        tools=[],
        rulesets=[],
    ):
        if not config:
            config = OpenAiStructureConfig()

        task_memory_client = [TaskMemoryClient(off_prompt=False)]
        agent_tools = []
        if len(tools) > 0:
            agent_tools += tools

        agent_tools += task_memory_client if len(agent_tools) > 0 else []

        agent_rulesets = []
        for ruleset in rulesets:
            agent_rulesets.append(ruleset)
        if not agent:
            agent = gtAgent(config=config, tools=agent_tools, rulesets=agent_rulesets)
        else:
            if config:
                agent.config = config
            if len(tools) > 0:
                agent.tools = agent_tools
            if len(rulesets) > 0:
                agent.rulesets = agent_rulesets

        # There are certain models that can't handle Tools well.
        # If this agent is using one of those models AND they have tools supplied, we'll
        # warn the user.
        model, simple_model = model_check(agent)
        if simple_model:
            if model == "":
                return (
                    "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent.",
                    agent,
                )
            else:
                return (
                    dedent(
                        f"""This Agent Configuration Model: **{ agent.config.prompt_driver.model }** may run into issues using tools.\n\nPlease consider using a different configuration, a different model, or removing tools from the agent and use the **Griptape Run: Tool Task** node for specific tool use."""
                    ),
                    agent,
                )
        # Run the agent if there's a prompt
        if input_string or STRING not in [default_prompt, ""]:
            if not input_string:
                prompt_text = STRING
            else:
                prompt_text = STRING + "\n" + input_string

            result = agent.run(prompt_text)
            output_string = result.output_task.output.value
        else:
            output_string = "Agent Created"
        return (output_string, agent)


class ExpandAgent:
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
    RETURN_NAMES = ("AGENT", "CONFIG", "RULESETS", "TOOLS", "MEMORY")

    FUNCTION = "expand"

    CATEGORY = "Griptape/Agent"
    OUTPUT_NODE = True

    def expand(self, agent):
        rulesets = agent.rulesets
        tools = agent.tools
        conversation_memory = agent.conversation_memory
        config = agent.config
        # Run the agent
        return (agent, config, rulesets, tools, conversation_memory)
