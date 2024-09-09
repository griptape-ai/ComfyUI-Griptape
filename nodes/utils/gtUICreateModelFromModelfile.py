from icecream import ic

from .ollama_utils import check_ollama_installed, clean_result, run_ollama_command


class gtUICreateModelFromModelfile:
    DESCRIPTION = (
        "Given a modelfile and a base model, creates a new model using Ollama."
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "modelfile": (
                    "STRING",
                    {"forceInput": True},
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
    CATEGORY = "Griptape/Agent Utils"

    FUNCTION = "create"

    def get_base_model(self, modelfile):
        # Modelfile is a string and the first line has a FROM line that looks like:
        # FROM base_model
        # so we need to get the base_model
        lines = modelfile.split("\n")
        for line in lines:
            if line.startswith("FROM"):
                return line.split(" ")[1]
        return None

    def create(self, **kwargs):
        modelfile = kwargs.get("modelfile", None)
        base_model = self.get_base_model(modelfile)
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
        cleaned_output = clean_result(result)
        ic(cleaned_output)
        return (cleaned_output, new_model)
