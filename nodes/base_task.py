from griptape.structures import Agent
from griptape.tasks import PromptTask


class gtUIBaseTask:
    def __init__(self):
        pass

    DESCRIPTION = "Run a PromptTask."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
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
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
    )

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent Tasks"

    def get_prompt_text(self, STRING, input_string):
        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string

        return prompt_text

    def run(
        self,
        STRING,
        input_string=None,
        agent=None,
    ):
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)
        try:
            agent.add_task(PromptTask(prompt_text))
        except Exception as e:
            print(e)
        result = agent.run()
        return (
            result.output_task.output.value,
            agent,
        )
