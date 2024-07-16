from random import randint

from griptape.tasks import PromptTask

from .BaseStructure import gtUIBaseStructure


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


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
