from griptape.drivers import AmazonSageMakerJumpstartEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

default_model = ""
default_endpoint = "jumpstart-dft-..."


class gtUIAmazonSageMakerJumpstartEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "OpenAI Compatable Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "endpoint": ("STRING", {"default": default_endpoint}),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", default_model)
        endpoint = kwargs.get("endpoint", default_endpoint)

        params = {}

        if model:
            params["model"] = model
        if endpoint:
            params["endopoint"] = endpoint
        driver = AmazonSageMakerJumpstartEmbeddingDriver(**params)
        return (driver,)
