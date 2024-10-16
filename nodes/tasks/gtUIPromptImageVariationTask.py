import base64
import os

import folder_paths
from griptape.drivers import (
    OpenAiImageGenerationDriver,
)
from griptape.engines import (
    VariationImageGenerationEngine,
)
from griptape.loaders import ImageLoader
from griptape.tasks import (
    VariationImageGenerationTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
    image_path_to_output,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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
            driver = OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dall-e-2",
            )
        # Create an engine configured to use the driver.
        engine = VariationImageGenerationEngine(
            image_generation_driver=driver,
        )
        image_artifact = ImageLoader().parse(base64.b64decode(final_image[0]))
        output_dir = folder_paths.get_temp_directory()
        variation_task = VariationImageGenerationTask(
            input=(prompt_text, image_artifact),
            image_generation_engine=engine,
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
