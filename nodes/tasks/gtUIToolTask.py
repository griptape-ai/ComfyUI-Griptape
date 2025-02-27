from griptape.tasks import (
    ToolTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class gtUIToolTask(gtUIBaseTask):
    DESCRIPTION = "Run a tool on a text prompt."
    CATEGORY = "Griptape/Agent"

    @classmethod
    def INPUT_TYPES(cls):
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

        if len(tool) == 0:
            return ("No tool provided.", agent)

        # If using Ollama, we need to turn off stream
        if "ollama" in str(type(agent.prompt_driver)).lower():
            agent.prompt_driver.stream = False

        # If using LMStudio, turn off native tools
        if "lmstudio" in str(type(agent.prompt_driver.model)).lower():
            agent.prompt_driver.use_native_tools = False

        prompt_text = self.get_prompt_text(STRING, input_string)

        agent.add_task(
            ToolTask(
                tool=tool[0],
            )
        )
        context = self.get_context_as_dict(kwargs.get("key_value_replacement", None))
        if context:
            agent.tasks[0].context = context
        result = agent.run(prompt_text)
        if isinstance(result.output_task.output.value, list):
            output = result.output_task.output.value[0]
        else:
            output = result.output_task.output.value
        return (output, agent)
