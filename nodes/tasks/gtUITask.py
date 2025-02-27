from griptape.artifacts import TextArtifact
from griptape.drivers.prompt.google import GooglePromptDriver
from griptape.drivers.vector.dummy import DummyVectorStoreDriver
from griptape.tasks import PromptTask, ToolkitTask, ToolTask
from griptape.tools import QueryTool, VectorStoreTool

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..patches.gemini_query_tool import GeminiQueryTool
from .gtUIBaseTask import gtUIBaseTask


class gtUITask(gtUIBaseTask):
    DESCRIPTION = "Create a task for an agent."
    CATEGORY = "Griptape/Agent"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tools": ("TOOL_LIST",),
            }
        )
        return inputs

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
                    if isinstance(config.prompt_driver, GooglePromptDriver):
                        tools.append(GeminiQueryTool())
                    else:
                        tools.append(QueryTool(off_prompt=False))
            tool_list = tools
        return tool_list

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        tools = kwargs.get("tools", [])
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        context = kwargs.get("key_value_replacement", None)
        prompt_text = self.get_prompt_text(STRING, input_string)

        if prompt_text.strip() == "":
            return ("No prompt provided", agent)

        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        model, simple_model = agent.model_check()
        if simple_model:
            response = agent.model_response(model)
            return (response, agent)
        if len(tools) == 0:
            task = PromptTask(prompt_text)
        else:
            tools = self.tool_check(agent.drivers_config, tools)
            if len(tools) == 1:
                task = ToolTask(prompt_text, tool=tools[0])
            else:
                task = ToolkitTask(
                    prompt_text,
                    tools=tools,
                )
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        if context:
            agent.tasks[0].context = self.get_context_as_dict(context)
        result = agent.run()
        output = result.output_task.output.value
        if isinstance(output, str):
            return (output, agent)
        elif isinstance(output, list):
            output_list = [item.value for item in output]
            output_str = "\n\n".join(output_list)
            return (output_str, agent)
        elif isinstance(output, TextArtifact):
            return (output.value, agent)
