import re

from icecream import ic

from ..utils.ollama_utils import check_ollama_installed, run_ollama_command


class gtUICreateAgentFromModelfile:
    DESCRIPTION = "Builds a new agent model using Ollama and a modelfile."

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "modelfile": (
                    "STRING",
                    {"forceInput": True},
                ),
                "base_model": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
                "new_model_name": (
                    "STRING",
                    {
                        "default": "new_model",
                    },
                ),
            }
        }
        return inputs

    @classmethod
    def VALIDATE_INPUTS(s):
        if not check_ollama_installed():
            return "You must have ollama installed on your machine to use this node."
        return True

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "NEW_MODEL_NAME",
    )
    OUTPUT_NODE = True
    CATEGORY = "Griptape/Agent"

    FUNCTION = "create"

    def clean_result(self, result):
        # Split the result into lines
        lines = result[0].split("\n")

        # Initialize lists to store different types of information
        layer_info = []
        other_info = []

        for line in lines:
            # Remove ANSI escape codes and strip whitespace
            clean_line = re.sub(r"\x1b\[.*?[\@-~]", "", line).strip()

            if "layer" in clean_line:
                # Extract and format layer information
                layer_type = (
                    "existing" if "using existing layer" in clean_line else "new"
                )
                sha = clean_line.split("sha256:")[-1].strip()
                layer_info.append(f"{layer_type.capitalize()} layer: sha256:{sha}")
            elif clean_line and not clean_line.startswith(("using", "creating")):
                # Add other relevant information
                other_info.append(clean_line)

        # Combine the formatted information
        cleaned_result = "\n".join(
            other_info + ["\n===========================\n"] + layer_info
        )
        return cleaned_result

    def create(self, **kwargs):
        modelfile = kwargs.get("modelfile", None)
        base_model = kwargs.get("base_model")
        ic(base_model)
        if ":" in str(base_model):
            base_model = base_model.split(":")[0]
        new_model_name = str(kwargs.get("new_model_name", "new_model"))

        # Save the contents of modelfile to a file named Modelfile.
        modelfile_path = "Modelfile"
        with open(modelfile_path, "w") as f:
            f.write(modelfile)

        # build the new modelname
        new_model = f"{new_model_name}-{base_model}"

        # run the command to cp the new model
        cmd = f"cp {base_model} {new_model}"
        ic(cmd)
        result = run_ollama_command(cmd)
        ic(result)

        # run the ollama command to create the new model
        cmd = f"create {new_model} -f {modelfile_path}"
        ic(cmd)
        result = run_ollama_command(cmd)
        ic(result)
        cleaned_output = self.clean_result(result)
        ic(cleaned_output)
        return (cleaned_output, new_model)
