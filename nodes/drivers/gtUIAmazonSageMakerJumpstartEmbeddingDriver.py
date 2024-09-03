from griptape.drivers import AmazonSageMakerJumpstartEmbeddingDriver

from ..config.gtUIAmazonBedrockSession import start_session
from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_model = ""
default_endpoint = "jumpstart-dft-..."
DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonSageMakerJumpstartEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "OpenAI Compatible Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)
        inputs["optional"].update(
            {
                "embedding_model": ("STRING", {"default": default_model}),
                "endpoint": ("STRING", {"default": default_endpoint}),
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", default_model)
        endpoint = kwargs.get("endpoint", default_endpoint)
        api_key = self.getenv(
            kwargs.get("aws_access_key_id_env_var", DEFAULT_AWS_ACCESS_KEY_ID)
        )
        secret_access_key = self.getenv(
            kwargs.get("aws_secret_access_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY)
        )
        region_name = self.getenv(
            kwargs.get("aws_default_region_env_var", DEFAULT_AWS_DEFAULT_REGION)
        )

        params = {
            "model": model,
            "endpoint": endpoint,
            "aws_access_key_id": api_key,
            "aws_secret_access_key": secret_access_key,
            "region_name": region_name,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        start_session(
            aws_access_key_id=params.get("aws_access_key_id", None),
            aws_secret_access_key=params.get("aws_secret_access_key", None),
            region_name=params.get("region_name", None),
        )
        params.pop("aws_access_key_id")
        params.pop("aws_secret_access_key")
        params.pop("region_name")
        driver = AmazonSageMakerJumpstartEmbeddingDriver(**params)
        return (driver,)
