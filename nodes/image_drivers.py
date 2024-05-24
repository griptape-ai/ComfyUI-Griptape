from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockStableDiffusionImageGenerationModelDriver,
    BedrockTitanImageGenerationModelDriver,
    LeonardoImageGenerationDriver,
    OpenAiImageGenerationDriver,
)

from ..py.griptape_config import get_config
from .base_driver import gtUIBaseImageGenerationDriver

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


class gtUIOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    @classmethod
    def INPUT_TYPES(s):
        models = ["dall-e-3", "dall-e-2"]
        sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]

        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "size": (sizes, {"default": sizes[2]}),
            }
        )
        return inputs

    def adjust_size_based_on_model(self, model, size):
        # pick the approprite size based on the model
        if model == "dall-e-2":
            if size in ["1024x1792", "1792x1024"]:
                size = "1024x1024"
        if model == "dall-e-3":
            if size in ["256x256", "512x512"]:
                size = "1024x1024"
        return size

    def create(self, model, size, prompt):
        size = self.adjust_size_based_on_model(model, size)
        driver = OpenAiImageGenerationDriver(model=model, image_size=size)
        return (driver,)


class gtUILeonardoImageGenerationDriver(gtUIBaseImageGenerationDriver):
    @classmethod
    def INPUT_TYPES(s):
        models = []
        for model in leonardo_models:
            models.append(model["name"])

        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "use_custom_model": (["yes", "no"], {"default": "no"}),
                "custom_model": ("STRING", {"default": ""}),
            }
        )
        return inputs

    def get_model_by_name(self, name):
        for model in leonardo_models:
            if model["name"] == name:
                return model["model"]
        return None

    def create(self, model, prompt, use_custom_model=False, custom_model=""):
        if use_custom_model == "yes" and custom_model != "":
            m = custom_model
        else:
            m = self.get_model_by_name(model)
        driver = LeonardoImageGenerationDriver(
            api_key=get_config(key="env.LEONARDO_API_KEY", default=None),
            model=m,
        )
        return (driver,)


class gtUIAmazonBedrockStableDiffusionImageGenerationDriver(
    gtUIBaseImageGenerationDriver
):
    @classmethod
    def INPUT_TYPES(s):
        style_presets = [
            "<None>",
            "3d-model",
            "analog-film",
            "anime",
            "cinematic",
            "comic-book",
            "digital-art",
            "enhance",
            "fantasy-art",
            "isometric",
            "line-art",
            "low-poly",
            "modeling-compound",
            "neon-punk",
            "origami",
            "photographic",
            "pixel-art",
            "tile-texture",
        ]
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "style_preset": (style_presets, {"default": style_presets[4]}),
                "width": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "seed": ("INT", {"default": 12345}),
            }
        )
        return inputs

    def create(self, style_preset, width, height, seed, prompt):
        if style_preset == "<None>":
            style_preset = None
        model_driver = BedrockStableDiffusionImageGenerationModelDriver(
            style_preset=style_preset,
        )
        driver = AmazonBedrockImageGenerationDriver(
            image_generation_model_driver=model_driver,
            model="stability.stable-diffusion-xl-v1",
            image_width=width,
            image_height=height,
            seed=seed,
        )
        return (driver,)


class gtUIAmazonBedrockTitanImageGenerationDriver(gtUIBaseImageGenerationDriver):
    @classmethod
    def INPUT_TYPES(s):
        sizes = ["512x512", "1024x1024"]
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "size": (sizes, {"default": sizes[0]}),
                "seed": ("INT", {"default": 10342349342}),
            }
        )
        return inputs

    def create(self, size, seed, prompt):
        width, height = size.split("x")
        model_driver = BedrockTitanImageGenerationModelDriver()
        driver = AmazonBedrockImageGenerationDriver(
            image_generation_model_driver=model_driver,
            model="amazon.titan-image-generator-v1",
            image_width=int(width),
            image_height=int(height),
            seed=seed,
        )
        return (driver,)
