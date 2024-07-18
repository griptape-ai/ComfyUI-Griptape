import os

from griptape.drivers import HuggingFaceHubEmbeddingDriver
from griptape.tokenizers import HuggingFaceTokenizer

from .BaseDriver import gtUIBaseDriver

default_model = "sentence-transformers/all-MiniLM-L6-v2"
default_tokenizer = "sentence-transformers/all-MiniLM-L6-v2"


class gtUIHuggingFaceHubEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Hugging Face Hub Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": (
                    "STRING",
                    {"default": default_model},
                ),
                "tokenizer": ("STRING", {"default": default_tokenizer}),
                "max_output_tokens": ("INT", {"default": 512}),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", default_model)
        api_key = os.getenv("HUGGINGFACE_HUB_ACCESS_TOKEN")
        tokenizer = kwargs.get("tokenizer", default_tokenizer)
        max_output_tokens = kwargs.get("max_output_tokens", 512)

        params = {}

        if model:
            params["model"] = model
        if tokenizer:
            params["tokenizer"] = HuggingFaceTokenizer(
                model=tokenizer, max_output_tokens=max_output_tokens
            )
        if api_key:
            params["api_token"] = api_key

        driver = HuggingFaceHubEmbeddingDriver(**params)
        return (driver,)
