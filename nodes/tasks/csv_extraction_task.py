from griptape.tasks import (
    CsvExtractionTask,
)

from ...py.griptape_config import get_config
from ..agent.agent import gtComfyAgent as Agent
from .base_task import gtUIBaseTask

OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")


class gtUICsvExtractionTask(gtUIBaseTask):
    DESCRIPTION = "Extract data from a CSV file."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "driver": ("DRIVER",),
                "columns": (
                    "STRING",
                    {
                        "multiline": False,
                        "dynamicPrompts": True,
                        "default": "Column 1, Column 2, Column 3",
                    },
                ),
            }
        )

        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        columns = kwargs.get("columns")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        try:
            if columns:
                column_list = columns.split(",")
            else:
                column_list = ["Column 1"]
            agent.add_task(
                CsvExtractionTask(prompt_text, args={"column_names": column_list})
            )
        except Exception as e:
            print(e)
        result = agent.run()
        # This returns a CSVRowArtifact object, which is not directly usable in ComfyUI
        # So we convert it to a string
        formatted_string = "\n".join(
            [
                ", ".join(
                    [f"{key.strip()}: {value}" for key, value in artifact.value.items()]
                )
                for artifact in result.output_task.output
            ]
        )

        return (formatted_string, agent)
