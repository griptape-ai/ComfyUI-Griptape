from griptape.drivers.prompt.amazon_bedrock import AmazonBedrockPromptDriver

from ..config.gtUIAmazonBedrockSession import start_session
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
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)

        # Set model default
        inputs["optional"]["model"] = (models, {"default": models[0]})
        inputs["optional"].update(
            {
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
                "max_tokens": (
                    "INT",
                    {
                        "default": 100,
                        "tooltip": "Maximum tokens to generate. Amazon Bedrock tends to fail if this isn't given.",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        region_name = kwargs.get("region_name", DEFAULT_AWS_DEFAULT_REGION)
        max_tokens = kwargs.get(
            "max_tokens", 100
        )  # Default max_tokens has to be passed
        secret_access_key = self.getenv(
            kwargs.get("secret_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY)
        )
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_AWS_ACCESS_KEY_ID))

        params = {}

        if model:
            params["model"] = model
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        if region_name:
            params["region_name"] = region_name
        if secret_access_key:
            params["aws_secret_access_key"] = secret_access_key
        if api_key:
            params["aws_access_key_id"] = api_key
        params["min_p"] = kwargs.get("min_p", 0.1)
        params["top_k"] = kwargs.get("top_k", 40)
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

        try:
            driver = AmazonBedrockPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
