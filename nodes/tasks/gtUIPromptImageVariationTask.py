import base64
import os

import folder_paths

try:
    from griptape.black_forest.drivers.black_forest_image_generation_driver import (
        BlackForestImageGenerationDriver,
    )
except ImportError:
    print("BlackForestImageGenerationDriver not found")
from griptape.drivers import (
    OpenAiImageGenerationDriver,
)
from griptape.loaders import ImageLoader
from griptape.tasks import (
    VariationImageGenerationTask,
)

from ...py.griptape_settings import GriptapeSettings
from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
    image_path_to_output,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"


class gtUIPromptImageVariationTask(gtUIBaseImageTask):
    DESCRIPTION = "Generate a variation of an image from a text prompt and an image."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
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

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        driver = kwargs.get("driver", None)
        input_string = kwargs.get("input_string", None)

        agent = Agent()
        final_image = convert_tensor_to_base_64(image)
        if not final_image:
            return ("No image provided", agent)

        prompt_text = self.get_prompt_text(STRING, input_string)
        if not driver:
            settings = GriptapeSettings()
            OPENAI_API_KEY = settings.get_settings_key_or_use_env("OPENAI_API_KEY")

            driver = OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dall-e-2",
            )
        # Check if driver is BlackForestImageGenerationDriver
        if "BlackForestImageGenerationDriver" in globals() and isinstance(
            driver, BlackForestImageGenerationDriver
        ):
            # check the model to make sure it's one that can handle Variation Image Generation
            if driver.model not in [
                "flux-pro-1.0-canny",
                "flux-pro-1.0-depth",
                # "flux-dev",
                "flux-pro-1.1",
                # "flux-pro",
                "flux-pro-1.1-ultra",
            ]:
                raise ValueError(
                    f"Model {driver.model} is not supported for image variation."
                )
                return (
                    None,
                    f"Model {driver.model} is not supported for image variation.",
                )
        image_artifact = ImageLoader().parse(base64.b64decode(final_image[0]))
        output_dir = folder_paths.get_temp_directory()
        variation_task = VariationImageGenerationTask(
            input=(prompt_text, image_artifact),
            image_generation_driver=driver,
            output_dir=output_dir,
        )

        # if deferred_evaluation:
        #     return (None, "Image Variation Task Created", variation_task)
        try:
            agent.add_task(variation_task)
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
