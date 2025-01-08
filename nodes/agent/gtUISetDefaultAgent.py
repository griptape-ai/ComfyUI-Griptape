from ...py.griptape_settings import GriptapeSettings
from .BaseAgent import BaseAgent


class gtUISetDefaultAgent(BaseAgent):
    DESCRIPTION = "Set the default agent."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["tools"]
        del inputs["optional"]["rulesets"]
        del inputs["optional"]["agent"]
        del inputs["optional"]["input_string"]
        del inputs["optional"]["STRING"]
        return inputs

    RETURN_TYPES = ("CONFIG",)
    OUTPUT_NODE = True

    def run(self, **kwargs):
        settings = GriptapeSettings()
        config = kwargs.get("config", None)
        if config:
            config_dict = config.to_dict()
            # grab the API keys as well
            for key in config_dict.keys():
                driver_type = f"_{key}"
                driver = getattr(config, driver_type, None)
                if driver:
                    if hasattr(driver, "api_key"):
                        api_key = driver.api_key
                        config_dict[key]["api_key"] = api_key

            settings.overwrite_settings_key("Griptape.default_config", config_dict)
            settings.save_settings()
        else:
            settings.overwrite_settings_key("Griptape.default_config", None)
            settings.save_settings()
        return (config,)
