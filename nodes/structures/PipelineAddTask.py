from random import randint

from griptape.tasks import PromptTask

from .BaseStructure import gtUIBaseStructure


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


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
