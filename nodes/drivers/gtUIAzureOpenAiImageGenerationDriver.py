import os

from griptape.drivers import (
    AzureOpenAiImageGenerationDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

models = ["dall-e-3", "dall-e-2"]
sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]
azure_endpoint_env_var = "AZURE_OPENAI_DALL_E_3_ENDPOINT"
default_api_key_env_var = "AZURE_OPENAI_DALL_E_3_API_KEY"


class gtUIAzureOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Azire OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "deployment_name": ("STRING", {"default": models[0]}),
                "endpoint_env_var": ("STRING", {"default": azure_endpoint_env_var}),
                "api_key_env_var": ("STRING", {"default": default_api_key_env_var}),
                "size": (sizes, {"default": sizes[2]}),
            }
        )
        return inputs

    def adjust_size_based_on_model(self, model, size):
        # pick the approprite size based on the model
        if model == "dall-e-2":
            if size in ["1024x1792", "1792x1024"]:
                size = "1024x1024"
        if model == "dall-e-3":
            if size in ["256x256", "512x512"]:
                size = "1024x1024"
        return size

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])
        deployment_name = kwargs.get("deployment_name", None)
        azure_deployment_env_var = kwargs.get(
            "endpoint_env_var", azure_endpoint_env_var
        )
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env_var)

        size = kwargs.get("size", sizes[2])
        size = self.adjust_size_based_on_model(model, size)

        api_key = os.getenv(api_key_env_var)
        azure_endpoint = os.getenv(azure_deployment_env_var)

        params = {}
        if model:
            params["model"] = model
        # if size:
        #     params["size"] = size
        if api_key:
            params["api_key"] = api_key
        if azure_endpoint:
            params["azure_endpoint"] = azure_endpoint
        if deployment_name:
            params["azure_deployment"] = deployment_name

        driver = AzureOpenAiImageGenerationDriver(**params)
        return (driver,)
