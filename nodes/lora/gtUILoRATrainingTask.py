instance_types = ["h100", "a100"]


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
                "output_path": ("STRING", {"default": "projects/loras"}),
                "status_comment": (
                    "STRING",
                    {"default": "Status"},
                ),
                "status": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MODEL", "STRING")
    RETURN_NAMES = ("IMAGE", "MODEL", "LOGS")

    FUNCTION = "create"

    CATEGORY = "Griptape/LoRA"

    def create(self, **kwargs):
        lora_config = kwargs.get("lora_config")

        image = kwargs.get("image")
        captions = kwargs.get("captions")
        job_title = kwargs.get("job_title")
        project = kwargs.get("project")
        instance_type = kwargs.get("instance_type")
        output_path = kwargs.get("output_path")
        status = "Not started.."

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

        payload = {
            "job_title": job_title,
            "project": project,
            "instance_type": instance_type,
            "software_package_ids": ["7be1b2410b3f93b2a2889f6ce191d4e1"],
            "force": False,
            "local_upload": True,
            "preemptible": True,
            "autoretry_policy": {"preempted": {"max_retries": 3}},
            "output_path": output_path,
            "environment": {
                "PATH": "/opt/blenderfoundation/blender/2/blender-2.93.0-glibc217",
                "CONDUCTOR_PATHHELPER": "0",
            },
            "upload_paths": [
                "/projects/training/images",
                "/projects/training/checkpoints",
                "/projects/training/loras",
            ],
            "tasks_data": [
                {
                    "command": 'blender -b "/projects/blender/bmw_half_turn_low.blend" -E CYCLES --render-output "/projects/blender/renders/img_" --render-frame 1..1 ',
                    "frames": "1",
                },
                {
                    "command": 'blender -b "/projects/blender/bmw_half_turn_low.blend" -E CYCLES --render-output "/projects/blender/renders/img_" --render-frame 2..2 ',
                    "frames": "2",
                },
                {
                    "command": 'blender -b "/projects/blender/bmw_half_turn_low.blend" -E CYCLES --render-output "/projects/blender/renders/img_" --render-frame 3..3 ',
                    "frames": "3",
                },
            ],
            "config": lora_config,
        }

        return {"ui": {"status": status}, "result": (image, model, payload)}
