from random import randint

from griptape.artifacts import AudioArtifact, ImageArtifact, TextArtifact
from griptape.structures import Pipeline
from griptape.tasks import PromptTask

from .base_structure import gtUIBaseStructure
from .utilities import image_to_comfyui


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUICreatePipeline(gtUIBaseStructure):
    def __init__(self):
        pass

    DESCRIPTION = "Create a Pipeline."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"task_1": ("TASK",)})
        del inputs["required"]["STRING"]
        del inputs["optional"]["input_string"]

        return inputs

    RETURN_TYPES = ("STRUCTURE",)
    RETURN_NAMES = ("STRUCTURE",)

    FUNCTION = "run"
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(s, int_field):
        return randint(0, 1000)

    def run(
        self,
        **kwargs,
    ):
        tasks = []
        for i, (key, value) in enumerate(kwargs.items()):
            if value is not None:
                if i == 0:
                    # append " {{ args[0] }}" to the first task if it's not there.
                    tasks.append(value)
        structure = Pipeline(tasks=tasks)
        return (structure,)


class gtUIPipelineAddTask(gtUIBaseStructure):
    DESCRIPTION = "Add a task to the end of a pipeline."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update({"structure": ("STRUCTURE",)})
        inputs["optional"].update(
            {
                "task": ("TASK", {}),
                "append_parent_output": ("BOOLEAN", {"default": True}),
            }
        )
        return inputs

    @classmethod
    def IS_CHANGED(s, int_field):
        return randint(0, 1000)

    RETURN_TYPES = ("STRUCTURE",)
    RETURN_NAMES = ("STRUCTURE",)

    FUNCTION = "run"
    # OUTPUT_NODE = Tru

    def run(self, **kwargs):
        structure = kwargs.get("structure")
        append_parent_output = kwargs.get("append_parent_output", True)
        task = kwargs.get("task")

        if task:
            if isinstance(task, PromptTask):
                if append_parent_output:
                    prev_value = task.input.value
                    task = PromptTask(
                        "{{ prev_value}}\n\n{{ parent_output }}",
                        context={"prev_value": prev_value},
                    )
                    # print(task.input.value)
                    # print(type(task.input.value))

                    # task.prompt = task.prompt.value + "\n\n" + task.input.value
            structure.add_task(task)
        return (structure,)


class gtUIPipelineInsertTask(gtUIBaseStructure):
    DESCRIPTION = "Insert a task into a pipeline."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update({"structure": ("STRUCTURE",)})
        inputs["optional"].update(
            {
                "parent_task": ("TASK", {}),
                "task": ("TASK", {}),
                "append_parent_output": ("BOOLEAN", {"default": True}),
            },
        )
        return inputs

    @classmethod
    def IS_CHANGED(s, int_field):
        return randint(0, 1000)

    RETURN_TYPES = ("STRUCTURE",)
    RETURN_NAMES = ("STRUCTURE",)

    FUNCTION = "run"
    # OUTPUT_NODE = True

    def run(
        self,
        **kwargs,
    ):
        structure = kwargs.get("structure")
        parent_task = kwargs.get("parent_task")
        task = kwargs.get("task")
        append_parent_output = kwargs.get("append_parent_output", True)

        if task and parent_task:
            if isinstance(task, PromptTask):
                if append_parent_output:
                    prev_value = task.input.value
                    task = PromptTask(
                        "{{ prev_value}}\n\n{{ parent_output }}",
                        context={"prev_value": prev_value},
                    )
                    # print(task.input.value)
                    # print(type(task.input.value))

                    # task.prompt = task.prompt.value + "\n\n" + task.input.value
            structure.insert_task(parent_task, task)
        return (structure,)


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
