from typing import Any, Tuple

from griptape.drivers import DummyEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Embedding Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update()

        return inputs

    CATEGORY = "Griptape/Agent Drivers/Embedding"

    RETURN_TYPES = ("EMBEDDING_DRIVER",)

    def create(self, **kwargs) -> Tuple[Any, ...]:
        driver = DummyEmbeddingDriver()
        return (driver,)
