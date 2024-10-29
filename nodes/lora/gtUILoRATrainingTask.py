import hashlib
import json
import os
import re
import shutil

import folder_paths
from griptape.structures import Pipeline
from griptape.tasks import ToolTask
from griptape.tools import CalculatorTool

# from .conductor_tool.tool import ConductorTool

instance_types = ["A5000", "A100"]


def to_safe_os_path(input_string):
    # Replace spaces with underscores
    safe_string = input_string.replace(" ", "_")

    # Convert to lowercase for consistency
    safe_string = safe_string.lower()

    # Replace any non-OS-safe characters (retain letters, numbers, underscores)
    safe_string = re.sub(r"[^a-z0-9_]", "", safe_string)

    return safe_string


def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def copy_and_save_description(file_path, description, dest_dir):
    """Copy the file to the destination directory and save the description."""
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)
    description_file = os.path.join(dest_dir, f"{os.path.splitext(filename)[0]}.txt")

    # Copy file if it doesn't exist or has different hash
    if not os.path.exists(dest_path) or calculate_hash(file_path) != calculate_hash(
        dest_path
    ):
        shutil.copy2(file_path, dest_path)  # Copy file, preserve metadata
        with open(description_file, "w") as desc_file:
            desc_file.write(description)


def check_and_copy_files(data, project_directory):
    """Check files, compare hash, copy and save description if necessary."""
    for item in data["captions"]:
        file_path = item["file"]
        description = item["description"]

        if os.path.exists(file_path):
            copy_and_save_description(file_path, description, project_directory)
        else:
            print(f"File {file_path} does not exist.")


class gtUILoRATrainingTask:
    DESCRIPTION = "Griptape LoRA: Training Task"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "lora_config": ("LORA_CONFIG", {}),
                "image": ("IMAGE", {}),
                "captions": ("STRING", {"forceInput": True}),
                "job_setting_comment": (
                    "STRING",
                    {"default": "Queue Settings"},
                ),
                "start_job_or_get_status": (
                    ["Start New Job", "Get Status"],
                    {"default": "Start New Job"},
                ),
                "job_settings_comment": (
                    "STRING",
                    {"default": "Job Settings"},
                ),
                "job_title": ("STRING", {"tooltip": "The name of the job."}),
                "project": (
                    "STRING",
                    {
                        "tooltip": "The name of the project, if associated with one",
                        "default": "Train LoRA",
                    },
                ),
                "instance_type": (instance_types, {"default": instance_types[0]}),
                "upload_path": (
                    "STRING",
                    {"default": folder_paths.get_input_directory()},
                ),
                "output_path": (
                    "STRING",
                    {"default": folder_paths.get_output_directory()},
                ),
                "links_comment": (
                    "STRING",
                    {"default": "Links"},
                ),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("JOB_ID", "LOGS")

    FUNCTION = "create"

    CATEGORY = "Griptape/LoRA"

    def create(self, **kwargs):
        lora_config = kwargs.get("lora_config")

        image = kwargs.get("image")
        captions = kwargs.get("captions")
        job_title = kwargs.get("job_title")
        project = kwargs.get("project")
        instance_type = kwargs.get("instance_type")
        instance_type = "cw-epycmilan-4-rtx4000-1"  # HACK: Hardcoded for now

        output_path = kwargs.get("output_path")

        # Copy the images to the training folder
        inputs = folder_paths.get_input_directory()
        project_safe_name = to_safe_os_path(project)
        project_dir = os.path.join(inputs, "projects", project_safe_name)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Copy the images to the training folder
        data = json.loads(captions)
        check_and_copy_files(data, project_dir)

        # with the lora_config, get the model and lora if chosen

        logs = {}
        model = lora_config.get("model")
        include_lora = lora_config.get("include_lora")
        if include_lora:
            base_lora = lora_config.get("base_lora")
        vram = lora_config.get("VRAM")
        repeat_trains_per_image = lora_config.get("repeat_trains_per_image")
        max_train_epochs = lora_config.get("max_train_epochs")
        trigger_word = lora_config.get("trigger_word")
        sample_image_prompts = lora_config.get("sample_image_prompts")
        sample_image_every_n_steps = lora_config.get("sample_image_every_n_steps")
        seed = lora_config.get("seed")
        workers = lora_config.get("workers")
        learning_rate = lora_config.get("learning_rate")
        sample_every_n_epochs = lora_config.get("save_every_n_epochs")
        guidance_scale = lora_config.get("guidance_scale")
        timestep_sampling = lora_config.get("timestep_sampling")
        lora_rank = lora_config.get("lora_rank")
        resize_dataset_images = lora_config.get("resize_dataset_images")

        """
        Example of a command to run the training script:
        (https://github.com/darkstorm2150/sd-scripts/blob/main/docs/train_network_README-en.md)

        accelerate launch --num_cpu_threads_per_process 1 train_network.py 
            --pretrained_model_name_or_path=<.ckpt, .safetensors, or directory of Diffusers version model> 
            --dataset_config=<.toml file created during data preparation> 
            --output_dir=<output folder for trained model>  
            --output_name=<filename for output of trained model> 
            --save_model_as=safetensors 
            --prior_loss_weight=1.0 
            --max_train_steps=400 
            --learning_rate=1e-4 
            --optimizer_type="AdamW8bit" 
            --xformers 
            --mixed_precision="fp16" 
            --cache_latents 
            --gradient_checkpointing
            --save_every_n_epochs=1 
            --network_module=networks.lora
        """
        SCENE_FILE_ROOT = os.path.dirname(os.path.abspath(__file__))

        SUBMISSION = {
            "job_title": job_title,
            "project": project,
            "instance_type": instance_type,
            "software_package_ids": [
                # "7be1b2410b3f93b2a2889f6ce191d4e1"
            ],  # will need pytorch, flux, etc
            "force": False,
            "local_upload": True,
            "preemptible": True,
            "autoretry_policy": None,
            "output_path": output_path,  # local folder where whatever we're pulling is going to be
            "environment": {},
            "upload_paths": [
                # f"{SCENE_FILE_ROOT}/projects/training/images",
                # f"{SCENE_FILE_ROOT}/projects/training/checkpoints",
                # f"{SCENE_FILE_ROOT}/projects/training/loras",
            ],
            "scout_frames": "1",
            "tasks_data": [
                {
                    "command": f'echo "Submitted a LORA training job!\n{lora_config}"',
                    "frames": "1",
                }
            ],
            # "config": lora_config,
        }

        pipeline = Pipeline()
        conductor_task = ToolTask(
            "Calculate 5*2",
            # f"submit a render job: {SUBMISSION}",
            # tool=ConductorTool(),
            tool=CalculatorTool(),
        )
        pipeline.add_task(conductor_task)

        response = pipeline.run()
        print(response)
        status = str(response.output_task.output)
        return {"ui": {"status": status}, "result": (status, SUBMISSION)}
