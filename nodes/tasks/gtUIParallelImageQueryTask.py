import base64

from griptape.artifacts import BaseArtifact, TextArtifact
from griptape.drivers.prompt.amazon_bedrock import AmazonBedrockPromptDriver
from griptape.drivers.prompt.anthropic import AnthropicPromptDriver
from griptape.loaders import ImageLoader
from griptape.structures import Workflow
from griptape.tasks import (
    CodeExecutionTask,
    PromptTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
# settings = GriptapeSettings()

# OPENAI_API_KEY = settings.get_settings_key_or_use_env("OPENAI_API_KEY")


def do_start_task(task: CodeExecutionTask) -> BaseArtifact:
    return TextArtifact(str(task.input))


class gtUIParallelImageQueryTask(gtUIBaseImageTask):
    DESCRIPTION = (
        "Query an image for multiple detailed descriptions. This runs in parallel."
    )

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        final_image = convert_tensor_to_base_64(image)
        if final_image:
            if not agent:
                agent = Agent()

            prompt_driver = agent.drivers_config.prompt_driver
            rulesets = agent.rulesets
            image_artifact = ImageLoader().parse(base64.b64decode(final_image[0]))

            prompt_text = self.get_prompt_text(STRING, input_string)

            # If the driver is AmazonBedrock or Anthropic, the prompt_text cannot be empty
            if prompt_text.strip() == "":
                if isinstance(
                    prompt_driver,
                    (AmazonBedrockPromptDriver, AnthropicPromptDriver),
                ):
                    prompt_text = "Describe this image"

            structure = Workflow(rulesets=rulesets)
            start_task = CodeExecutionTask("Start", on_run=do_start_task, id="START")
            end_task = PromptTask(
                "Concatenate just the output values of the tasks, separated by two newlines: {{ parent_outputs }}",
                id="END",
                prompt_driver=agent.drivers_config.prompt_driver,
                rulesets=rulesets,
            )
            structure.add_task(start_task)
            structure.add_task(end_task)

            prompts = prompt_text.split("\n")
            prompt_tasks = []
            for prompt in prompts:
                task = PromptTask(
                    (prompt, [image_artifact]),
                    prompt_driver=prompt_driver,
                    context=self.get_context_as_dict(
                        kwargs.get("key_value_replacement", None)
                    ),
                )
                prompt_tasks.append(task)

            structure.insert_tasks(start_task, prompt_tasks, end_task)

            result = structure.run()
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)
