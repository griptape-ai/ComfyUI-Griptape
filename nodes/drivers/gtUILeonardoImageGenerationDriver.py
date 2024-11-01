from griptape.drivers import (
    LeonardoImageGenerationDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_API_KEY_ENV_VAR = "LEONARDO_API_KEY"

leonardo_models = [
    {
        "name": "default",
        "model": "1e60896f-3c26-4296-8ecc-53e2afecc132",
        "url": "https://app.leonardo.ai/models/1e60896f-3c26-4296-8ecc-53e2afecc132",
    },
    {
        "name": "Leonardo Anime XL",
        "model": "e71a1c2f-4f80-4800-934f-2c68979d8cc8",
        "url": "https://app.leonardo.ai/models/e71a1c2f-4f80-4800-934f-2c68979d8cc8",
    },
    {
        "name": "Leonardo Lightning XL",
        "model": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
        "url": "https://app.leonardo.ai/models/b24e16ff-06e3-43eb-8d33-4416c2d75876",
    },
    {
        "name": "Leonardo Kino XL",
        "model": "aa77f04e-3eec-4034-9c07-d0f619684628",
        "url": "https://app.leonardo.ai/models/aa77f04e-3eec-4034-9c07-d0f619684628",
    },
    {
        "name": "SDXL 1.0",
        "model": "16e7060a-803e-4df3-97ee-edcfa5dc9cc8",
        "url": "https://app.leonardo.ai/models/16e7060a-803e-4df3-97ee-edcfa5dc9cc8",
    },
    {
        "name": "Leonardo Vision XL",
        "model": "5c232a9e-9061-4777-980a-ddc8e65647c6",
        "url": "https://app.leonardo.ai/models/5c232a9e-9061-4777-980a-ddc8e65647c6",
    },
    {
        "name": "AlbedoBase XL",
        "model": "2067ae52-33fd-4a82-bb92-c2c55e7d2786",
    },
    {
        "name": "Retro illustrations",
        "model": "133a8391-de9e-49e1-aee6-12d375cdef14",
        "url": "https://app.leonardo.ai/models133a8391-de9e-49e1-aee6-12d375cdef14",
    },
    {
        "name": "mon prefere artiste",
        "model": "bb18b23f-d86e-4280-9a0c-8e7c051e3daf",
        "url": "https://app.leonardo.ai/models/bb18b23f-d86e-4280-9a0c-8e7c051e3daf",
    },
    {
        "name": "Watercolor sketch",
        "model": "966002a0-9d71-42ca-922d-233a5781dd8c",
        "url": "https://app.leonardo.ai/models/966002a0-9d71-42ca-922d-233a5781dd8c",
    },
    {
        "name": "ArchDwg",
        "model": "cce5a67f-9f7c-48a7-baf7-bd32c55745f5",
        "url": "https://app.leonardo.ai/models/cce5a67f-9f7c-48a7-baf7-bd32c55745f5",
    },
]


class gtUILeonardoImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = (
        "Leonardo.AI Image Generation Driver. Learn more at http://leonardo.ai"
    )

    @classmethod
    def INPUT_TYPES(s):
        models = []
        for model in leonardo_models:
            models.append(model["name"])

        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Select the model to use for image generation.",
                    },
                ),
                "use_custom_model": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Enable to use a custom model ID."},
                ),
                "custom_model": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Enter the custom model ID if 'Use Custom Model' is enabled.",
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_token_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable for the API key. Do not use your actual API key directly.",
                    },
                ),
            }
        )
        return inputs

    def get_model_by_name(self, name):
        for model in leonardo_models:
            if model["name"] == name:
                return model["model"]
        return None

    def create(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_token_env_var", DEFAULT_API_KEY_ENV_VAR))
        model = kwargs.get("model", leonardo_models[0])
        use_custom_model = kwargs.get("use_custom_model", False)
        custom_model = kwargs.get("custom_model", "")

        if use_custom_model and custom_model != "":
            m = custom_model
        else:
            m = self.get_model_by_name(model)

        params = {}
        if api_key:
            params["api_key"] = api_key
        if m:
            params["model"] = m
        driver = LeonardoImageGenerationDriver(**params)
        return (driver,)
