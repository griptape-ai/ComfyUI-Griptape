import base64
import os

import folder_paths
from griptape.black_forest.drivers.black_forest_image_generation_driver import (
    BlackForestImageGenerationDriver,
)
from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    AzureOpenAiImageGenerationDriver,
    LeonardoImageGenerationDriver,
    OpenAiImageGenerationDriver,
)
from griptape.engines import (
    InpaintingImageGenerationEngine,
)
from griptape.loaders import ImageLoader
from griptape.tasks import InpaintingImageGenerationTask

from ...py.griptape_settings import GriptapeSettings
from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
    image_path_to_output,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"


class gtUIInpaintingImageGenerationTask(gtUIBaseImageTask):
    DESCRIPTION = (
        "Generate an image using an input image, a mask image, and a text prompt."
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "mask": ("MASK",),
            }
        )
        inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = (
        "IMAGE",
        "STRING",
    )
    RETURN_NAMES = (
        "IMAGE",
        "FILE_PATH",
    )

    def _model_supports_inpainting(self, driver):
        # Map driver types to their supported models and default error messages
        supported_models = {
            OpenAiImageGenerationDriver: {
                "models": ["dall-e-2"],
                "default_message": "OpenAI model must be dall-e-2 for inpainting.",
            },
            BlackForestImageGenerationDriver: {
                "models": ["flux-pro-1.0-fill"],
                "default_message": "BlackForest model must be flux-pro-1.0-fill for inpainting.",
            },
            LeonardoImageGenerationDriver: {
                "models": [],
                "default_message": "Leonardo.AI does not support Inpainting. Please choose a different driver.",
            },
            AmazonBedrockImageGenerationDriver: {
                "models": ["stability.stable-diffusion-xl-v1"],
                "default_message": "Amazon Bedrock model must be stability.stable-diffusion-xl-v1 for inpainting.",
            },
            AzureOpenAiImageGenerationDriver: {
                "models": ["dall-e-2"],
                "default_message": "Azure OpenAI model must be dall-e-2 for inpainting.",
            },
        }

        # Get the supported models and error message for the driver's type
        driver_type = type(driver)
        if driver_type in supported_models:
            config = supported_models[driver_type]
            if driver.model in config["models"]:
                return True, ""
            else:
                return False, config["default_message"]

        # Driver type not supported
        return (
            False,
            f"Driver type {driver_type.__name__} or model {driver.model} is not supported for image inpainting.",
        )

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        mask = kwargs.get("mask")
        driver = kwargs.get("driver", None)
        input_string = kwargs.get("input_string", None)

        agent = Agent()
        final_image = convert_tensor_to_base_64(image)
        final_mask = convert_tensor_to_base_64(mask)
        # final_mask = mask_to_image(mask)
        if not final_image:
            return ("No image provided", agent)
        if not final_mask:
            return ("No mask provided", agent)
        prompt_text = self.get_prompt_text(STRING, input_string)
        if not driver:
            settings = GriptapeSettings()
            OPENAI_API_KEY = settings.get_settings_key_or_use_env("OPENAI_API_KEY")

            driver = OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dall-e-2",
            )
        # Check the model can handle InPainting
        inpainting_supported, msg = self._model_supports_inpainting(driver)
        if not inpainting_supported:
            raise ValueError(msg)

        # Quick fix for flux-pro-1.0-fill
        if isinstance(driver, BlackForestImageGenerationDriver):
            # check the model to make sure it's one that can handle Variation Image Generation
            if driver.model == "flux-pro-1.0-fill":
                driver.model = "flux-pro-1.0"

        # Create an engine configured to use the driver.
        engine = InpaintingImageGenerationEngine(
            image_generation_driver=driver,
        )
        image_artifact = ImageLoader().parse(base64.b64decode(final_image[0]))
        mask_artifact = ImageLoader().parse(base64.b64decode(final_mask[0]))
        output_dir = folder_paths.get_temp_directory()
        inpainting_task = InpaintingImageGenerationTask(
            input=(prompt_text, image_artifact, mask_artifact),
            image_generation_engine=engine,
            output_dir=output_dir,
        )

        # if deferred_evaluation:
        #     return (None, "Image Variation Task Created", variation_task)
        try:
            agent.add_task(inpainting_task)
        except Exception as e:
            print(e)
        try:
            result = agent.run()
        except Exception as e:
            print(e)
        filename = result.output_task.output.name
        image_path = os.path.join(output_dir, filename)
        # Get the image in a format ComfyUI can read
        output_image, output_mask = image_path_to_output(image_path)

        return (output_image, image_path)
