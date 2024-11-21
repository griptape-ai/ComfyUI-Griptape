from griptape.black_forest.drivers.black_forest_image_generation_driver import (
    BlackForestImageGenerationDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_API_KEY = "BFL_API_KEY"
models = ["flux-pro-1.1", "flux-pro", "flux-dev", "flux-pro-1.1-ultra"]
widths = [str(i) for i in range(256, 1441, 32)]
heights = [str(i) for i in range(256, 1441, 32)]
safety_tolerance_list = ["strict", "high", "medium", "low", "very_low", "none"]
aspect_ratios = [f"{w}:{h}" for w in range(21, 8, -1) for h in range(9, 22)]


class gtUIBlackForestImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Black Forest Image Generation Driver to use Flux models."

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
                "width": (
                    widths,
                    {"default": "1024", "tooltip": "Select the desired image width."},
                ),
                "height": (
                    heights,
                    {"default": "768", "tooltip": "Select the desired image height."},
                ),
                "aspect_ratio_width": (
                    "INT",
                    {
                        "default": "16",
                        "min": 9,
                        "max": 21,
                        "tooltip": "Select the desired aspect width.",
                    },
                ),
                "aspect_ratio_height": (
                    "INT",
                    {
                        "default": "9",
                        "min": 9,
                        "max": 21,
                        "tooltip": "Select the desired aspect height.",
                    },
                ),
                "prompt_upsampling": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Whether to perform upsampling on the prompt. If active, automatically modifies the prompt for more creative generation.",
                        "label_on": "True (Modify Prompt)",
                        "label_off": "False (No Modification)",
                    },
                ),
                "safety_tolerance": (
                    safety_tolerance_list,
                    {
                        "default": safety_tolerance_list[2],
                        "tooltip": "Select the safety tolerance level.",
                    },
                ),
                "steps": (
                    "INT",
                    {
                        "default": None,
                        "tooltip": "Number of steps for the image generation process.",
                        "min": 1,
                        "max": 50,
                    },
                ),
                "guidance": (
                    "FLOAT",
                    {
                        "default": None,
                        "tooltip": "Guidance for the image generation process. High guidance scales improve prompt adherence as the cost of reduced realism.",
                        "min": 1.5,
                        "max": 5,
                    },
                ),
                "interval": (
                    "INT",
                    {
                        "default": None,
                        "tooltip": "Optional interfal parameter for guidance control.",
                        "min": 1,
                        "max": 4,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 10342349342,
                        "tooltip": "Seed for random number generation.",
                    },
                ),
                "raw": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Generate less processed, more natural-looking images",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("image_generation_model", models[0])
        width = kwargs.get("width", "1024")
        height = kwargs.get("height", "768")
        aspect_ratio_width = kwargs.get("aspect_ratio_width", 16)
        aspect_ratio_height = kwargs.get("aspect_ratio_height", 9)
        aspect_ratio = f"{aspect_ratio_width}:{aspect_ratio_height}"
        prompt_upsampling = kwargs.get("prompt_upsampling", False)
        safety_tolerance_str = kwargs.get("safety_tolerance", safety_tolerance_list[2])
        safety_tolerance = safety_tolerance_list.index(safety_tolerance_str)
        seed = kwargs.get("seed", 10342349342)
        steps = kwargs.get("steps", None)
        guidance = kwargs.get("guidance", None)
        interval = kwargs.get("interval", 0.5)
        raw = kwargs.get("raw", False)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if safety_tolerance:
            params["safety_tolerance"] = int(safety_tolerance)
        if seed:
            params["seed"] = int(seed)
        if api_key:
            params["api_key"] = api_key

        if model == "flux-pro-1.1-ultra":
            if aspect_ratio:
                params["aspect_ratio"] = aspect_ratio
        else:
            if width:
                params["width"] = int(width)
            if height:
                params["height"] = int(height)
            if prompt_upsampling:
                params["prompt_upsampling"] = bool(prompt_upsampling)

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = BlackForestImageGenerationDriver(**params)
        return (driver,)
