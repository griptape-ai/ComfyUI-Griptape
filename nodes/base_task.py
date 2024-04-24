from griptape.tasks import PromptTask, TextSummaryTask, ToolTask, ToolkitTask
from griptape.structures import Agent
from jinja2 import Template

default_prompt = "{{ input_string }}"


class gtUIBaseTask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": default_prompt,
                    },
                ),
            },
            "optional": {
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
                "agent": ("STRUCTURE",),
            },
        }

    RETURN_TYPES = ("STRING", "STRUCTURE")
    RETURN_NAMES = ("output", "agent")

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Tasks"

    def get_prompt_text(self, string_prompt, input_string):
        # We want to take the string_prompt and substitute {{ input_string }}
        template = Template(string_prompt)
        return template.render(input_string=input_string)

    def run(
        self,
        string_prompt,
        input_string=None,
        agent=None,
    ):
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(string_prompt, input_string)
        try:
            agent.add_task(PromptTask(prompt_text))
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent)
