class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


import folder_paths

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

    def save(self, **kwargs):
        print(f": {kwargs['text']=}")
        print(f"Saving file: {kwargs['filename_prefix']}")
        return {"ui": {"message": f"Saved file: {kwargs['filename_prefix']}"}}
