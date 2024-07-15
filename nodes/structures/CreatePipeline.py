from random import randint

from griptape.structures import Pipeline

from .BaseStructure import gtUIBaseStructure


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
