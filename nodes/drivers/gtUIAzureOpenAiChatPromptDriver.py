from griptape.drivers import AzureOpenAiChatPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
DEFAULT_AZURE_ENDPOINT_ENV_VAR = "AZURE_OPENAI_ENDPOINT"
DEFAULT_API_KEY_ENV_VAR = "AZURE_OPENAI_API_KEY"


class gtUIAzureOpenAiChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "deployment_name": ("STRING", {"default": models[0]}),
                "response_format": (["default", "json_object"], {"default": "default"}),
            }
        )
        inputs["optional"].update(
            {
                "endpoint_env_var": (
                    "STRING",
                    {"default": DEFAULT_AZURE_ENDPOINT_ENV_VAR},
                ),
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY_ENV_VAR}),
            }
        )

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        deployment_name = kwargs.get("deployment_name", None)
        response_format = kwargs.get("response_format", None)
        seed = kwargs.get("seed", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts_on_fail = kwargs.get("max_attempts_on_fail", None)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        azure_endpoint_env_var = kwargs.get(
            "endpoint_env_var", DEFAULT_AZURE_ENDPOINT_ENV_VAR
        )

        if api_key_env_var:
            api_key = self.getenv(api_key_env_var)
        if azure_endpoint_env_var:
            azure_endpoint = self.getenv("AZURE_OPENAI_ENDPOINT")

        params = {}

        if api_key:
            params["api_key"] = api_key
        if azure_endpoint:
            params["azure_endpoint"] = azure_endpoint
        if model:
            params["model"] = model
        if deployment_name:
            params["azure_deployment"] = deployment_name
        if not response_format == "default":
            params["response_format"] = response_format
        if seed:
            params["seed"] = seed
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts_on_fail:
            params["max_attempts"] = max_attempts_on_fail

        try:
            driver = AzureOpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
