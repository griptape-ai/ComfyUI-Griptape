from griptape.tasks import (
    TextSummaryTask,
    ToolTask,
    ToolkitTask,
    ImageQueryTask,
    PromptImageGenerationTask,
    VariationImageGenerationTask,
)
from griptape.engines import (
    ImageQueryEngine,
    PromptImageGenerationEngine,
    VariationImageGenerationEngine,
)
from griptape.drivers import OpenAiVisionImageQueryDriver, OpenAiImageGenerationDriver
from griptape.loaders import ImageLoader
from griptape.structures import Agent

from .base_task import gtUIBaseTask
from .base_image_task import gtUIBaseImageTask
import base64
import folder_paths
import os
from .utlities import image_path_to_output, convert_tensor_to_base_64
from jinja2 import Template
from groq import Groq

default_prompt = "{{ input_prompt }}"
# GROQ_API_KEY = "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"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class gtUIPromptTask(gtUIBaseTask): ...


class gtUIGroqPromptTask(gtUIBaseTask):
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": default_prompt,
                    },
                ),
            },
            "optional": {
                "input_prompt": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)

    FUNCTION = "run"

    def get_prompt_text(self, string_prompt, input_prompt):
        # We want to take the string_prompt and substitute {{ input_prompt }}
        template = Template(string_prompt)
        return template.render(input_prompt=input_prompt)

    def run(
        self,
        string_prompt,
        input_prompt=None,
    ):
        # Create a groq agent
        agent = Groq(api_key=GROQ_API_KEY)

        prompt_text = self.get_prompt_text(string_prompt, input_prompt)
        chat_completion = agent.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
            model="mixtral-8x7b-32768",
        )
        result = chat_completion.choices[0].message.content
        return (result, agent)


class gtUIPromptImageGenerationTask(gtUIBaseTask):

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["agent"]
        # inputs["optional"].remove("agent")
        return inputs

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "file_path")
    CATEGORY = "Griptape/Preview"

    def run(
        self,
        string_prompt,
        driver=None,
        input_prompt=None,
        # agent=None,
    ):
        # if not agent:
        agent = Agent()

        prompt_text = self.get_prompt_text(string_prompt, input_prompt)
        if not driver:
            driver = OpenAiImageGenerationDriver(
                model="dall-e-3", quality="hd", style="natural"
            )
        # Create an engine configured to use the driver.
        engine = PromptImageGenerationEngine(
            image_generation_driver=driver,
        )

        try:
            output_dir = folder_paths.get_temp_directory()

            agent.add_task(
                PromptImageGenerationTask(
                    input=prompt_text,
                    image_generation_engine=engine,
                    output_dir=output_dir,
                )
            )
        except Exception as e:
            print(e)
        result = agent.run()
        filename = result.output_task.output.name
        image_path = os.path.join(output_dir, filename)

        # Get the image in a format ComfyUI can read
        output_image, output_mask = image_path_to_output(image_path)

        return (output_image, image_path)


class gtUIPromptImageVariationTask(gtUIBaseImageTask):

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "file_path")
    CATEGORY = "Griptape/Images"

    def run(
        self,
        string_prompt,
        image,
        driver=None,
        input_prompt=None,
        # agent=None,
    ):
        # if not agent:
        agent = Agent()
        final_image = convert_tensor_to_base_64(image)
        if not final_image:
            return ("No image provided", agent)

        prompt_text = self.get_prompt_text(string_prompt, input_prompt)
        if not driver:
            driver = OpenAiImageGenerationDriver(
                model="dall-e-2",
            )
        # Create an engine configured to use the driver.
        engine = VariationImageGenerationEngine(
            image_generation_driver=driver,
        )
        image_artifact = ImageLoader().load(base64.b64decode(final_image))
        try:
            output_dir = folder_paths.get_temp_directory()

            agent.add_task(
                VariationImageGenerationTask(
                    input=(prompt_text, image_artifact),
                    image_generation_engine=engine,
                    output_dir=output_dir,
                )
            )
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


class gtUIImageQueryTask(gtUIBaseImageTask):

    def run(
        self,
        string_prompt,
        image,
        input_prompt=None,
        agent=None,
    ):
        final_image = convert_tensor_to_base_64(image)
        if final_image:
            if not agent:
                agent = Agent()

            driver = OpenAiVisionImageQueryDriver(model="gpt-4-vision-preview")
            engine = ImageQueryEngine(image_query_driver=driver)
            image_artifact = ImageLoader().load(base64.b64decode(final_image))

            prompt_text = self.get_prompt_text(string_prompt, input_prompt)

            task = ImageQueryTask(
                input=(prompt_text, [image_artifact]), image_query_engine=engine
            )
            try:
                agent.add_task(task)
            except Exception as e:
                print(e)
            result = agent.run()
            output = result.output_task.output.value
        else:
            output = "No image provided"
        return (output, agent)


class gtUITextSummaryTask(gtUIBaseTask):
    def run(self, string_prompt, input_prompt=None, agent=None):
        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(string_prompt, input_prompt)
        try:
            agent.add_task(TextSummaryTask(prompt_text))
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent)


class gtUIToolTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tool": ("TOOL",),
            }
        )
        return inputs

    def run(
        self,
        string_prompt,
        tool=None,
        input_prompt=None,
        agent=None,
    ):
        if not tool:
            return super().create(string_prompt, input_prompt, agent)

        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(string_prompt, input_prompt)

        task = ToolTask(prompt_text, tool=tool)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run()
        print(result.output_task.output.value)
        return (result.output_task.output.value, agent)


class gtUIToolkitTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tools": ("TOOL_LIST",),
            }
        )
        return inputs

    def run(
        self,
        string_prompt,
        tools=[],
        input_prompt=None,
        agent=None,
    ):
        if len(tools) == 0:
            return super().run(string_prompt, input_prompt, agent)

        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(string_prompt, input_prompt)

        task = ToolkitTask(prompt_text, tools=tools)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent)
