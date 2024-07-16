from griptape.artifacts import AudioArtifact, ImageArtifact, TextArtifact

from ..utilities import image_to_comfyui
from .BaseStructure import gtUIBaseStructure


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIRunStructure(gtUIBaseStructure):
    def __init__(self):
        pass

    DESCRIPTION = "Run a Structure."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update({"structure": ("STRUCTURE",)})
        inputs["optional"].update(
            {
                "STRING": ("STRING", {"default": "", "multiline": True}),
            }
        )
        return inputs

    RETURN_TYPES = (
        any,
        "STRING",
        "STRUCTURE",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "TASK_OUTPUTS",
        "STRUCTURE",
    )

    FUNCTION = "run"
    OUTPUT_NODE = True

    def append_prompt_text(self, structure, prompt_text):
        if prompt_text.strip() != "":
            # Check and see if the first task has an input
            if structure.tasks:
                first_task = structure.tasks[0]
                if isinstance(first_task.input, TextArtifact):
                    new_artifact = TextArtifact(
                        first_task.input.value + "\n\n {{ args[0] }}"
                    )
                    first_task.input = new_artifact
                    structure.tasks[0] = first_task

        return structure

    def run(self, **kwargs):
        STRING = kwargs.get("STRING", "")
        structure = kwargs.get("structure")
        input_string = kwargs.get("input_string", "")

        prompt_text = self.get_prompt_text(STRING, input_string)

        # If prompt_text isn't empty, we'll need to add it to the first task if we can.
        structure = self.append_prompt_text(structure, prompt_text)
        # Run the structure
        result = structure.run(prompt_text)

        # Handle the results
        task_outputs = repr(
            [
                {"input": task.input.value, "output": task.output.value}
                for task in structure.tasks
            ]
        )

        # Depending on the type of output, we'll need to adjust it
        if isinstance(result.output_task.output, str):
            output = result.output_task.output
        elif isinstance(result.output_task.output, TextArtifact):
            output = result.output_task.output.value
        elif isinstance(result.output_task.output, ImageArtifact):
            output, output_mask = image_to_comfyui(result.output_task.output.value)
        elif isinstance(result.output_task.output, AudioArtifact):
            output = type(result.output_task.output)
        return (output, task_outputs, structure)
