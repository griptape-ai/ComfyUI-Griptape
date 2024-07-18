import os

from griptape.drivers import AzureOpenAiImageQueryDriver

from .gtUIBaseImageQueryDriver import gtUIBaseImageQueryDriver

models = [
    "gpt-4o",
    "gpt-4-vision-preview",
]

default_api_key_env = "AZURE_OPENAI_API_KEY"
default_azure_endpoint_env_var = "AZURE_OPENAI_ENDPOINT"


class gtUIAzureOpenAiImageQueryDriver(gtUIBaseImageQueryDriver):
    DESCRIPTION = "Griptape Azure OpenAI Image Query Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "deployment_name": ("STRING", {"default": models[0]}),
                "endpoint_env_var": (
                    "STRING",
                    {"default": default_azure_endpoint_env_var},
                ),
                "api_key_env_var": ("STRING", {"default": default_api_key_env}),
            }
        )
        inputs["optional"].update({})

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env)
        endpoint_env_var = kwargs.get(
            "endpoint_env_var", default_azure_endpoint_env_var
        )
        deployment_name = kwargs.get("deployment_name", models[0])
        model = kwargs.get("model", models[0])

        params = {}

        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        if model:
            params["model"] = model
        if endpoint_env_var:
            params["azure_endpoint"] = os.getenv(endpoint_env_var)
        if deployment_name:
            params["azure_deployment"] = deployment_name

        try:
            driver = AzureOpenAiImageQueryDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None,)
