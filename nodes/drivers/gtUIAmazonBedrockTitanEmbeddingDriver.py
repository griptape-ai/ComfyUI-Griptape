from griptape.drivers import AmazonBedrockTitanEmbeddingDriver

from ..config.gtUIAmazonBedrockSession import start_session
from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = [
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockTitanEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Amazon Bedrock Titan Embedding Driver"

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
                "embedding_model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Select the embedding model to use.",
                    },
                ),
                "aws_access_key_id_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_ACCESS_KEY_ID,
                        "tooltip": "Enter the name of the environment variable for your AWS_ACCESS_KEY_ID, not your actual key.",
                    },
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_SECRET_ACCESS_KEY,
                        "tooltip": "Enter the name of the environment variable for your AWS_SECRET_ACCESS_KEY, not your actual key.",
                    },
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_DEFAULT_REGION,
                        "tooltip": "Enter the name of the environment variable for your AWS_DEFAULT_REGION, not your actual region.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", None)
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
            "aws_access_key_id": api_key,
            "aws_secret_access_key": secret_access_key,
            "region_name": region_name,
        }

        if model:
            params["model"] = model
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

        driver = AmazonBedrockTitanEmbeddingDriver(**params)
        return (driver,)
