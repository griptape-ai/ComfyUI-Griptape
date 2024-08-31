from griptape.drivers import BaseRerankDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseRerankDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Rerank Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update()

        return inputs

    CATEGORY = "Griptape/Agent Drivers/Rerank"

    RETURN_TYPES = ("RERANK_DRIVER",)

    def create(self, **kwargs):
        driver = BaseRerankDriver()
        return (driver,)
