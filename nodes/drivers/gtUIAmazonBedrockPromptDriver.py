import boto3
from griptape.drivers import AmazonBedrockPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
            }
        )
        inputs["optional"].update(
            {
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

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        aws_region = kwargs.get("aws_region", DEFAULT_AWS_DEFAULT_REGION)
        secret_key_env_var = kwargs.get(
            "secret_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY
        )
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_AWS_ACCESS_KEY_ID)
        max_tokens = kwargs.get("max_tokens", 0)

        params = {}

        # Create a boto3 session
        try:
            boto3.Session(
                aws_access_key_id=self.getenv(api_key_env_var),
                aws_secret_access_key=self.getenv(secret_key_env_var),
                region_name=self.getenv(aws_region),
            )
        except Exception as e:
            print(f"Failed to create session: {e}")
        if model:
            params["model"] = model
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        # if session:
        #     params["session"] = session
        if use_native_tools:
            params["use_native_tools"] = use_native_tools

        try:
            driver = AmazonBedrockPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
