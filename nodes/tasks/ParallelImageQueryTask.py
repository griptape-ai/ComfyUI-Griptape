import base64
from textwrap import dedent

from griptape.artifacts import BaseArtifact, TextArtifact
from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AnthropicImageQueryDriver,
    DummyImageQueryDriver,
)
from griptape.engines import (
    ImageQueryEngine,
)
from griptape.loaders import ImageLoader
from griptape.structures import Workflow
from griptape.tasks import (
    CodeExecutionTask,
    ImageQueryTask,
    PromptTask,
)

from ...py.griptape_config import get_config
from ..agent.agent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .BaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")


def do_start_task(task: CodeExecutionTask) -> BaseArtifact:
    return TextArtifact(str(task.input))


class gtUIParallelImageQueryTask(gtUIBaseImageTask):
    DESCRIPTION = (
        "Query an image for multiple detailed descriptions. This runs in parallel."
    )
    CATEGORY = "Griptape/Images"

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        image = kwargs.get("image")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        final_image = convert_tensor_to_base_64(image)
        if final_image:
            if not agent:
                agent = Agent()

            image_query_driver = agent.config.image_query_driver
            rulesets = agent.rulesets
            # If the driver is a DummyImageQueryDriver we'll return a nice error message
            if isinstance(image_query_driver, DummyImageQueryDriver):
                return (
                    dedent("""
                    I'm sorry, this agent doesn't have access to a valid ImageQueryDriver.
                    You might want to try using a different Agent Configuration.

                    Reach out for help on Discord (https://discord.gg/gnWRz88eym) if you would like some help.
                    """),
                    agent,
                )
            engine = ImageQueryEngine(image_query_driver=image_query_driver)
            image_artifact = ImageLoader().load(base64.b64decode(final_image[0]))

            prompt_text = self.get_prompt_text(STRING, input_string)

            # If the driver is AmazonBedrock or Anthropic, the prompt_text cannot be empty
            if prompt_text.strip() == "":
                if isinstance(
                    image_query_driver,
                    (AmazonBedrockImageQueryDriver, AnthropicImageQueryDriver),
                ):
                    prompt_text = "Describe this image"

            structure = Workflow(rulesets=rulesets)
            start_task = CodeExecutionTask("Start", run_fn=do_start_task, id="START")
            end_task = PromptTask(
                "Concatenate just the output values of the tasks, separated by two newlines: {{ parent_outputs }}",
                id="END",
                prompt_driver=agent.config.prompt_driver,
                rulesets=rulesets,
            )
            structure.add_task(start_task)
            structure.add_task(end_task)

            prompts = prompt_text.split("\n")
            prompt_tasks = []
            for prompt in prompts:
                # task = ToolTask(tool=ImageQueryClient(off_prompt=True), rulesets=rulesets)
                task = ImageQueryTask(
                    input=(prompt, [image_artifact]), image_query_engine=engine
                )
                prompt_tasks.append(task)

            structure.insert_tasks(start_task, prompt_tasks, end_task)

            result = structure.run()
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)
