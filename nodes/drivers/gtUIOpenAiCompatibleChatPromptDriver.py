from griptape.drivers import OpenAiChatPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_model = "gpt-4o"
default_base_url = "https://api.openai.com/v1"
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"


class gtUIOpenAiCompatibleChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "base_url": ("STRING", {"default": default_base_url}),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY_ENV}),
                "use_native_tools": ("BOOLEAN", {"default": False}),
            }
        )

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {}

        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if base_url:
            params["base_url"] = base_url
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
