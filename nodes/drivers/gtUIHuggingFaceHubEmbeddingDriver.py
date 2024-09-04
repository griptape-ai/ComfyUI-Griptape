from griptape.drivers import HuggingFaceHubEmbeddingDriver
from griptape.tokenizers import HuggingFaceTokenizer

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_model = "sentence-transformers/all-MiniLM-L6-v2"
default_tokenizer = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_API_KEY_ENV_VAR = "HUGGINGFACE_HUB_ACCESS_TOKEN"


class gtUIHuggingFaceHubEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Hugging Face Hub Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_model": (
                    "STRING",
                    {"default": default_model},
                ),
                "tokenizer": ("STRING", {"default": default_tokenizer}),
                "max_output_tokens": ("INT", {"default": 512}),
                "api_token_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", default_model)
        api_key = self.getenv(kwargs.get("api_token_env_var", DEFAULT_API_KEY_ENV_VAR))
        tokenizer = kwargs.get("tokenizer", default_tokenizer)
        max_output_tokens = kwargs.get("max_output_tokens", 512)

        params = {
            "model": model,
            "api_token": api_key,
            "tokenizer": HuggingFaceTokenizer(
                model=tokenizer, max_output_tokens=max_output_tokens
            ),
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = HuggingFaceHubEmbeddingDriver(**params)
        except Exception as e:
            print(f"Error creating driver: {e}")

        return (driver,)
