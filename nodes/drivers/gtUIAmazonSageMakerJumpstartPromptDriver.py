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

        inputs["required"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "endpoint": ("STRING", {"default": default_endpoint}),
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
        # api_key = os.getenv("GOOGLE_API_KEY")
        model = kwargs.get("model", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        endpoint = kwargs.get("endpoint", default_endpoint)
        params = {}

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
        try:
            driver = AmazonSageMakerJumpstartPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
