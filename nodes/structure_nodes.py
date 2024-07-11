from random import randint

from griptape.structures import Pipeline
from griptape.tasks import PromptTask

from .base_structure import gtUIBaseStructure


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
        tasks = [value for value in kwargs.values()]
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

    def run(
        self,
        structure,
        append_parent_output,
        task=None,
    ):
        if task:
            if isinstance(task, PromptTask):
                if append_parent_output:
                    prev_value = task.input.value
                    task = PromptTask(
                        "{{ prev_value}}\n\n{{ parent_output }}",
                        context={"prev_value": prev_value},
                    )
                    print(f"{task.input=}")
                    print(f"{task=}")
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
        structure,
        parent_task=None,
        task=None,
        append_parent_output=True,
    ):
        if task and parent_task:
            if isinstance(task, PromptTask):
                if append_parent_output:
                    prev_value = task.input.value
                    task = PromptTask(
                        "{{ prev_value}}\n\n{{ parent_output }}",
                        context={"prev_value": prev_value},
                    )
                    print(f"{task.input=}")
                    print(f"{task=}")
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
                "STRING": ("STRING", {"default": "Enter a task prompt here."}),
            }
        )
        return inputs

    RETURN_TYPES = (
        any,
        "STRUCTURE",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "STRUCTURE",
    )

    FUNCTION = "run"
    OUTPUT_NODE = True

    def run(self, structure, STRING):
        result = structure.run(STRING)
        return (result.output_task.output,)
