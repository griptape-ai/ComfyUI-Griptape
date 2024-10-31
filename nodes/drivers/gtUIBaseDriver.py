import os

from griptape.drivers import DummyPromptDriver

from ...py.griptape_settings import GriptapeSettings


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
        settings = GriptapeSettings()
        settings.setup()
        api_key = settings.get_settings_key(f"Griptape.{env}")
        if not api_key:
            api_key = os.getenv(env, None)
        if not api_key:
            raise ValueError(f"Environment variable {env} is not set")
        return api_key

    def create(self, **kwargs):
        driver = DummyPromptDriver()
        return (driver,)
