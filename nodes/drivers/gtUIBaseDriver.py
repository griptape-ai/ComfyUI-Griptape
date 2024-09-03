import os

from griptape.drivers import DummyPromptDriver


class gtUIBaseDriver:
    DESCRIPTION = "Griptape Driver"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers"

    def getenv(self, env):
        return os.getenv(env, None)

    def create(self, **kwargs):
        driver = DummyPromptDriver()
        return (driver,)
