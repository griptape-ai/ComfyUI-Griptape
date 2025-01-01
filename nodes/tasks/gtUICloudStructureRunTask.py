from typing import Any, Tuple

from griptape.drivers import GriptapeCloudStructureRunDriver
from griptape.tasks import StructureRunTask

from ...py.griptape_settings import GriptapeSettings
from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class gtUICloudStructureRunTask(gtUIBaseTask):
    DESCRIPTION = "Runs a Griptape Cloud Structure"
    CATEGORY = "Griptape/Code"
    OUTPUTS = ("STRING", "AGENT")

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        del inputs["required"]["STRING"]

        inputs["required"].update(
            {
                "structure_id": (
                    "STRING",
                    {
                        "placeholder": "xxxx-xxxx-xxxx-xxxx",
                        "default": "",
                    },
                ),
                "split_input_into_args": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "If enabled, the input string will be split into separate arguments by newline.",
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
            }
        )
        return inputs

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        split_input_into_args = kwargs.get("split_input_into_args", False)
        agent = kwargs.get("agent", None)
        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string).strip()
        if split_input_into_args:
            prompt_texts = prompt_text.split("\n")
        else:
            prompt_texts = [prompt_text]
        structure_id = kwargs.get("structure_id", "")
        settings = GriptapeSettings()
        api_key = settings.get_settings_key_or_use_env("GRIPTAPE_CLOUD_API_KEY")
        if not api_key:
            api_key = ""
        structure_run_driver = GriptapeCloudStructureRunDriver(
            api_key=api_key, structure_id=structure_id
        )
        task = StructureRunTask(structure_run_driver=structure_run_driver)
        prev_task = agent.tasks[0]
        try:
            agent.add_task(task)
            result = agent.run([arg for arg in prompt_texts if arg.strip()])
            value = result.output_task.output.value
            agent.add_task(prev_task)
            return (value, agent)
        except Exception as e:
            return (str(e), None)
            print(e)
