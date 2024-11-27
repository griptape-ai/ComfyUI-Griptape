from griptape.tasks import PromptTask, TextSummaryTask, ToolkitTask, ToolTask
from openai import OpenAIError

# from server import PromptServer
from .gtComfyAgent import gtComfyAgent

default_prompt = "{{ input_string }}"
max_attempts_default = 10


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


run_types = ["Default", "Prompt", "Tool(s)", "Summarize"]


class gtUIRunAgent:
    """
    Run a Griptape Agent
    """

    def __init__(self):
        self.default_prompt = default_prompt
        self.agent = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                        "tooltip": "An existing agent to use.\nIf not provided, a new agent will be created.",
                    },
                ),
                "run_type": (run_types, {"default": run_types[0]}),
                "tools": ("TOOL_LIST", {"forceInput": True, "INPUT_IS_LIST": True}),
                "inputs": ("*",),
                "text": (
                    "STRING",
                    {"multiline": True, "dynamicPrompts": False},
                ),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, input_types):
        return True

    RETURN_TYPES = (
        any,
        "AGENT",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
    )
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent"

    def run(self, **kwargs):
        run_type = kwargs.get("run_type", run_types[0])
        inputs = kwargs.get("inputs", [])
        agent = kwargs.get("agent", None)
        tools = kwargs.get("tools", [])
        text = kwargs.get("text", None)

        create_dict = {}

        # Configuration
        if agent:
            config = agent.drivers_config
            create_dict["config"] = agent.drivers_config.prompt_driver

        # Tools
        create_dict["tools"] = self.tool_check(config, tools)

        if agent:
            create_dict["rulesets"] = agent.rulesets

        # Memory
        if agent:
            create_dict["conversation_memory"] = agent.conversation_memory
            create_dict["meta_memory"] = agent.meta_memory
            create_dict["task_memory"] = agent.task_memory

        prompt = []
        try:
            # Now create the agent
            self.agent = gtComfyAgent(**create_dict)

            # Check for inputs. If none, then just create the agent
            if len(inputs) == 0 and text.strip() == "":
                output = "Agent created."
            else:
                # Get the prompt text
                if len(inputs) == 0:
                    prompt = [text]
                else:
                    prompt = [text] + inputs

                if run_type == "Default":
                    result = self.agent.run(prompt)
                else:
                    if run_type == "Prompt" or (
                        run_type == "Tool(s)" and len(tools) == 0
                    ):
                        self.agent.add_task(PromptTask(prompt))
                    elif run_type == "Tool(s)":
                        if len(tools) == 1:
                            self.agent.add_task(ToolTask(prompt, tool=tools[0]))
                        else:
                            self.agent.add_task(ToolkitTask(prompt, tools=tools))
                    elif run_type == "Summarize":
                        self.agent.add_task(TextSummaryTask(prompt))
                    result = self.agent.run()
                output = result.output_task.output
            return (
                output,
                self.agent,
            )

        except OpenAIError as e:
            if "api_key" in str(e).lower():
                return (
                    "Error: OpenAI API key is missing. Please provide a valid API key.",
                    None,
                )
            else:
                return (f"OpenAI Error: {str(e)}", None)
        except Exception as e:
            return (f"Error creating agent: {str(e)}", None)
