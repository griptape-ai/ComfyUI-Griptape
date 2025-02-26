# pyright: reportMissingImports=false
import os
from typing import Any, Tuple

import folder_paths
from griptape.drivers.image_generation.dummy import DummyImageGenerationDriver
from griptape.drivers.image_generation.openai import OpenAiImageGenerationDriver
from griptape.structures import Pipeline
from griptape.tasks import (
    PromptImageGenerationTask,
)

from ...py.griptape_settings import GriptapeSettings
from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    image_path_to_output,
)
from .gtUIBaseTask import gtUIBaseTask

default_prompt = "{{ input_string }}"


class gtUIPromptImageGenerationTask(gtUIBaseTask):
    DESCRIPTION = "Generate an image from a text prompt."

    @classmethod
    def INPUT_TYPES(cls):
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
    CATEGORY = "Griptape/Image"

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("STRING")
        driver = kwargs.get("driver", None)
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)
        pipeline = None
        if not driver:
            # Check and see if the agent.config has an image_generation_driver
            if isinstance(
                agent.drivers_config.image_generation_driver, DummyImageGenerationDriver
            ):
                settings = GriptapeSettings()
                OPENAI_API_KEY = settings.get_settings_key_or_use_env("OPENAI_API_KEY")
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
                driver = agent.drivers_config.image_generation_driver
        output_dir = folder_paths.get_temp_directory()
        prompt_task = PromptImageGenerationTask(
            input=prompt_text,
            image_generation_driver=driver,
            output_dir=output_dir,
            context=self.get_context_as_dict(kwargs.get("key_value_replacement", None)),
        )
        try:
            pipeline = Pipeline()
            pipeline.add_task(prompt_task)
            # agent.add_task(prompt_task)
        except Exception as e:
            print(e)

        if pipeline is not None:
            result = pipeline.run()
            filename = result.output_task.output.name
            image_path = os.path.join(output_dir, filename)

            # Get the image in a format ComfyUI can read
            output_image, output_mask = image_path_to_output(image_path)

            return (output_image, agent, image_path)
        else:
            return ("Error", agent, None)
