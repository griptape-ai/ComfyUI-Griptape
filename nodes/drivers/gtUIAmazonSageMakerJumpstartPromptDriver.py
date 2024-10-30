import boto3
from griptape.drivers import AmazonSageMakerJumpstartPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_model = "meta-llama/Meta-Llama-3-8B-Instruct"
default_endpoint = "jumpstart-dft-..."
DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonSageMakerJumpstartPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": (
                    "STRING",
                    {
                        "default": default_model,
                        "tooltip": "Specify the model to use. Default is Meta-Llama-3-8B-Instruct.",
                    },
                ),
                "endpoint": (
                    "STRING",
                    {
                        "default": default_endpoint,
                        "tooltip": "Specify the SageMaker endpoint to use.",
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

    FUNCTION = "create"

    def create(self, **kwargs):
        # api_key = os.getenv("GOOGLE_API_KEY")
        model = kwargs.get("model", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        endpoint = kwargs.get("endpoint", default_endpoint)
        region_name = kwargs.get("region_name", DEFAULT_AWS_DEFAULT_REGION)
        secret_key_env_var = kwargs.get(
            "secret_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY
        )
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_AWS_ACCESS_KEY_ID)

        use_native_tools = kwargs.get("use_native_tools", False)
        params = {}
        # Create a boto3 session
        try:
            boto3.Session(
                aws_access_key_id=self.getenv(api_key_env_var),
                aws_secret_access_key=self.getenv(secret_key_env_var),
                region_name=self.getenv(region_name),
            )
        except Exception as e:
            print(f"Failed to create session: {e}")

        # if api_key:
        #     params["api_key"] = api_key
        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if endpoint:
            params["endpoint"] = endpoint
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        try:
            driver = AmazonSageMakerJumpstartPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
