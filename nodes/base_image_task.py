from .base_task import gtUIBaseTask


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

    CATEGORY = "Griptape/Create"

    def run(self, STRING, image, input_string=None, agent=None):
        output = "Output"
        return (output, agent)
