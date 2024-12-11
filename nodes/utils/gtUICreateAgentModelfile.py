from ..utils.ollama_utils import check_ollama_installed

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUICreateAgentModelfile:
    DESCRIPTION = "Creates a Modelfile to build a new Model for Ollama."

    @classmethod
    def INPUT_TYPES(s):
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
                "base_model": ((), {}),
                "agent": ("AGENT", {}),
                "include_conversation_memory": ("BOOLEAN", {"default": True}),
                "include_rulesets": (
                    "BOOLEAN",
                    {
                        "default": True,
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("MODELFILE",)
    OUTPUT_NODE = True
    CATEGORY = "Griptape/Agent Utils"

    FUNCTION = "create"

    def add_system_prompt(self, agent):
        # Get the rulesets
        if len(agent.rulesets) == 0:
            return
        self.modelfile_contents += 'SYSTEM """'
        rulesets = agent.rulesets
        for ruleset in rulesets:
            if ruleset:
                for rule in ruleset.rules:
                    value = rule.value.strip().rstrip(".") + ". "
                    self.modelfile_contents += value
        self.modelfile_contents += '"""\n'
        return

    def add_messages(self, agent):
        conversation_memory = agent.conversation_memory
        runs = conversation_memory.runs
        if len(runs) == 0:
            return
        for run in runs:
            user_message = run.input.value
            assistant_message = run.output.value
            self.modelfile_contents += f'MESSAGE user "{user_message}"\n'
            self.modelfile_contents += f'MESSAGE assistant "{assistant_message}"\n'

        return

    def create(self, **kwargs):
        agent = kwargs.get("agent", None)
        base_model = kwargs.get("base_model", None)
        if ":" in str(base_model):
            base_model = base_model.split(":")[0]
        include_conversation_memory = kwargs.get("include_conversation_memory", True)
        include_rulesets = kwargs.get("include_rulesets", True)

        self.modelfile_contents = f"FROM {base_model}\n"
        self.modelfile_contents = f"FROM {base_model}\n"
        if include_rulesets:
            self.add_system_prompt(agent)
        if include_conversation_memory:
            self.add_messages(agent)

        return (self.modelfile_contents, base_model)
