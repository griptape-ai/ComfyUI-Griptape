from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver
from .image_generation.bria_image_generation_driver import BriaImageGenerationDriver

DEFAULT_API_KEY = "BRIA_API_KEY"
models = ["base", "fast", "hd"]
model_versions = ["2.3", "2.2"]
aspect_ratios = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9"]
mediums = ["photography", "art"]
guidance_methods = [
    "None",
    "controlnet_canny",
    "controlnet_depth",
    "controlnet_recoloring",
    "controlnet_color_grid",
]


class gtUIBriaImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Bria.ai Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "image_generation_model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Select the image generation model.",
                    },
                ),
                "image_generation_model_version": (
                    model_versions,
                    {
                        "default": model_versions[0],
                        "tooltip": "Select the model version.",
                    },
                ),
                "aspect_ratio": (
                    aspect_ratios,
                    {
                        "default": aspect_ratios[0],
                        "tooltip": "Select the aspect ratio.",
                    },
                ),
                "max_attempts": (
                    "INT",
                    {
                        "default": 1,
                        "tooltip": "Number of attempts to generate the image.",
                    },
                ),
                "steps_num": (
                    "INT",
                    {
                        "default": 30,
                        "tooltip": "Number of steps to generate the image.",
                        "min": 20,
                        "max": 50,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "tooltip": "Seed for the random number generator.",
                    },
                ),
                "prompt_enhancement": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Optionally set to true if you want to enhance the prompt using Meta llama 3.",
                    },
                ),
                "text_guidance_scale": (
                    "FLOAT",
                    {
                        "default": 5.0,
                        "tooltip": "Determines how closely the generated image should adhere to the input text description. This parameter is optional.",
                        "min": 1.0,
                        "max": 10.0,
                    },
                ),
                "medium": (
                    mediums,
                    {
                        "default": mediums[0],
                        "tooltip": "Select the medium.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
                "image_variation_comment": (
                    "STRING",
                    {"default": "Image Variation Settings --------"},
                ),
                "guidance_1_comment": (
                    "STRING",
                    {
                        "default": "Method 1",
                    },
                ),
                "guidance_method_1": (
                    guidance_methods,
                    {"default": guidance_methods[0]},
                ),
                "guidance_method_1_scale": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                    },
                ),
                "guidance_2_comment": (
                    "STRING",
                    {
                        "default": "Method 2",
                    },
                ),
                "guidance_method_2": (
                    guidance_methods,
                    {"default": guidance_methods[0]},
                ),
                "guidance_method_2_scale": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                    },
                ),
                "guidance_3_comment": (
                    "STRING",
                    {
                        "default": "Method 3",
                    },
                ),
                "guidance_method_3": (
                    guidance_methods,
                    {"default": guidance_methods[0]},
                ),
                "guidance_method_3_scale": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                    },
                ),
                "guidance_4_comment": (
                    "STRING",
                    {
                        "default": "Method 4",
                    },
                ),
                "guidance_method_4": (
                    guidance_methods,
                    {"default": guidance_methods[0]},
                ),
                "guidance_method_4_scale": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                    },
                ),
            }
        )

        return inputs

    def adjust_version_based_on_model(self, model):
        # pick the approprite version
        if model == "hd":
            model_version = "2.2"
        return model_version

    def build_params(self, **kwargs):
        model = kwargs.get("image_generation_model", models[0])
        model_version = kwargs.get("image_generation_model_version", model_versions[0])
        if model == "hd":
            model_version = self.adjust_version_based_on_model(model)

        aspect_ratio = kwargs.get("aspect_ratio", aspect_ratios[0])
        max_attempts = kwargs.get("max_attempts", 1)
        steps_num = kwargs.get("steps_num", 30)
        seed = kwargs.get("seed", 0)
        prompt_enhancement = kwargs.get("prompt_enhancement", False)
        text_guidance_scale = kwargs.get("text_guidance_scale", 5.0)
        medium = kwargs.get("medium", mediums[0])

        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        params["model_version"] = model_version
        params["aspect_ratio"] = aspect_ratio
        params["type"] = "png"
        params["medium"] = medium
        params["prompt_enhancement"] = prompt_enhancement
        params["text_guidance_scale"] = text_guidance_scale
        params["seed"] = seed
        params["steps_num"] = steps_num
        params["max_attempts"] = max_attempts
        params["api_key"] = api_key

        if model != "hd":
            guidance_method_1 = kwargs.get("guidance_method_1", guidance_methods[0])
            guidance_method_2 = kwargs.get("guidance_method_2", guidance_methods[0])
            guidance_method_3 = kwargs.get("guidance_method_3", guidance_methods[0])
            guidance_method_4 = kwargs.get("guidance_method_4", guidance_methods[0])

            if guidance_method_1 != guidance_methods[0]:
                params["guidance_method_1"] = guidance_method_1
                params["guidance_method_1_scale"] = kwargs.get(
                    "guidance_method_1_scale", 1.0
                )
            if guidance_method_2 != guidance_methods[0]:
                params["guidance_method_2"] = guidance_method_2
                params["guidance_method_2_scale"] = kwargs.get(
                    "guidance_method_2_scale", 1.0
                )
            if guidance_method_3 != guidance_methods[0]:
                params["guidance_method_3"] = guidance_method_3
                params["guidance_method_3_scale"] = kwargs.get(
                    "guidance_method_3_scale", 1.0
                )
            if guidance_method_4 != guidance_methods[0]:
                params["guidance_method_4"] = guidance_method_4
                params["guidance_method_4_scale"] = kwargs.get(
                    "guidance_method_4_scale", 1.0
                )

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = BriaImageGenerationDriver(**params)
        return (driver,)
