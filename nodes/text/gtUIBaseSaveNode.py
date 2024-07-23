import os

import folder_paths


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIBaseSaveNode:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    DESCRIPTION = "Save a file."

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "text": ("STRING", {"default": "", "forceInput": True}),
                "filename_prefix": ("STRING", {"default": ""}),
            },
            "optional": {},
        }
        return inputs

    # INPUT_IS_LIST = True
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "Griptape/Text"
    RETURN_TYPES = ()

    def create_output_path(self, path_filename):
        # Check if the path is absolute
        if os.path.isabs(path_filename):
            full_path = os.path.dirname(path_filename)
            filename = os.path.basename(path_filename)
        else:
            # Normalize the path to handle both Windows and Unix-style paths
            normalized_path = os.path.normpath(path_filename)

            # Split the path into directory and filename
            path, filename = os.path.split(normalized_path)

            # Combine the output_dir with the provided path
            full_path = os.path.join(self.output_dir, path)

        # Create all necessary directories
        os.makedirs(full_path, exist_ok=True)

        # Construct the full output path
        full_output_path = os.path.join(full_path, filename)

        return full_output_path

    def save(self, **kwargs):
        print(f": {kwargs['text']=}")
        print(f"Saving file: {kwargs['filename_prefix']}")
        return {"ui": {"message": f"Saved file: {kwargs['filename_prefix']}"}}
