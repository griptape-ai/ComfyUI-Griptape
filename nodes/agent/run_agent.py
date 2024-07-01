from .base_agent import BaseAgent


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

        # Warn for models
        model, simple_model = self.agent.model_check()
        if simple_model:
            return (self.agent.model_response(model), self.agent)

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
