from .ollama_utils import (
    check_ollama_installed,
    clean_result,
    run_ollama_command,
)

default_port = "11434"
default_base_url = "http://127.0.0.1"

# models = get_available_models()
# DEFAULT_MODEL = ""
# if len(models) > 0:
#     DEFAULT_MODEL = models[0]


class gtUIRemoveOllamaModel:
    DESCRIPTION = "Ollama can sometimes be overrun with models. This node allows you to remove a model by name."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL of the Ollama server",
                    },
                ),
                "port": (
                    "STRING",
                    {
                        "default": default_port,
                        "tooltip": "The port of the Ollama server",
                    },
                ),
                "model": (
                    (),
                    {"tooltip": "The model to remove"},
                ),
            }
        }
        return inputs

    @classmethod
    def VALIDATE_INPUTS(cls):
        if not check_ollama_installed():
            return "You must have ollama installed on your machine to use this node."
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    OUTPUT_NODE = True
    CATEGORY = "Griptape/Agent Utils"

    FUNCTION = "remove"

    def remove(self, **kwargs):
        model = kwargs.get("model", None)

        # run the command to remove the model
        cmd = f"rm {model}"
        result = run_ollama_command(cmd)

        cleaned_output = clean_result(result)
        return (cleaned_output,)
