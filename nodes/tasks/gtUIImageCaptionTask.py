"""Generates image captions."""

import base64
import json
import os

from griptape.loaders import ImageLoader
from griptape.rules import Rule, Ruleset
from griptape.structures import Workflow
from griptape.tasks import PromptTask
from icecream import ic

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import (
    convert_tensor_to_base_64,
)
from .gtUIBaseImageTask import gtUIBaseImageTask

default_prompt = "{{ input_string }}"
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def find_image_filenames(node_id, prompt):
    def trace_inputs(current_node_id, prompt_data):
        # Get the current node data from the prompt
        current_node = prompt_data[current_node_id]
        class_type = current_node["class_type"]
        # If the node is a "LoadImage" node, return the image filename
        if class_type == "LoadImage":
            return [current_node["inputs"]["image"]]
        # Check if it's a directory-loading node, like "LoadImagesFromDir"
        if class_type in ["LoadImagesFromDir //Inspire"]:
            directory = current_node["inputs"]["directory"]
            start_index = current_node["inputs"].get("start_index", 0)
            image_load_cap = current_node["inputs"].get("image_load_cap", 0)

            # List files in the directory
            all_files = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]
            selected_files = (
                sorted(all_files)[start_index : start_index + image_load_cap]
                if image_load_cap > 0
                else sorted(all_files)
            )
            ic(selected_files)
            return selected_files

        # If the node is not "LoadImage", trace back its inputs
        input_filenames = []
        if "inputs" in current_node:
            for input_key, input_value in current_node["inputs"].items():
                if isinstance(
                    input_value, list
                ):  # If input is a reference to another node
                    input_node_id = input_value[0]
                    input_filenames.extend(trace_inputs(input_node_id, prompt_data))

        return input_filenames

    # Start tracing from the given node_id
    return trace_inputs(node_id, prompt)


class gtUIImageCaptionTask(gtUIBaseImageTask):
    DESCRIPTION = "Build a JSON list of images and their descriptions."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "sample_index": (
                    "INT",
                    {
                        "default": 0,
                        "tooltip": "Choose which image to display a sample caption for.",
                    },
                ),
                "sample_output": ("STRING", {"multiline": True}),
            }
        )
        del inputs["optional"]["input_string"]
        del inputs["required"]["STRING"]
        return inputs

    # Remove input_string
    # change output to CAPTIONS

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    CATEGORY = "Griptape/LoRA"
    # OUTPUT_NODE = True

    def run(self, **kwargs):
        image = kwargs.get("image")
        ic(type(image))
        agent = kwargs.get("agent", None)
        unique_id = kwargs.get("unique_id")
        prompt = kwargs.get("prompt")
        extra_pnginfo = kwargs.get("extra_pnginfo")
        sample_index = kwargs.get("sample_index")
        image_filenames = find_image_filenames(unique_id, prompt)
        images = convert_tensor_to_base_64(image)
        output_example = "No example available"
        if images:
            if not agent:
                agent = Agent()
            prompt_driver = agent.drivers_config.prompt_driver
            prompt_text = "Describe this image for LoRA training."

            image_artifacts = []
            for base64Image in images:
                try:
                    image_artifacts.append(
                        ImageLoader().load(base64.b64decode(base64Image))
                    )
                except Exception as e:
                    raise (f"Couldn't load image {e}")

            rulesets = agent.rulesets

            # Create task-specific rulesets
            task_ruleset = Ruleset(
                name="ImageRuleset",
                rules=[
                    Rule(
                        "Always output a valid JSON object with the keys 'file' and 'description'."
                    )
                ],
            )
            json_ruleset = Ruleset(
                name="JSONRuleset", rules=[Rule("Never wrap your response in ```")]
            )
            tasks = []
            task_args = {}
            if agent.drivers_config.prompt_driver:
                task_args["prompt_driver"] = prompt_driver
            if len(rulesets) > 0:
                task_args["rulesets"] = rulesets + [json_ruleset]
            else:
                task_args["rulesets"] = [json_ruleset]

            end_task = PromptTask(
                """Output a valid JSON object as 'captions', and list the descriptions and image names with the keys 'file' and 'description'.
                Example:
                {
                  "captions":[
                    {
                        "file": "raccoon_rummaging.png",
                        "description": "The image shows a raccoon in an alleyway at night..."
                    }
                  ]
                }\n\n-----\n\n{{ parent_outputs }}""",
                id="END",
                **task_args,
            )
            end_task.prompt_driver.output_format = "json_object"

            task_args["rulesets"] += [task_ruleset]
            for index, artifact in enumerate(image_artifacts):
                task = PromptTask(
                    [
                        f"Image Name: {image_filenames[index]}\n\n{prompt_text}",
                        artifact,
                    ],
                    **task_args,
                )
                task.prompt_driver.output_format = "json_object"
                task.add_child(end_task)
                tasks.append(task)
            workflow = Workflow(tasks=[*tasks, end_task])
            result = workflow.run()
            output = result.output_task.output.value
            index = min(sample_index, len(json.loads(output)["captions"]) - 1)
            output_example = json.loads(output)["captions"][index]["description"]
        else:
            output = "No image provided"

        # return (output,)
        return {
            "ui": {"sample_output": output},
            "result": (output,),
        }
