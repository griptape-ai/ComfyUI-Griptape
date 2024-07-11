import re
from random import randint

from griptape.tasks import PromptTask

from .agent.agent import gtComfyAgent as Agent


class gtUIBaseTask:
    def __init__(self):
        pass

    DESCRIPTION = "Run a PromptTask."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "deferred_evaluation": ("BOOLEAN", {"default": False}),
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                        "dynamicPrompts": True,
                        "default": "",
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
                "agent": ("AGENT",),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "AGENT",
        "TASK",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
        "TASK",
    )

    FUNCTION = "run"
    # OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent Tasks"

    @classmethod
    def IS_CHANGED(s, deferred_evaluation):
        if deferred_evaluation:
            return randint(0, 1000)
        else:
            return ""

    def get_prompt_text(self, STRING, input_string):
        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string

        prompt_text = self.format_parent_output_string(prompt_text)
        print(f"{prompt_text=}")
        return prompt_text

    def format_parent_output_string(self, input_string):
        # Check if the string already contains properly formatted versions
        if re.search(r"\{\{\s*parent_outputs?\s*\}\}", input_string):
            return input_string

        # Replace 'parent_output' with '{{ parent_output }}'
        input_string = re.sub(r"\bparent_output\b", "{{ parent_output }}", input_string)

        # Replace 'parent_outputs' with '{{ parent_outputs }}'
        input_string = re.sub(
            r"\bparent_outputs\b", "{{ parent_outputs }}", input_string
        )

        return input_string

    def run(
        self,
        STRING,
        deferred_evaluation=False,
        input_string=None,
        agent=None,
    ):
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)
        task = PromptTask(prompt_text)
        if deferred_evaluation:
            try:
                return (
                    "Prompt Task created.",
                    agent,
                    task,
                )
            except Exception as e:
                print(e)
        else:
            try:
                agent.add_task(task)
            except Exception as e:
                print(e)
            result = agent.run()
            return (
                result.output_task.output.value,
                agent,
                task,
            )
