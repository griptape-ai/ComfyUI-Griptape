from .BaseAgent import BaseAgent
from .gtComfyAgent import gtComfyAgent


class RunAgent(BaseAgent):
    DESCRIPTION = "Run a simple Griptape Agent"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["config"]
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]

        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING", "")
        agent = kwargs.get("agent", None)
        input_string = kwargs.get("input_string", None)

        if not agent:
            self.agent = gtComfyAgent()
        else:
            self.agent = agent

        # Warn for models
        model, simple_model = self.agent.model_check()
        if simple_model:
            return (self.agent.model_response(model), self.agent)

        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string
        tools = self.agent.tools
        # if len(tools) > 0:
        #     self.agent.add_task(ToolkitTask(prompt_text, tools=tools))
        # else:
        #     self.agent.add_task(PromptTask(prompt_text))
        result = self.agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            self.agent,
        )
