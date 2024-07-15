from griptape.tasks import (
    PromptTask,
    ToolTask,
)

from ...py.griptape_config import get_config
from ..agent.agent import gtComfyAgent as Agent
from .base_task import gtUIBaseTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")


class gtUIToolTask(gtUIBaseTask):
    DESCRIPTION = "Run a tool on a text prompt."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tool": ("TOOL_LIST",),
            }
        )
        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        tool = kwargs.get("tool", [])
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)

        # Figure out what tool to use.
        # If none are provided, check the agent for tools
        # if the agent doesn't have any, then we won't use any tools.
        agent_tools = []
        agent_tools = agent.tools

        if len(tool) > 0:
            agent_tool = tool[0]
        elif len(agent_tools) > 0:
            agent_tool = agent_tools[0]
        else:
            agent_tool = None

        if agent_tool:
            # No point in using off_prompt if we're using a ToolTask - it's not supported
            agent_tool.off_prompt = False
            task = ToolTask(prompt_text, tool=agent_tool)
        else:
            task = PromptTask(prompt_text)

        # if deferred_evaluation:
        #     return ("Tool Task Created", task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent)
