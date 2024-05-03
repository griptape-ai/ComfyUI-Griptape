from griptape.structures import Agent as gtAgent
from griptape.config import (
    OpenAiStructureConfig,
)
from griptape.tools import TaskMemoryClient

from .base_agent import BaseAgent
from .utilities import get_prompt_text

default_prompt = "{{ input_string }}"


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

    CATEGORY = "Griptape/Create"

    def run(
        self,
        string_prompt,
        config=None,
        tool=None,
        input_string=None,
        tools=[],
        rulesets=[],
    ):
        if not config:
            config = OpenAiStructureConfig()

        task_memory_client = [TaskMemoryClient(off_prompt=False)]
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
        if input_string or string_prompt not in [default_prompt, ""]:
            if not input_string:
                prompt_text = string_prompt
            else:
                prompt_text = get_prompt_text(string_prompt, input_string)
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

    CATEGORY = "Griptape/Combine-Expand"

    def expand(self, agent):

        rulesets = agent.rulesets
        tools = agent.tools
        conversation_memory = agent.conversation_memory
        config = agent.config
        # Run the agent
        return (agent, config, rulesets, tools, conversation_memory)
