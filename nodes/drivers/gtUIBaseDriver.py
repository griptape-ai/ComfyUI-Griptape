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
        api_key = settings.get_settings_key_or_use_env(env)
        return api_key

    def create(self, **kwargs):
        driver = DummyPromptDriver()
        return (driver,)
