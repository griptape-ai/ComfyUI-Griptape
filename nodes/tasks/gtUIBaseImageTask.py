from typing import Any, Tuple

from .gtUIBaseTask import gtUIBaseTask


class gtUIBaseImageTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'image' and adjust others as necessary
        inputs["required"].update(
            {
                "image": ("IMAGE",),
            }
        )
        return inputs

    CATEGORY = "Griptape/Image"

    def run(self, **kwargs) -> Tuple[Any, ...]:
        agent = kwargs.get("agent", None)
        output = "Output"
        return (output, agent)
