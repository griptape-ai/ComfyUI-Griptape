from griptape.drivers import (
    AmazonOpenSearchVectorStoreDriver,
)

from ..config.gtUIAmazonBedrockSession import start_session
from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_HOST_ENV = "AMAZON_OPENSEARCH_HOST"
DEFAULT_INDEX_ENV = "AMAZON_OPENSEARCH_INDEX_NAME"
DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonOpenSearchVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Open Search Vector Store Driver: https://aws.amazon.com/opensearch-service/"

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
                "host_env": ("STRING", {"default": DEFAULT_HOST_ENV}),
                "index_env": ("STRING", {"default": DEFAULT_INDEX_ENV}),
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
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = self.getenv(kwargs.get("host_env", DEFAULT_HOST_ENV))
        index_env_var = self.getenv(kwargs.get("index_name_env", DEFAULT_INDEX_ENV))
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
            "host": host_env,
            "index_name": index_env_var,
            "aws_access_key_id": api_key,
            "aws_secret_access_key": secret_access_key,
            "region_name": region_name,
        }

        if not embedding_driver:
            params["embedding_driver"] = self.get_default_embedding_driver()
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
        driver = AmazonOpenSearchVectorStoreDriver(**params)
        return (driver,)
