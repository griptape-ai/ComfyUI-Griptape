from griptape.drivers import OpenAiEmbeddingDriver

from .gtUIOpenAiCompatibleEmbeddingDriver import gtUIOpenAiCompatibleEmbeddingDriver

default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioEmbeddingDriver(gtUIOpenAiCompatibleEmbeddingDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["api_key_env_var"]

        inputs["optional"].update(
            {
                "embedding_model": ((), {}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
                "use_native_tools": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model")
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port")
        api_key = kwargs.get("api_key")

        params = {
            "model": model,
            "base_url": f"{base_url}:{port}/v1/embeddings",
            "api_key": api_key,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        try:
            driver = OpenAiEmbeddingDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
