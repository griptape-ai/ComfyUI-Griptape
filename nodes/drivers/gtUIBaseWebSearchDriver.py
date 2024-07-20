from griptape.drivers import BaseWebSearchDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseWebSearchDriver(gtUIBaseDriver):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("WEB_SEARCH_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Web Search"

    def create(
        self,
    ):
        driver = BaseWebSearchDriver()
        return (driver,)
