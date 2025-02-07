# pyright: reportMissingImports=false

import logging

from comfy.comfy_types import IO
from comfy_execution.graph import ExecutionBlocker
from griptape.drivers import DummyVectorStoreDriver
from griptape.tools import QueryTool, RagTool, VectorStoreTool
from openai import OpenAIError

from ...py.griptape_settings import GriptapeSettings
from ..utilities import stream_run

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
                    IO.STRING,
                    {
                        "forceInput": True,
                        # "dynamicPrompts": True,
                        "tooltip": "Additional text be appended to the STRING with a newline character.",
                    },
                ),
                "STRING": (
                    IO.STRING,
                    {
                        "multiline": True,
                        # "dynamicPrompts": True,
                        "tooltip": "The prompt text.",
                    },
                ),
                "max_subtasks": (
                    "INT",
                    {
                        "default": 3,
                        "tooltip": "The maximum number of subtasks to run when an Agent uses a Tool",
                    },
                ),
                "output_stream": (
                    "MARKDOWN",
                    {
                        "multiline": True,
                        "tooltip": "The output stream from the agent.",
                        "placeholder": "The output stream from the agent.",
                    },
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
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

    def _get_max_subtask_result(self, result_value, max_subtasks):
        if "Exceeded tool limit" in result_value:
            print("Exceeded tool limit")
            last_valid_input = self.agent.tasks[0].subtasks[-2].input.value[0].value
            last_valid_response = self.agent.tasks[0].subtasks[-2].output
            result_value = (
                f"[Conversation limit of {max_subtasks} reached.]\n"
                f"The agent had to stop before reaching the requested back-and-forth.\n"
                f"Here’s the last valid action and response:\n\n"
                f"[Action]: {last_valid_input}\n\n"
                f"[Response]: {last_valid_response}"
            )
        return result_value

    def run(self, **kwargs):
        STRING = kwargs.get("STRING", "")
        config = kwargs.get("config", None)
        agent = kwargs.get("agent", None)
        tools = kwargs.get("tools", [])
        rulesets = kwargs.get("rulesets", [])
        input_string = kwargs.get("input_string", None)
        max_subtasks = kwargs.get("max_subtasks", 2)
        node_id = kwargs.get("unique_id", None)
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

            # Set the maximum subtasks
            if max_subtasks > 1:
                self.agent.tasks[0].max_subtasks = max_subtasks

            # Check for inputs. If none, then just create the agent
            if not input_string and STRING == "":
                output_string = "Agent created."
            else:
                # Get the prompt text
                if not input_string:
                    prompt_text = STRING
                else:
                    prompt_text = STRING + "\n\n" + input_string

                stream_run(
                    agent=self.agent,
                    prompt_text=prompt_text,
                    node_id=node_id,
                    widget_name="output_stream",
                )
                # if True:
                #     output_string = ""
                #     for artifact in Stream(self.agent).run(prompt_text):
                #         output_string += artifact.value
                #         PromptServer.instance.send_sync(
                #             "griptape.stream_agent_run",
                #             {
                #                 "text_context": output_string,
                #                 "id": node_id,
                #                 "widget": "output_stream",
                #             },
                #         )

                # else:
                #     result = self.agent.run(prompt_text)
                #     output_string = self._get_max_subtask_result(
                #         result.output_task.output.value, max_subtasks
                #     )
                output_string = self.agent.output_task.output.value
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
