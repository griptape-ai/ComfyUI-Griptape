import base64
import os
from textwrap import dedent

import folder_paths
from griptape.artifacts import BaseArtifact, TextArtifact
from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AnthropicImageQueryDriver,
    DummyAudioTranscriptionDriver,
    DummyImageGenerationDriver,
    DummyImageQueryDriver,
    OpenAiAudioTranscriptionDriver,
    OpenAiImageGenerationDriver,
)
from griptape.engines import (
    AudioTranscriptionEngine,
    ImageQueryEngine,
    PromptImageGenerationEngine,
    VariationImageGenerationEngine,
)
from griptape.loaders import AudioLoader, ImageLoader
from griptape.structures import Pipeline, Workflow
from griptape.tasks import (
    AudioTranscriptionTask,
    CodeExecutionTask,
    CsvExtractionTask,
    ImageQueryTask,
    JsonExtractionTask,
    PromptImageGenerationTask,
    PromptTask,
    TextSummaryTask,
    ToolkitTask,
    ToolTask,
    VariationImageGenerationTask,
)
from griptape.utils import load_file
from schema import Schema

from ..py.griptape_config import get_config
from .agent.agent import gtComfyAgent as Agent
from .base_audio_task import gtUIBaseAudioTask
from .base_image_task import gtUIBaseImageTask
from .base_task import gtUIBaseTask
from .utilities import (
    convert_tensor_to_base_64,
    image_path_to_output,
)

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")


class gtUIPromptTask(gtUIBaseTask): ...


class gtUICsvExtractionTask(gtUIBaseTask):
    DESCRIPTION = "Extract data from a CSV file."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "driver": ("DRIVER",),
                "columns": (
                    "STRING",
                    {
                        "multiline": False,
                        "dynamicPrompts": True,
                        "default": "Column 1, Column 2, Column 3",
                    },
                ),
            }
        )

        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        columns = kwargs.get("columns")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        try:
            if columns:
                column_list = columns.split(",")
            else:
                column_list = ["Column 1"]
            agent.add_task(
                CsvExtractionTask(prompt_text, args={"column_names": column_list})
            )
        except Exception as e:
            print(e)
        result = agent.run()
        # This returns a CSVRowArtifact object, which is not directly usable in ComfyUI
        # So we convert it to a string
        formatted_string = "\n".join(
            [
                ", ".join(
                    [f"{key.strip()}: {value}" for key, value in artifact.value.items()]
                )
                for artifact in result.output_task.output
            ]
        )

        return (formatted_string, agent)


class gtUIJsonExtractionTask(gtUIBaseTask):
    DESCRIPTION = "Extract data from a JSON file."

    @classmethod
    def INPUT_TYPES(s):
        default_schema = '{"users": [{"name": str, "age": int, "location": str}]}'
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "driver": ("DRIVER",),
                "schema": (
                    "STRING",
                    {
                        "multiline": True,
                        "dynamicPrompts": True,
                        "default": default_schema,
                    },
                ),
            }
        )

        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        schema = kwargs.get("schema")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        try:
            if schema:
                print(schema)
                template_schema = Schema(schema).json_schema("TemplateSchema")
            else:
                template_schema = Schema({}).json_schema("TemplateSchema")
            agent.add_task(
                JsonExtractionTask(
                    prompt_text, args={"template_schema": template_schema}
                )
            )
        # TODO - error extracting json
        except Exception as e:
            print(e)
        result = agent.run()
        output = result.output_task.output
        print(output)

        return (str(output.value), agent)


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
        "TASK",
    )
    RETURN_NAMES = ("IMAGE", "AGENT", "file_path", "TASK")
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

        # if deferred_evaluation:
        #     return (None, agent, "Image Generation Task created", prompt_task)

        result = agent.run()
        filename = result.output_task.output.name
        image_path = os.path.join(output_dir, filename)

        # Get the image in a format ComfyUI can read
        output_image, output_mask = image_path_to_output(image_path)

        return (output_image, agent, image_path)


class gtUIPromptImageVariationTask(gtUIBaseImageTask):
    DESCRIPTION = "Generate a variation of an image from a text prompt and an image."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = ("IMAGE", "STRING", "TASK")
    RETURN_NAMES = ("IMAGE", "FILE_PATH", "TASK")

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
        image_artifact = ImageLoader().load(base64.b64decode(final_image[0]))
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


