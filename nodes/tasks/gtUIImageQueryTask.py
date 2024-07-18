import base64
import os

from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AnthropicImageQueryDriver,
)
from griptape.loaders import ImageLoader

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class gtUIImageQueryTask(gtUIBaseImageTask):
    DESCRIPTION = "Query an image for a detailed description."
    CATEGORY = "Griptape/Images"

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        images = convert_tensor_to_base_64(image)

        if images:
            if not agent:
                agent = Agent()
            image_query_driver = agent.config.image_query_driver
            prompt_text = self.get_prompt_text(STRING, input_string)

            # If the driver is AmazonBedrock or Anthropic, the prompt_text cannot be empty
            if prompt_text.strip() == "":
                if isinstance(
                    image_query_driver,
                    (AmazonBedrockImageQueryDriver, AnthropicImageQueryDriver),
                ):
                    prompt_text = "Describe this image"

            image_artifacts = []
            for base64Image in images:
                try:
                    image_artifacts.append(
                        ImageLoader().load(base64.b64decode(base64Image))
                    )
                except Exception as e:
                    raise (f"Couldn't load image {e}")

            # if deferred_evaluation:
            #     task = PromptTask([prompt_text, *image_artifacts])
            #     return ("Image Query Task Created", task)
            result = agent.run([prompt_text, *image_artifacts])
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)
