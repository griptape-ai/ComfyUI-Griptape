import os

from .gtUIBaseSaveNode import gtUIBaseSaveNode


class gtUISaveText(gtUIBaseSaveNode):
    DESCRIPTION = "Save text to a file."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "filename_prefix": ("STRING", {"default": "griptape_output.txt"}),
            }
        )
        return inputs

    def save(self, **kwargs):
        text = kwargs.get("text", None)
        filename_prefix = kwargs.get("filename_prefix", None)

        full_output_folder = self.output_dir

        full_output_file = os.path.join(full_output_folder, filename_prefix)

        try:
            with open(full_output_file, "w") as f:
                f.write(text)
            print(f"Saved file: {full_output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")
            return (None, str(e))
        return (full_output_file,)
