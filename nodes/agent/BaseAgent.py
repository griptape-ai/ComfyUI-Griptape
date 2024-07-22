from griptape.drivers import DummyVectorStoreDriver
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import TaskMemoryClient, VectorStoreClient
from openai import OpenAIError

# from server import PromptServer
from ...py.griptape_config import get_config
from .gtComfyAgent import gtComfyAgent

default_prompt = "{{ input_string }}"
max_attempts_default = 10


def get_default_config():
    return get_config("agent_config")


class BaseAgent:
    """
    Create a Griptape Agent
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
                    },
                ),
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                    },
                ),
                "tools": ("TOOL_LIST", {"forceInput": True, "INPUT_IS_LIST": True}),
                "rulesets": ("RULESET", {"forceInput": True}),
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                        "dynamicPrompts": True,
                    },
                ),
                "STRING": (
                    "STRING",
                    {"multiline": True, "dynamicPrompts": True},
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "AGENT",
    )
    RETURN_NAMES = (
        "OUTPUT",
        "AGENT",
    )
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent"

    def tool_check(self, config, tools):
        tool_list = []
        if len(tools) > 0:
            # Check and see if any of the tools are VectorStoreClients
            for tool in tools:
                if isinstance(tool, VectorStoreClient):
                    # Check and see if the driver is a DummyVectorStoreDriver
                    # If it is, replace it with the agent's vector store driver
                    if isinstance(tool.vector_store_driver, DummyVectorStoreDriver):
                        vector_store_driver = config.vector_store_driver
                        try:
                            # set the tool's vector store driver to the agent's vector store driver
                            tool.vector_store_driver = vector_store_driver
                        except Exception as e:
                            print(f"Error: {str(e)}")
            # Check and see if any of the tools have been set to off_prompt
            off_prompt = False
            for tool in tools:
                if tool.off_prompt and not off_prompt:
                    off_prompt = True
            if off_prompt:
                taskMemoryClient = False
                # check and see if TaskMemoryClient is in tools
                for tool in tools:
                    if isinstance(tool, TaskMemoryClient):
                        taskMemoryClient = True
                if not taskMemoryClient:
                    tools.append(TaskMemoryClient(off_prompt=False))
            tool_list = tools
        return tool_list

    def run(self, **kwargs):
        STRING = kwargs.get("STRING", "")
        config = kwargs.get("config", None)
        agent = kwargs.get("agent", None)
        tools = kwargs.get("tools", [])
        rulesets = kwargs.get("rulesets", [])
        input_string = kwargs.get("input_string", None)

        create_dict = {}

        # Configuration
        if config:
            create_dict["config"] = config
        elif agent:
            create_dict["config"] = agent.config

        # Tools
        create_dict["tools"] = self.tool_check(create_dict["config"], tools)

        # Rulesets
        if len(rulesets) > 0:
            create_dict["rulesets"] = rulesets
        elif agent:
            create_dict["rulesets"] = agent.rulesets

        # Memory
        if agent:
            create_dict["conversation_memory"] = agent.conversation_memory
            create_dict["meta_memory"] = agent.meta_memory
            create_dict["task_memory"] = agent.task_memory

        try:
            # Now create the agent
            self.agent = gtComfyAgent(**create_dict)

            # Warn for models
            model, simple_model = self.agent.model_check()
            if simple_model:
                return (self.agent.model_response(model), self.agent)

            # Check for inputs. If none, then just create the agent
            if not input_string and STRING == "":
                output_string = "Agent created."
            else:
                # Get the prompt text
                if not input_string:
                    prompt_text = STRING
                else:
                    prompt_text = STRING + "\n\n" + input_string

                # # Start to think about sending update messages
                # PromptServer.instance.send_sync(
                #     "comfy.gtUI.textmessage",
                #     {"message": f"Created agent with prompt: {prompt_text}"},
                # )

                if len(tools) > 0:
                    self.agent.add_task(ToolkitTask(prompt_text, tools=tools))
                else:
                    self.agent.add_task(PromptTask(prompt_text))
                result = self.agent.run()
                output_string = result.output_task.output.value
            return (
                output_string,
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
