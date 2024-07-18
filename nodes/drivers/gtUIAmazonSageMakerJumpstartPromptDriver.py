from griptape.drivers import AmazonSageMakerJumpstartPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_model = "meta-llama/Meta-Llama-3-8B-Instruct"
default_endpoint = "jumpstart-dft-..."


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
        inputs["optional"].update({})

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Prompt"

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
