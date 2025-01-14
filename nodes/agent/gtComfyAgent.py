from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import DriversConfig, OpenAiDriversConfig
from griptape.drivers import GooglePromptDriver
from griptape.structures import Agent
from griptape.tools import QueryTool

from ...py.griptape_settings import GriptapeSettings
from ..patches.gemini_query_tool import GeminiQueryTool

default_prompt = "{{ input_string }}"

load_dotenv()


class gtComfyAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Extract drivers_config from kwargs if it exists
        drivers_config = kwargs.pop("drivers_config", None)

        if drivers_config is None:
            # Get the default config
            settings = GriptapeSettings()
            agent_config = settings.get_settings_key("default_config")
            try:
                if agent_config:
                    Defaults.drivers_config = DriversConfig.from_dict(agent_config)
                    kwargs["prompt_driver"] = Defaults.drivers_config.prompt_driver
                else:
                    # Set the default config
                    settings = GriptapeSettings()
                    api_key = settings.get_settings_key_or_use_env("OPENAI_API_KEY")
                    Defaults.drivers_config = OpenAiDriversConfig()
                    Defaults.drivers_config.prompt_driver.api_key = api_key
                    Defaults.drivers_config.embedding_driver.api_key = api_key
                    Defaults.drivers_config.text_to_speech_driver.api_key = api_key
                    Defaults.drivers_config.audio_transcription_driver.api_key = api_key
                    Defaults.drivers_config.image_generation_driver.api_key = api_key
            except Exception:
                print(
                    "Warning - default agent settings are corrupted.\nSetting default to OpenAIDriversConfig"
                )
                Defaults.drivers_config = OpenAiDriversConfig()
                settings.overwrite_settings_key("Griptape.default_config", None)
                settings.save_settings()

        else:
            Defaults.drivers_config = drivers_config

        if "prompt_driver" in kwargs:
            Defaults.drivers_config.prompt_driver = kwargs["prompt_driver"]

        if "tools" in kwargs:
            self._fix_google_query_tool(
                Defaults.drivers_config.prompt_driver, kwargs["tools"]
            )
        # Initialize the parent class
        super().__init__(*args, **kwargs)

        # Add any additional initialization here
        self.drivers_config = Defaults.drivers_config

    def _fix_google_query_tool(self, prompt_driver, tools):
        # Check and see if any of the tools have been set to off_prompt
        off_prompt = False
        return_tools = tools
        for tool in tools:
            if tool.off_prompt and not off_prompt:
                off_prompt = True
        if off_prompt:
            for x, tool in enumerate(tools):
                if isinstance(tool, QueryTool):
                    # Check and see if the prompt driver is a GooglePromptDriver
                    print(f"Prompt Driver: {prompt_driver}")
                    if isinstance(prompt_driver, GooglePromptDriver):
                        tools[x] = GeminiQueryTool()
        return return_tools

    def set_default_config(self):
        # agent_config = get_config("agent_config")
        settings = GriptapeSettings()
        agent_config = settings.get_settings_key("default_config")
        if agent_config:
            config = DriversConfig.from_dict(agent_config)
            new_agent = self.update_config(config)
            self = new_agent
        else:
            config = OpenAiDriversConfig()

    def model_check(self):
        # There are certain models that can't handle Tools well.
        # If this agent is using one of those models AND they have tools supplied, we'll
        # warn the user.
        simple_models = ["llama3", "llama3:latest", "mistral", "LLama-3"]
        drivers = ["OllamaPromptDriver", "LMStudioPromptDriver"]
        agent_prompt_driver_name = self.prompt_driver.__class__.__name__
        model = self.prompt_driver.model
        if agent_prompt_driver_name in drivers:
            if model == "":
                return (model, True)

            # Convert model and simple_models to lowercase for case-insensitive comparison
            model_lower = model.lower()
            simple_models_lower = [m.lower() for m in simple_models]

            # Check for exact match
            if model_lower in simple_models_lower:
                if len(self.tools) > 0:
                    return (model, True)

        return (model, False)

    def model_response(self, model):
        if model == "":
            return "You have provided a blank model for the Agent Configuration.\n\nPlease specify a model configuration, or disconnect it from the agent."
        else:
            return f"This Agent Configuration Model: **{ self.prompt_driver.model }** may run into issues using tools.\n\nPlease consider using a different configuration, a different model, or removing tools from the agent and use the **Griptape Run: Tool Task** node for specific tool use."

    def update_agent(
        self,
        # config=None,
        tools=None,
        rulesets=None,
        conversation_memory=None,
        meta_memory=None,
        task_memory=None,
        prompt_driver=None,
    ):
        update_dict = {
            # "config": config or self.config,
            "prompt_driver": prompt_driver or self.prompt_driver,
            "tools": tools or self.tools,
            "rulesets": rulesets or self.rulesets,
            "conversation_memory": conversation_memory or self.conversation_memory,
            "meta_memory": meta_memory or self.meta_memory,
            "task_memory": task_memory or self.task_memory,
        }
        new_agent = gtComfyAgent(**update_dict)
        return new_agent

    def update_config(self, config):
        tools = self.tools
        rulesets = self.rulesets
        conversation_memory = self.conversation_memory
        prompt_driver = self.prompt_driver
        new_agent = gtComfyAgent(
            drivers_config=config,
            prompt_driver=prompt_driver,
            tools=tools,
            rulesets=rulesets,
            conversation_memory=conversation_memory,
        )

        return new_agent