class gtUIAudioTranscriptionTask(gtUIBaseAudioTask):
    DESCRIPTION = "Transcribe an audio file."
    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("STRING", "TASK")
    RETURN_NAMES = ("OUTPUT", "TASK")

    def run(self, **kwargs):
        audio = kwargs.get("audio", None)
        audio_filepath = kwargs.get("audio_filepath", None)
        driver = kwargs.get("driver", None)

        audio_artifact = None
        if audio:
            audio = self.save_audio_tempfile(audio)[0]
        elif audio_filepath:
            audio = audio_filepath
        else:
            return ("There is no audio file.",)

        try:
            audio_artifact = AudioLoader().load(load_file(audio))
        except Exception as e:
            print(f"Error loading audio file: {e}")
        if audio_artifact:
            if not driver:
                audio_transcription_driver = OpenAiAudioTranscriptionDriver(
                    model="whisper-1"
                )
            else:
                audio_transcription_driver = driver

            # If the driver is a DummyAudioTranscriptionDriver we'll return a nice error message
            if isinstance(audio_transcription_driver, DummyAudioTranscriptionDriver):
                return (
                    dedent(
                        """
                    I'm sorry, this agent doesn't have access to a valid AudioTranscriptionDriver.
                    You might want to try using a different Agent Configuration.

                    Reach out for help on Discord (https://discord.gg/gnWRz88eym) if you would like some help.
                    """,
                    ),
                )
            engine = AudioTranscriptionEngine(
                audio_transcription_driver=audio_transcription_driver
            )
            # prompt_text = self.get_prompt_text(STRING, input_string)

            task = AudioTranscriptionTask(
                input=lambda _: audio_artifact,
                audio_transcription_engine=engine,
            )

            # if deferred_evaluation:
            #     return ("Audio Transcription Task created", task)
            pipeline = Pipeline()
            pipeline.add_task(task)
            try:
                result = pipeline.run()
            except Exception as e:
                print(e)
            output = result.output_task.output.value
        else:
            output = "No audio provided"
        return (output,)


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


class gtUITextSummaryTask(gtUIBaseTask):
    DESCRIPTION = "Summarize a text prompt."

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        task = TextSummaryTask(prompt_text)
        # if deferred_evaluation:
        #     return ("Text Summary Task Created", agent, task)
        try:
            agent.add_task(TextSummaryTask(prompt_text))
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent, task)


class gtUIToolTask(gtUIBaseTask):
    DESCRIPTION = "Run a tool on a text prompt."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'tool' and adjust others as necessary
        inputs["optional"].update(
            {
                "tool": ("TOOL_LIST",),
            }
        )
        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        tool = kwargs.get("tool", [])
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        if not agent:
            agent = Agent()

        prompt_text = self.get_prompt_text(STRING, input_string)

        # Figure out what tool to use.
        # If none are provided, check the agent for tools
        # if the agent doesn't have any, then we won't use any tools.
        agent_tools = []
        agent_tools = agent.tools

        if len(tool) > 0:
            agent_tool = tool[0]
        elif len(agent_tools) > 0:
            agent_tool = agent_tools[0]
        else:
            agent_tool = None

        if agent_tool:
            # No point in using off_prompt if we're using a ToolTask - it's not supported
            agent_tool.off_prompt = False
            task = ToolTask(prompt_text, tool=agent_tool)
        else:
            task = PromptTask(prompt_text)

        # if deferred_evaluation:
        #     return ("Tool Task Created", task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent)


class gtUIToolkitTask(gtUIBaseTask):
    DESCRIPTION = "Provide a list of tools, and have the agent decide which of them to use utilizing Chain of Thought."

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

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        tools = kwargs.get("tools", [])
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        prompt_text = self.get_prompt_text(STRING, input_string)

        if len(tools) == 0:
            return super().run(STRING, input_string, agent)

        if prompt_text.strip() == "":
            return ("No prompt provided", agent)
        # if the tool is provided, keep going
        if not agent:
            agent = Agent()

        model, simple_model = agent.model_check()
        if simple_model:
            response = agent.model_response(model)
            return (response, agent)

        task = ToolkitTask(prompt_text, tools=tools)
        # if deferred_evaluation:
        #     return ("Toolkit Task Created.", task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)

        result = agent.run()
        return (result.output_task.output.value, agent)
