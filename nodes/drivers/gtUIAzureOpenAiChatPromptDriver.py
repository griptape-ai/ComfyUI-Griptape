from griptape.drivers.prompt.azure_openai_chat_prompt_driver import (
    AzureOpenAiChatPromptDriver,
)

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]

DEFAULT_AZURE_ENDPOINT_ENV_VAR = "AZURE_OPENAI_ENDPOINT"
DEFAULT_API_KEY_ENV_VAR = "AZURE_OPENAI_API_KEY"


class gtUIAzureOpenAiChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Clear the required and optional inputs
        inputs["required"] = {}
        inputs["optional"] = {}

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)
        inputs["optional"].update(
            {
                "model": (models, {"default": models[0]}),
                "deployment_name": ("STRING", {"default": models[0]}),
                "response_format": (["default", "json_object"], {"default": "default"}),
                "endpoint_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AZURE_ENDPOINT_ENV_VAR,
                        "tooltip": "Enter the name of the environment variable for AZURE_OPENAI_ENDPOINT, not the actual endpoint.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Enter the name of the environment variable for AZURE_OPENAI_API_KEY, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        deployment_name = kwargs.get("deployment_name", None)
        response_format = kwargs.get("response_format", None)
        seed = kwargs.get("seed", None)
        temperature = kwargs.get("temperature", None)
        max_attempts_on_fail = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        api_key_env_var = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        azure_endpoint_env_var = self.getenv(
            kwargs.get("endpoint_env_var", DEFAULT_AZURE_ENDPOINT_ENV_VAR)
        )

        params = {
            "api_key": api_key_env_var,
            "azure_endpoint": azure_endpoint_env_var,
            "model": model,
            "azure_deployment": deployment_name,
            "seed": seed,
            "temperature": temperature,
            "max_attempts": max_attempts_on_fail,
            "use_native_tools": use_native_tools,
        }
        if response_format == "json_object":
            response_format = {"type": "json_object"}
            params["response_format"] = response_format

        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = AzureOpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
