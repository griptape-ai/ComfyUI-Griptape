from griptape.structures import Agent as gtAgent
from griptape.drivers import OpenAiChatPromptDriver, OpenAiEmbeddingDriver
from griptape.config import (
    OpenAiStructureConfig,
)
from jinja2 import Template

default_prompt = "{{ input_prompt }}"


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
                "input_prompt": (
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

    RETURN_TYPES = ("STRING", "STRUCTURE")
    RETURN_NAMES = ("output", "agent")
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent"

    def get_prompt_text(self, string_prompt, input_prompt):
        # We want to take the string_prompt and substitute {{ prompt }}
        template = Template(string_prompt)
        return template.render(input_prompt=input_prompt)

    def run(
        self,
        string_prompt,
        agent=None,
        input_prompt=None,
    ):
        if not agent:
            agent = gtAgent(config=OpenAiStructureConfig())

        if not input_prompt:
            prompt_text = string_prompt
        else:
            prompt_text = self.get_prompt_text(string_prompt, input_prompt)
        result = agent.run(prompt_text)
        output_string = result.output_task.output.value
        return (
            output_string,
            agent,
        )
