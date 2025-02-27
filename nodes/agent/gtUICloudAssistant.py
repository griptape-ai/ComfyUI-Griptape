import re
from typing import Any, Tuple

import requests
from griptape.drivers.assistant.griptape_cloud import GriptapeCloudAssistantDriver
from griptape.drivers.memory.conversation.griptape_cloud import (
    GriptapeCloudConversationMemoryDriver,
)
from griptape.memory.structure import ConversationMemory
from griptape.structures import Pipeline
from griptape.tasks import AssistantTask

from ...py.griptape_settings import GriptapeSettings
from ..utilities import replace_with_context


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


def get_first_n_words(text, n=10):
    words = text.split()
    return " ".join(words[:n])


class Assistant:
    def __init__(self, assistant_id: str):
        settings = GriptapeSettings()
        self.api_key = settings.get_settings_key_or_use_env("GT_CLOUD_API_KEY")
        if not self.api_key:
            self.api_key = settings.get_settings_key_or_use_env("GT_CLOUD_API_KEY")
        conversation_memory_driver = GriptapeCloudConversationMemoryDriver(
            api_key=self.api_key
        )
        conversation_memory = ConversationMemory(
            conversation_memory_driver=conversation_memory_driver
        )
        self.thread_id = conversation_memory.conversation_memory_driver.thread_id

        self.assistant_driver = GriptapeCloudAssistantDriver(
            api_key=self.api_key, assistant_id=assistant_id, thread_id=self.thread_id
        )

    def set_thread_name(self, thread_name: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = {"name": get_first_n_words(thread_name)}
        try:
            response = requests.patch(
                f"https://cloud.griptape.ai/api/threads/{self.thread_id}",
                headers=headers,
                json=data,
            )
            if response.status_code == 200:
                return True
        except Exception as e:
            print(e)
            return False


class gtUICloudAssistant:
    DESCRIPTION = "Runs a Griptape Cloud Assistant"
    CATEGORY = "Griptape/Agent"
    RETURN_TYPES = (
        "STRING",
        "ASSISTANT",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "ASSISTANT",
    )
    OUTPUT_TOOLTIPS = (
        "Text response from the Agent",
        "The Assistant. Can be connected to other nodes.",
    )
    FUNCTION = "run"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "assistant": (
                    "ASSISTANT",
                    {
                        "forceInput": True,
                        "tooltip": "An existing assistant to use.\nIf not provided, an assistant_id must be specified.",
                    },
                ),
                "assistant_id": (
                    "STRING",
                    {
                        "placeholder": "xxxx-xxxx-xxxx-xxxx",
                        "default": "",
                        "tooltip": "The id of your assistant to run.\nIf an assistant is connect, this will be ignored.",
                    },
                ),
                "split_input_into_args": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "If enabled, the input string will be split into separate arguments by newline.",
                    },
                ),
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                        "multiline": True,
                        "tooltip": "Additional text be appended to the STRING with a newline character.",
                    },
                ),
                "key_value_replacement": (
                    "DICT",
                    {
                        "tooltip": "The will replace the {{ key }} with a value.",
                    },
                ),
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                        "placeholder": "Enter arguments, one per line",
                        "tooltip": "Specify input arguments that will be passed to the structure during execution.",
                    },
                ),
            },
        }

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

    def get_prompt_text(self, STRING, input_string):
        # Get the prompt text
        if not input_string:
            prompt_text = STRING
        else:
            prompt_text = STRING + "\n" + input_string

        prompt_text = self.format_parent_output_string(prompt_text)
        return prompt_text

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("STRING")
        self.assistant = kwargs.get("assistant", None)
        if not self.assistant:
            assistant_id = kwargs.get("assistant_id", "")
            self.assistant = Assistant(assistant_id=assistant_id)

        if not self.assistant and assistant_id == "":
            msg = "An assistant or assistant_id must be provided."
            return (msg, None)

        input_string = kwargs.get("input_string", None)
        split_input_into_args = kwargs.get("split_input_into_args", False)

        prompt_text = self.get_prompt_text(STRING, input_string).strip()
        context = kwargs.get("key_value_replacement", None)
        if context:
            prompt_text = replace_with_context(prompt_text, context)
        if split_input_into_args:
            prompt_texts = prompt_text.split("\n")
        else:
            prompt_texts = [prompt_text]

        self.assistant.set_thread_name(prompt_texts[0])

        pipeline = Pipeline(
            tasks=[AssistantTask(assistant_driver=self.assistant.assistant_driver)]
        )
        try:
            result = pipeline.run([arg for arg in prompt_texts if arg.strip()])
            value = result.output_task.output.value
            return (value, self.assistant)
        except Exception as e:
            return (str(e), None)
            print(e)
