from typing import Any, Tuple

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseWebSearchDriver(gtUIBaseDriver):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("WEB_SEARCH_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers/Web Search"

    def create(self, **kwargs) -> Tuple[Any, ...]:
        driver = None
        return (driver,)
