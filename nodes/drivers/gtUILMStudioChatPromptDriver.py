from griptape.drivers import OpenAiChatPromptDriver

from .gtUIOpenAiCompatibleChatPromptDriver import gtUIOpenAiCompatibleChatPromptDriver

default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioChatPromptDriver(gtUIOpenAiCompatibleChatPromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["api_key_env_var"]

        inputs["optional"].update(
            {
                "model": ((), {}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
                "use_native_tools": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        params["base_url"] = f"{params['base_url']}:{kwargs['port']}/v1"

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
