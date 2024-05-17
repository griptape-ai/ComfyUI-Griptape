from griptape.config import (
    OpenAiStructureConfig,
)
from griptape.structures import Agent as gtAgent

from .utilities import get_prompt_text

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
                    "STRUCTURE",
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
                "string_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": default_prompt,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRUCTURE",
    )
    RETURN_NAMES = (
        "output",
        "agent",
    )
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Run"

    def run(
        self,
        string_prompt,
        agent=None,
        input_string=None,
    ):
        if not agent:
            agent = gtAgent(config=OpenAiStructureConfig(model="gpt-4o"))

        # Get the prompt text
        if input_string or string_prompt not in [default_prompt, ""]:
            if not input_string:
                prompt_text = string_prompt
            else:
                prompt_text = get_prompt_text(string_prompt, input_string)
        else:
            prompt_text = "Hello"
        result = agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            agent,
        )
