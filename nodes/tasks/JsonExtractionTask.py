import os

from griptape.tasks import (
    JsonExtractionTask,
)
from schema import Schema

from ..agent.agent import gtComfyAgent as Agent
from .BaseTask import gtUIBaseTask

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class gtUIJsonExtractionTask(gtUIBaseTask):
    DESCRIPTION = "Extract data from a JSON file."

    @classmethod
    def INPUT_TYPES(s):
        default_schema = '{"users": [{"name": str, "age": int, "location": str}]}'
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "driver": ("DRIVER",),
                "schema": (
                    "STRING",
                    {
                        "multiline": True,
                        "dynamicPrompts": True,
                        "default": default_schema,
                    },
                ),
            }
        )

        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        schema = kwargs.get("schema")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        try:
            if schema:
                print(schema)
                template_schema = Schema(schema).json_schema("TemplateSchema")
            else:
                template_schema = Schema({}).json_schema("TemplateSchema")
            agent.add_task(
                JsonExtractionTask(
                    prompt_text, args={"template_schema": template_schema}
                )
            )
        # TODO - error extracting json
        except Exception as e:
            print(e)
        result = agent.run()
        output = result.output_task.output
        print(output)

        return (str(output.value), agent)
