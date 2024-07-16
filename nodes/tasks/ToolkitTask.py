from griptape.tasks import (
    ToolkitTask,
)

from ..agent.agent import gtComfyAgent as Agent
from .BaseTask import gtUIBaseTask


class gtUIToolkitTask(gtUIBaseTask):
    DESCRIPTION = "Provide a list of tools, and have the agent decide which of them to use utilizing Chain of Thought."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tools": ("TOOL_LIST",),
            }
        )
        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        tools = kwargs.get("tools", [])
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        prompt_text = self.get_prompt_text(STRING, input_string)

        if len(tools) == 0:
            return super().run(STRING, input_string, agent)

        if prompt_text.strip() == "":
            return ("No prompt provided", agent)
        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        model, simple_model = agent.model_check()
        if simple_model:
            response = agent.model_response(model)
            return (response, agent)

        task = ToolkitTask(
            prompt_text,
            tools=tools,
        )
        # if deferred_evaluation:
        #     return ("Toolkit Task Created.", task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)

        result = agent.run()
        return (result.output_task.output.value, agent)
