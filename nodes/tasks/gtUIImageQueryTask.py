import base64

from griptape.drivers.prompt.amazon_bedrock import AmazonBedrockPromptDriver
from griptape.drivers.prompt.anthropic import AnthropicPromptDriver
from griptape.loaders import ImageLoader
from griptape.structures import Workflow
from griptape.tasks import PromptTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"


class gtUIImageQueryTask(gtUIBaseImageTask):
    DESCRIPTION = "Query an image for a detailed description."

    def _is_grog(self, prompt_driver):
        if hasattr(prompt_driver, "base_url") and prompt_driver.base_url:
            if "groq" in prompt_driver.base_url:
                return True
        return False

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        images = convert_tensor_to_base_64(image)

        if images:
            if not agent:
                agent = Agent()
            prompt_driver = agent.drivers_config.prompt_driver
            prompt_text = self.get_prompt_text(STRING, input_string)
            # If the driver is AmazonBedrock or Anthropic, the prompt_text cannot be empty
            if prompt_text.strip() == "":
                if isinstance(
                    prompt_driver,
                    (AmazonBedrockPromptDriver, AnthropicPromptDriver),
                ):
                    prompt_text = "Describe this image"

            # If the driver is Groq, rulesets _must_ be empty
            rulesets = []
            tmp_agent_rulesets = []
            tmp_task_rulesets = []

            if self._is_grog(prompt_driver):
                if len(agent.rulesets) > 0:
                    print(
                        "[Griptape Run: Image Description] Warning: Rulesets are not supported with Groq. Removing temporarily while getting Image Description."
                    )
                    tmp_agent_rulesets = agent.rulesets
                    tmp_task_rulesets = agent.tasks[0].rulesets
                    agent._rulesets = []
                    agent.tasks[0]._rulesets = []
            else:
                rulesets = agent.rulesets
            # Load each of the images
            image_artifacts = []
            for base64Image in images:
                try:
                    image_artifacts.append(
                        ImageLoader().parse(base64.b64decode(base64Image))
                    )
                except Exception as e:
                    raise RuntimeError(f"Couldn't load image {e}")

            tasks = []
            context = kwargs.get("key_value_replacement", None)
            # Depending on the model, we might need to use a workflow instead of a simple prompt
            if len(image_artifacts) > 2:
                task_args = {}
                if agent.drivers_config.prompt_driver:
                    task_args["prompt_driver"] = prompt_driver

                if context:
                    task_args["context"] = self.get_context_as_dict(context)
                if len(rulesets) > 0:
                    if "groq" not in prompt_driver.base_url:
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
                if context:
                    agent.tasks[0].context = self.get_context_as_dict(context)
                result = agent.run([prompt_text, *image_artifacts])

            # Reset the rulesets
            if self._is_grog(prompt_driver):
                agent._rulesets = tmp_agent_rulesets
                agent.tasks[0]._rulesets = tmp_task_rulesets
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)
