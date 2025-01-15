# pyright: reportMissingImports=false

import logging

from comfy_execution.graph import ExecutionBlocker
from griptape.drivers import DummyVectorStoreDriver
from griptape.tools import QueryTool, RagTool, VectorStoreTool
from openai import OpenAIError

from ...py.griptape_settings import GriptapeSettings

# from server import PromptServer
from .gtComfyAgent import gtComfyAgent

default_prompt = "{{ input_string }}"
max_attempts_default = 10


def get_default_config():
    settings = GriptapeSettings()
    return settings.get_settings_key("default_config")


class BaseAgent:
    """
    Create a Griptape Agent
    """

    def __init__(self):
        self.default_prompt = default_prompt
        self.agent = None

    @classmethod
    def INPUT_TYPES(cls):
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
                "config": (
                    "CONFIG",
                    {
                        "forceInput": True,
                        "tooltip": "The configuration for the agent. If not provided, the default configuration will be used.",
                    },
                ),
                "tools": (
                    "TOOL_LIST",
                    {
                        "forceInput": True,
                        "INPUT_IS_LIST": True,
                        "tooltip": "One or more tools to use with the agent.",
                    },
                ),
                "rulesets": (
                    "RULESET",
                    {
                        "forceInput": True,
                        "tooltip": "One or more rules to use with the agent.\nUse these to control the agent behavior.",
                    },
                ),
                "input_string": (
                    "STRING",
                    {
                        "forceInput": True,
                        # "dynamicPrompts": True,
                        "tooltip": "Additional text be appended to the STRING with a newline character.",
                    },
                ),
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                        # "dynamicPrompts": True,
                        "tooltip": "The prompt text.",
                    },
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
    OUTPUT_TOOLTIPS = (
        "Text response from the Agent",
        "The Agent. Can be connected to other nodes.",
    )
    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Griptape/Agent"

    def rag_tool_ruleset(self, tools):
        for tool in tools:
            # Check and see if any of the tools are RAGTools
            if isinstance(tool, RagTool):
                # See if there's an additional attribute on the RagTool
                if hasattr(tool, "use_rules"):
                    # if it's true, get the ruleset
                    if getattr(tool, "use_rules", False):
                        ruleset = getattr(tool, "ruleset", None)
                        return ruleset
        return None

    def tool_check(self, config, tools):
        tool_list = []
        if len(tools) > 0:
            # Logic per tool
            for tool in tools:
                # Check and see if any of the tools are VectorStoreTools
                if isinstance(tool, VectorStoreTool):
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
                # check and see if QueryTool is in tools
                for tool in tools:
                    if isinstance(tool, QueryTool):
                        taskMemoryClient = True
                if not taskMemoryClient:
                    tools.append(QueryTool(off_prompt=False))
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
            # Defaults.drivers_config = config
            create_dict["prompt_driver"] = config.prompt_driver
            create_dict["drivers_config"] = config
        elif agent:
            create_dict["prompt_driver"] = agent.prompt_driver
            create_dict["drivers_config"] = agent.drivers_config
        # Tools
        create_dict["tools"] = self.tool_check(config, tools)

        # add a ruleset to handle RAGTools if it's on.
        rulesets.append(self.rag_tool_ruleset(tools))
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
            if create_dict["rulesets"] == [None]:
                create_dict["rulesets"] = []
            # Now create the agent
            self.agent = gtComfyAgent(**create_dict)

            # Warn for models
            model, simple_model = self.agent.model_check()
            if model == "":
                error_msg = "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent."
                logging.error(error_msg)
                raise Exception(error_msg)
                return (
                    ExecutionBlocker(error_msg),
                    self.agent,
                )
            if simple_model:
                print(f"This is a simple model: {model}")
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

                result = self.agent.run(prompt_text)
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
