from griptape.drivers import BaseImageQueryDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseImageQueryDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Image Query Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update()

        return inputs

    CATEGORY = "Griptape/Drivers/Image Query"

    def create(self, **kwargs):
        driver = BaseImageQueryDriver()
        return (driver,)
