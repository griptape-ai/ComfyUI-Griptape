from griptape.tasks import PromptTask, ToolkitTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class gtUIToolkitTask(gtUIBaseTask):
    DESCRIPTION = "Provide a list of tools, and have the agent decide which of them to use utilizing Chain of Thought."
    CATEGORY = "Griptape/Agent"

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

        if prompt_text.strip() == "":
            return ("No prompt provided", agent)
        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        model, simple_model = agent.model_check()
        if simple_model:
            response = agent.model_response(model)
            return (response, agent)

        if len(tools) == 0:
            task = PromptTask(
                prompt_text,
            )
        else:
            task = ToolkitTask(
                prompt_text,
                tools=tools,
            )
        context = self.get_context_as_dict(kwargs.get("key_value_replacement", None))
        if context:
            task.context = context
        # if deferred_evaluation:
        #     return ("Toolkit Task Created.", task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)

        result = agent.run()
        return (result.output_task.output.value, agent)
