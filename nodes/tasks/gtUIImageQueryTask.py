import base64

from griptape.drivers import AmazonBedrockPromptDriver, AnthropicPromptDriver
from griptape.loaders import ImageLoader
from griptape.structures import Workflow
from griptape.tasks import PromptTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class gtUIImageQueryTask(gtUIBaseImageTask):
    DESCRIPTION = "Query an image for a detailed description."

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        images = convert_tensor_to_base_64(image)

        if images:
            if not agent:
                agent = Agent()
            prompt_driver = agent.config.prompt_driver
            prompt_text = self.get_prompt_text(STRING, input_string)
            # If the driver is AmazonBedrock or Anthropic, the prompt_text cannot be empty
            if prompt_text.strip() == "":
                if isinstance(
                    prompt_driver,
                    (AmazonBedrockPromptDriver, AnthropicPromptDriver),
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
            # Depending on the model, we might need to use a workflow instead of a simple prompt
            rulesets = agent.rulesets
            tasks = []
            if len(image_artifacts) > 2:
                task_args = {}
                if agent.config.prompt_driver:
                    task_args["prompt_driver"] = prompt_driver
                if len(rulesets) > 0:
                    task_args["rulesets"] = rulesets
                end_task = PromptTask(
                    "Concatenate just the output values of the tasks, separated by two newlines: {{ parent_outputs }}",
                    id="END",
                    **task_args,
                )
                for artifact in image_artifacts:
                    task = PromptTask([prompt_text, artifact], **task_args)
                    task.add_child(end_task)
                    tasks.append(task)
                workflow = Workflow(tasks=[*tasks, end_task])
                result = workflow.run()
            else:
                result = agent.run([prompt_text, *image_artifacts])
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)
