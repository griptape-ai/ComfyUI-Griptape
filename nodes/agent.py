from griptape.structures import Agent as gtAgent
from griptape.drivers import OpenAiChatPromptDriver, OpenAiEmbeddingDriver
from griptape.config import (
    StructureConfig,
    StructureGlobalDriversConfig,
    OpenAiStructureConfig,
)
from griptape.tools import TaskMemoryClient

from .base_agent import BaseAgent
from jinja2 import Template

default_prompt = "{{ input_prompt }}"


class ExpandAgent:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agent": (
                    "STRUCTURE",
                    {
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRUCTURE",
        "CONFIG",
        "RULESET",
        "TOOL_LIST",
        "MEMORY",
    )
    RETURN_NAMES = ("agent", "config", "rulesets", "tools", "conversation_memory")

    FUNCTION = "expand"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent"

    def expand(self, agent):

        rulesets = agent.rulesets
        tools = agent.tools
        conversation_memory = agent.conversation_memory
        config = agent.config
        # Run the agent
        return (agent, config, rulesets, tools, conversation_memory)


class RunAgent(BaseAgent): ...


class CreateAgent(BaseAgent):
    """
    Create a Griptape Agent
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        default_config = OpenAiStructureConfig()
        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                    },
                ),
                "tool": ("TOOL", {"forceInput": True}),
                "tools": ("TOOL_LIST", {"forceInput": True, "INPUT_IS_LIST": True}),
                "rulesets": ("RULESET", {"forceInput": True}),
            },
        )
        return inputs

    RETURN_TYPES = ("STRING", "STRUCTURE")
    RETURN_NAMES = ("output", "agent")
    FUNCTION = "run"

    # OUTPUT_NODE = False

    def run(
        self,
        string_prompt,
        config=None,
        tool=None,
        input_prompt=None,
        tools=[],
        rulesets=[],
    ):
        if not config:
            config = OpenAiStructureConfig()

        task_memory_client = [TaskMemoryClient(off_prompt=False)]
        # print(f"Model: {config.global_drivers.prompt_driver.model}")
        # Collect the tools to be used
        agent_tools = []
        if tool:
            agent_tools = [tool]
        if len(tools) > 0:
            agent_tools += tools

        agent_tools += task_memory_client if len(agent_tools) > 0 else []

        agent_rulesets = []
        for ruleset in rulesets:
            agent_rulesets.append(ruleset)
        agent = gtAgent(config=config, tools=agent_tools, rulesets=agent_rulesets)

        # Run the agent if there's a prompt
        if input_prompt or string_prompt not in [default_prompt, ""]:
            if not input_prompt:
                prompt_text = string_prompt
            else:
                prompt_text = self.get_prompt_text(string_prompt, input_prompt)
            result = agent.run(prompt_text)
            output_string = result.output_task.output.value
        else:
            output_string = "Agent Created"
        return (output_string, agent)

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
