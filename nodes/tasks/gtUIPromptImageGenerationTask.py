import os

import folder_paths
from griptape.drivers import (
    DummyImageGenerationDriver,
    OpenAiImageGenerationDriver,
)
from griptape.engines import (
    PromptImageGenerationEngine,
)
from griptape.tasks import (
    PromptImageGenerationTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    image_path_to_output,
)
from .gtUIBaseTask import gtUIBaseTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class gtUIPromptImageGenerationTask(gtUIBaseTask):
    DESCRIPTION = "Generate an image from a text prompt."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"driver": ("DRIVER",)})
        return inputs

    RETURN_TYPES = (
        "IMAGE",
        "AGENT",
        "STRING",
    )
    RETURN_NAMES = (
        "IMAGE",
        "AGENT",
        "file_path",
    )
    CATEGORY = "Griptape/Images"

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        driver = kwargs.get("driver", None)
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)

        if not driver:
            # Check and see if the agent.config has an image_generation_driver
            if isinstance(
                agent.config.image_generation_driver, DummyImageGenerationDriver
            ):
                # create a default driver
                driver = OpenAiImageGenerationDriver(
                    model="dall-e-3",
                    quality="hd",
                    style="natural",
                    api_key=OPENAI_API_KEY,
                )
                print(
                    "Current driver doesn't have an image_generation - using OpenAI by default."
                )
            else:
                driver = agent.config.image_generation_driver
        # Create an engine configured to use the driver.
        engine = PromptImageGenerationEngine(
            image_generation_driver=driver,
        )

        output_dir = folder_paths.get_temp_directory()
        prompt_task = PromptImageGenerationTask(
            input=prompt_text,
            image_generation_engine=engine,
            output_dir=output_dir,
        )
        try:
            agent.add_task(prompt_task)
        except Exception as e:
            print(e)

        result = agent.run()
        filename = result.output_task.output.name
        image_path = os.path.join(output_dir, filename)

        # Get the image in a format ComfyUI can read
        output_image, output_mask = image_path_to_output(image_path)

        return (output_image, agent, image_path)
