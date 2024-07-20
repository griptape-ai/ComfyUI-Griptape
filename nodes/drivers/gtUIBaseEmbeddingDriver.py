from griptape.drivers import BaseEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update()

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    RETURN_TYPES = ("EMBEDDING_DRIVER",)

    def create(self, **kwargs):
        driver = BaseEmbeddingDriver()
        return (driver,)
