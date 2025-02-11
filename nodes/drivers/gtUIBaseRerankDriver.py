from typing import Any, Tuple

from griptape.drivers.rerank.local import LocalRerankDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseRerankDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Rerank Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update()

        return inputs

    CATEGORY = "Griptape/Agent Drivers/Rerank"

    RETURN_TYPES = ("RERANK_DRIVER",)

    def create(self, **kwargs) -> Tuple[Any, ...]:
        driver = LocalRerankDriver()
        return (driver,)
