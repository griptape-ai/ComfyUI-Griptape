from griptape.structures import Agent as gtAgent

default_prompt = "{{ input_string }}"


class BaseAgent:
    """
    Create a Griptape Agent
    """

    def __init__(self):
        self.default_prompt = default_prompt
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                    },
                ),
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                    },
                ),
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

    CATEGORY = "Griptape/Run"

    def run(
        self,
        STRING,
        agent=None,
        input_string=None,
    ):
        if not agent:
            agent = gtAgent()

        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n\n" + input_string

        result = agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            agent,
        )
