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
        instance_type = kwargs.get("instance_type")
        model = ""
        status = "Not started.."
        logs = {}

        print(lora_config)
        payload = {
            "job_title": "Blender example bmw_half_turn_low.blend",
            "project": "default",
            "instance_type": "n1-standard-4",
            "software_package_ids": ["7be1b2410b3f93b2a2889f6ce191d4e1"],
            "force": False,
            "local_upload": True,
            "preemptible": True,
            "autoretry_policy": {"preempted": {"max_retries": 3}},
            "output_path": "projects/blender/renders",
            "environment": {
                "PATH": "/opt/blenderfoundation/blender/2/blender-2.93.0-glibc217",
                "CONDUCTOR_PATHHELPER": "0",
            },
            "upload_paths": [
                "/projects/blender/bmw_half_turn_low.blend",
                "/projects/blender/sourceimages/img_0001.png",
            ],
            "scout_frames": "1,3",
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
        }

        return {"ui": {"status": status}, "result": (image, model, payload)}
